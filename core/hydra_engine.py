import json
import os
import re
import shutil
import subprocess
import tempfile
import threading
import uuid
from datetime import datetime


class HydraExecutor:
    def __init__(
        self,
        targets,
        service,
        username,
        password,
        user_list,
        pass_list,
        port,
        tasks,
        stop_on_success,
        verbose,
        http_path=None,
        http_params=None,
        http_fail=None,
    ):
        self.targets = [t.strip() for t in targets if t and t.strip()]
        self.service = service
        self.username = username
        self.password = password
        self.user_list = user_list
        self.pass_list = pass_list
        self.port = port
        self.tasks = tasks
        self.stop_on_success = stop_on_success
        self.verbose = verbose
        self.http_path = http_path
        self.http_params = http_params
        self.http_fail = http_fail

        self.targets_file = None
        self.process = None
        self.start_time = None
        self.return_code = None
        self.error = None

        self._state_lock = threading.Lock()
        self._running = False
        self._stop_requested = False
        self._output_lines = []
        self._pending_lines = []
        self._thread = None

    @staticmethod
    def parse_targets(raw_targets):
        return [t.strip() for t in re.split(r"[,\s]+", raw_targets or "") if t.strip()]

    @property
    def is_running(self):
        with self._state_lock:
            return self._running

    def start(self):
        with self._state_lock:
            if self._running:
                return False
            self._running = True

        self.return_code = None
        self.error = None
        self.start_time = datetime.now()
        self._stop_requested = False
        self._output_lines = []
        self._pending_lines = []

        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()
        return True

    def stop(self):
        self._stop_requested = True
        if self.process and self.process.poll() is None:
            try:
                self.process.terminate()
            except Exception:
                pass

    def pop_new_output(self):
        pending = list(self._pending_lines)
        self._pending_lines.clear()
        return pending

    def get_output(self):
        return list(self._output_lines)

    def _append_output(self, line):
        self._output_lines.append(line)
        self._pending_lines.append(line)

    def _validate(self):
        if not self.targets:
            return "Informe ao menos um alvo."

        if not self.service:
            return "Informe o serviço."

        if self.service == "http-post-form":
            if not all([self.http_path, self.http_params, self.http_fail]):
                return "Preencha todos os campos do HTTP POST."
            if "^USER^" not in self.http_params or "^PASS^" not in self.http_params:
                return "Use ^USER^ e ^PASS^ nos parâmetros."

        return None

    def _write_targets_file(self):
        if len(self.targets) <= 1:
            self.targets_file = None
            return

        tmp = tempfile.NamedTemporaryFile(delete=False, mode="w", encoding="utf-8", suffix=".txt")
        tmp.write("\n".join(self.targets))
        tmp.close()
        self.targets_file = tmp.name

    def _build_command(self):
        cmd = ["hydra", "-I"]

        if self.tasks:
            cmd.extend(["-t", str(self.tasks)])
        if self.stop_on_success:
            cmd.append("-f")
        if self.verbose:
            cmd.append("-V")
        if self.port:
            cmd.extend(["-s", str(self.port)])

        if self.user_list:
            cmd.extend(["-L", self.user_list])
        elif self.username:
            cmd.extend(["-l", self.username])

        if self.pass_list:
            cmd.extend(["-P", self.pass_list])
        elif self.password:
            cmd.extend(["-p", self.password])

        if self.targets_file:
            cmd.extend(["-M", self.targets_file])
        else:
            cmd.append(self.targets[0])

        if self.service == "http-post-form":
            cmd.append("http-post-form")
            cmd.append(f"{self.http_path}:{self.http_params}:{self.http_fail}")
        else:
            cmd.append(self.service)

        return cmd

    def _run(self):
        try:
            validation_error = self._validate()
            if validation_error:
                self.error = validation_error
                self._append_output(f"[ERRO] {validation_error}")
                self.return_code = 1
                return

            if not shutil.which("hydra"):
                self.error = "Hydra não encontrado no PATH."
                self._append_output(f"[ERRO] {self.error}")
                self.return_code = 127
                return

            self._write_targets_file()
            cmd = self._build_command()
            self._append_output(f"[INFO] Executando: {' '.join(cmd)}")

            self.process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
            )

            for line in self.process.stdout:
                if self._stop_requested:
                    self._append_output("[INFO] Ataque interrompido pelo usuário.")
                    break
                self._append_output(line.rstrip())

            if self._stop_requested and self.process.poll() is None:
                self.process.terminate()

            self.return_code = self.process.wait()

        except Exception as exc:
            self.error = f"Erro ao executar Hydra: {exc}"
            self._append_output(f"[ERRO] {self.error}")
            self.return_code = 1
        finally:
            if self.targets_file and os.path.exists(self.targets_file):
                try:
                    os.remove(self.targets_file)
                except OSError:
                    pass
            with self._state_lock:
                self._running = False

    def save_log(self, base_dir):
        log_dir = os.path.join(base_dir, "logs")
        os.makedirs(log_dir, exist_ok=True)

        now = datetime.now()
        duration = None
        if self.start_time:
            duration = (now - self.start_time).total_seconds()

        success = self.return_code == 0
        found_creds = None
        if success and self.username and self.password:
            found_creds = {"username": self.username, "password": self.password}

        log_data = {
            "attack_id": str(uuid.uuid4()),
            "tool": "Hydra",
            "timestamp": now.isoformat(),
            "duration_seconds": duration,
            "targets": self.targets,
            "service": self.service,
            "port": self.port,
            "attack_type": "single" if self.username and self.password else "wordlist",
            "severity": "HIGH" if success else "INFO",
            "success": success,
            "credentials_found": found_creds if success else None,
            "evidence": "Valid credentials found" if success else "No credentials found",
            "return_code": self.return_code,
        }

        filename = f"hydra_{now.strftime('%Y-%m-%d_%H-%M-%S')}.json"
        filepath = os.path.join(log_dir, filename)

        with open(filepath, "w", encoding="utf-8") as file_obj:
            json.dump(log_data, file_obj, indent=4, ensure_ascii=False)

        return filepath


def parse_credentials(output_lines):
    """Parseia credenciais encontradas do output do Hydra. """
    credentials = []
    pattern = re.compile(
        r'\[(\d+)\]\[([^\]]+)\]\s+host:\s+(\S+)\s+login:\s+(\S+)\s+password:\s+(.+)'
    )
    for line in output_lines:
        match = pattern.search(line)
        if match:
            credentials.append({
                "username": match.group(4),
                "password": match.group(5).strip(),
            })
    return credentials


def build_hydra_payload(executor) -> dict:
    """Converte resultado do HydraExecutor para formato HydraResultadoRequest."""
    from datetime import datetime, timezone

    output = executor.get_output()
    sucesso = executor.return_code == 0

    credenciais = parse_credentials(output)

    if not credenciais and sucesso and executor.username and executor.password:
        credenciais = [{"username": executor.username, "password": executor.password}]

    # Tipo de ataque
    if executor.user_list or executor.pass_list:
        tipo_ataque = "wordlist"
    else:
        tipo_ataque = "single"

    now = datetime.now(timezone.utc)
    inicio = executor.start_time.astimezone(timezone.utc).isoformat() if executor.start_time else now.isoformat()

    return {
        "servico": executor.service,
        "porta": executor.port or 0,
        "tipoAtaque": tipo_ataque,
        "sucesso": sucesso,
        "inicio": inicio,
        "fim": now.isoformat(),
        "alvos": executor.targets,
        "credenciaisEncontradas": credenciais if credenciais else [],
    }
