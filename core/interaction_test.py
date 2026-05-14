import ctypes
import hashlib
import os
import platform
import socket
import stat
import threading
from datetime import datetime

import psutil


def is_admin():
    try:
        return os.getuid() == 0
    except AttributeError:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0


def get_system_metadata():
    return {
        "hostname": socket.gethostname(),
        "os": f"{platform.system()} {platform.release()}",
        "user": os.getlogin(),
        "arch": platform.architecture()[0],
        "ip_local": socket.gethostbyname(socket.gethostname()),
    }


def check_world_writable(path):
    try:
        st = os.stat(path)
        return bool(st.st_mode & stat.S_IWOTH)
    except Exception:
        return False


def scan_ports():
    open_ports = []
    for port in [21, 22, 80, 443, 3306, 8080]:
        sock = socket.socket()
        sock.settimeout(0.3)
        try:
            sock.connect(("127.0.0.1", port))
            open_ports.append(port)
        except Exception:
            pass
        finally:
            sock.close()
    return open_ports


def list_suspicious_processes():
    suspicious = []
    for process in psutil.process_iter(["name"]):
        try:
            name = (process.info["name"] or "").lower()
            if any(flag in name for flag in ["keylogger", "hack", "inject", "rat"]):
                suspicious.append(name)
        except Exception:
            continue
    return suspicious


def hash_file(path):
    try:
        with open(path, "rb") as file_obj:
            return hashlib.sha256(file_obj.read()).hexdigest()
    except Exception:
        return None


def check_firewall():
    if os.name != "nt":
        return os.system("ufw status > /dev/null 2>&1") == 0
    return os.system("netsh advfirewall show allprofiles > nul") == 0


def run_interaction_test(base_dir):
    log_path = os.path.join(base_dir, "logs", "auditoria_seguranca.log")
    os.makedirs(os.path.dirname(log_path), exist_ok=True)

    meta = get_system_metadata()
    results = []

    with open(log_path, "a", encoding="utf-8") as log:
        log.write("\n" + "=" * 60 + "\n")
        log.write("AURA SECURITY TOOLKIT - RELATÓRIO DE SEGURANÇA\n")
        log.write(f"DATA/HORA: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
        log.write(f"ESTAÇÃO: {meta['hostname']} ({meta['ip_local']})\n")
        log.write(f"USUÁRIO: {meta['user']}\n")
        log.write(f"SISTEMA: {meta['os']} [{meta['arch']}]\n")
        log.write("-" * 60 + "\n")

        if is_admin():
            results.append("[HIGH] Execução com privilégios elevados (Admin/Root)")
        else:
            results.append("[OK] Execução com privilégios limitados")

        test_path = "/tmp" if os.name != "nt" else os.environ.get("TEMP", "C:\\Temp")
        if check_world_writable(test_path):
            results.append(f"[MEDIUM] Diretório {test_path} com permissão global de escrita")
        else:
            results.append(f"[OK] Permissões seguras em {test_path}")

        ports = scan_ports()
        if ports:
            results.append(f"[MEDIUM] Portas abertas detectadas: {ports}")
        else:
            results.append("[OK] Nenhuma porta crítica aberta")

        processes = list_suspicious_processes()
        if processes:
            results.append(f"[HIGH] Processos suspeitos: {processes}")
        else:
            results.append("[OK] Nenhum processo suspeito identificado")

        if check_firewall():
            results.append("[OK] Firewall ativo")
        else:
            results.append("[HIGH] Firewall pode estar desativado")

        target_file = "/etc/hosts" if os.name != "nt" else r"C:\Windows\System32\drivers\etc\hosts"
        file_hash = hash_file(target_file)

        if file_hash:
            results.append(f"[INFO] Hash do arquivo hosts: {file_hash[:16]}...")
        else:
            results.append("[LOW] Não foi possível gerar hash do arquivo crítico")

        for result in results:
            log.write(result + "\n")

        log.write("-" * 60 + "\n")
        log.write(f"HASH DO RELATÓRIO: {hashlib.sha256(str(results).encode()).hexdigest()}\n")
        log.write("=" * 60 + "\n")

    return results, meta, log_path


class InteractionTestExecutor:
    def __init__(self, base_dir):
        self.base_dir = base_dir
        self.results = None
        self.meta = None
        self.log_path = None
        self.error = None

        self._state_lock = threading.Lock()
        self._running = False
        self._thread = None

    @property
    def is_running(self):
        with self._state_lock:
            return self._running

    def start(self):
        with self._state_lock:
            if self._running:
                return False
            self._running = True

        self.results = None
        self.meta = None
        self.log_path = None
        self.error = None

        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()
        return True

    def _run(self):
        try:
            self.results, self.meta, self.log_path = run_interaction_test(self.base_dir)
        except Exception as exc:
            self.error = str(exc)
        finally:
            with self._state_lock:
                self._running = False
