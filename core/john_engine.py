import hashlib
import itertools
import json
import os
import string
import threading
import time
import warnings
from datetime import datetime
from multiprocessing import Manager, Pool, cpu_count
from core.reporting import build_report_header

warnings.filterwarnings("ignore", category=UserWarning)

try:
    from passlib.hash import bcrypt

    HAS_BCRYPT = True
except ImportError:
    HAS_BCRYPT = False


def worker(args):
    word, target_hash, algorithm, salt, use_rules, stop_event = args

    if stop_event.is_set():
        return None

    word = word.replace("\ufeff", "").replace("\r", "").replace("\n", "").strip()
    if not word:
        return None

    if algorithm == "BCRYPT":
        if not HAS_BCRYPT:
            return None
        try:
            if bcrypt.verify(word, target_hash):
                stop_event.set()
                return word
        except Exception:
            return None
        return None

    algo_map = {
        "MD5": hashlib.md5,
        "SHA1": hashlib.sha1,
        "SHA256": hashlib.sha256,
        "SHA512": hashlib.sha512,
    }
    algo_func = algo_map.get(algorithm)
    if not algo_func:
        return None

    variants = {word}
    if use_rules:
        variants |= {word.lower(), word.upper(), word.capitalize(), word[::-1], word + "123", word + "!", "!" + word}

    for variant in variants:
        if stop_event.is_set():
            return None

        test = variant + salt if salt else variant
        digest = algo_func(test.encode()).hexdigest().lower()

        if digest == target_hash:
            stop_event.set()
            return variant

    return None


class JohnEngine:
    def __init__(self):
        self.hash_length_map = {32: "MD5", 40: "SHA1", 64: "SHA256", 128: "SHA512"}
        self.mask_map = {
            "?l": string.ascii_lowercase,
            "?u": string.ascii_uppercase,
            "?d": string.digits,
            "?s": "!@#$%^&*()",
        }

    def detect_algorithm(self, target_hash):
        target_hash = target_hash.strip()
        if target_hash.startswith(("$2a$", "$2b$", "$2y$")):
            return "BCRYPT"
        return self.hash_length_map.get(len(target_hash))

    def crack_wordlist(
        self,
        target_hash,
        wordlist_path,
        algorithm=None,
        salt=None,
        use_rules=False,
        callback=None,
        processes=None,
        external_stop_event=None,
    ):
        target_hash = target_hash.strip().lower()

        if not algorithm:
            algorithm = self.detect_algorithm(target_hash)
            if not algorithm:
                return {"success": False, "error": "Algoritmo não identificado"}

        try:
            with open(wordlist_path, "r", encoding="utf-8", errors="ignore") as file_obj:
                words = file_obj.readlines()
        except Exception as exc:
            return {"success": False, "error": str(exc)}

        processes = processes or cpu_count()
        tested = 0
        start = time.time()

        with Manager() as manager:
            stop_event = manager.Event()
            args = [(word, target_hash, algorithm, salt, use_rules, stop_event) for word in words]

            with Pool(processes) as pool:
                chunksize = 1 if algorithm == "BCRYPT" else 100

                for result in pool.imap_unordered(worker, args, chunksize):
                    tested += 1

                    if callback and tested % 100 == 0:
                        elapsed = time.time() - start
                        speed = int(tested / elapsed) if elapsed > 0 else 0
                        callback(tested, speed)

                    if external_stop_event and external_stop_event.is_set():
                        stop_event.set()
                        pool.terminate()
                        return {"success": False, "error": "Ataque interrompido pelo usuário"}

                    if result:
                        pool.terminate()
                        return {
                            "success": True,
                            "password": result,
                            "hash": target_hash,
                            "algorithm": algorithm,
                            "salt": salt,
                        }

        return {"success": False, "error": "Senha não encontrada"}

    def expand_mask(self, mask):
        pools = []
        index = 0
        while index < len(mask):
            token = mask[index : index + 2]
            if token in self.mask_map:
                pools.append(self.mask_map[token])
                index += 2
            else:
                pools.append(mask[index])
                index += 1
        return ("".join(parts) for parts in itertools.product(*pools))

    def crack_mask(self, target_hash, mask, algorithm=None, salt=None, callback=None, external_stop_event=None):
        target_hash = target_hash.strip().lower()

        if not algorithm:
            algorithm = self.detect_algorithm(target_hash)
            if not algorithm:
                return {"success": False, "error": "Algoritmo não identificado"}

        if algorithm == "BCRYPT":
            return {"success": False, "error": "Modo máscara não suporta BCRYPT"}

        algo_map = {
            "MD5": hashlib.md5,
            "SHA1": hashlib.sha1,
            "SHA256": hashlib.sha256,
            "SHA512": hashlib.sha512,
        }
        algo_func = algo_map.get(algorithm)
        if not algo_func:
            return {"success": False, "error": "Algoritmo inválido"}

        start = time.time()
        tested = 0

        for candidate in self.expand_mask(mask):
            if external_stop_event and external_stop_event.is_set():
                return {"success": False, "error": "Ataque interrompido pelo usuário"}

            tested += 1
            test = candidate + salt if salt else candidate
            digest = algo_func(test.encode()).hexdigest().lower()

            if callback and tested % 1000 == 0:
                elapsed = time.time() - start
                speed = int(tested / elapsed) if elapsed > 0 else 0
                callback(tested, speed)

            if digest == target_hash:
                return {
                    "success": True,
                    "password": candidate,
                    "hash": target_hash,
                    "algorithm": algorithm,
                    "salt": salt,
                }

        return {"success": False, "error": "Senha não encontrada"}

    def save_result(self, result, base_dir, user_context=None):
        log_dir = os.path.join(base_dir, "logs")
        os.makedirs(log_dir, exist_ok=True)

        now = datetime.now()
        data = {
            "report_header": build_report_header(user_context, now),
            "status": "SUCESSO" if result.get("success") else "FALHA",
            "hash": result.get("hash"),
            "algoritmo": result.get("algorithm"),
            "senha": result.get("password"),
            "data": now.strftime("%d/%m/%Y %H:%M:%S"),
            "summary": {
                "algorithm": result.get("algorithm"),
                "password_found": result.get("password"),
                "hash": result.get("hash"),
                "salt": result.get("salt"),
            },
        }

        path = os.path.join(log_dir, f"john_result_{now.strftime('%Y%m%d_%H%M%S')}.json")
        with open(path, "w", encoding="utf-8") as file_obj:
            json.dump(data, file_obj, indent=4, ensure_ascii=False)
        return path


class JohnExecutor:
    def __init__(self, target_hash, payload, algorithm, salt=None, mode="wordlist", rules=False):
        self.target_hash = target_hash
        self.payload = payload
        self.algorithm = algorithm
        self.salt = salt
        self.mode = mode
        self.rules = rules

        self.engine = JohnEngine()
        self.result = None
        self.error = None
        self.total_tested = 0

        self._stop_event = threading.Event()
        self._state_lock = threading.Lock()
        self._running = False
        self._progress = []
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

        self.result = None
        self.error = None
        self.total_tested = 0
        self._progress = []
        self._stop_event.clear()

        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()
        return True

    def stop(self):
        self._stop_event.set()

    def _on_progress(self, tested, speed):
        self._progress.append((tested, speed))
        self.total_tested = tested

    def pop_progress(self):
        items = list(self._progress)
        self._progress.clear()
        return items

    def _run(self):
        try:
            if self.mode == "wordlist":
                self.result = self.engine.crack_wordlist(
                    target_hash=self.target_hash,
                    wordlist_path=self.payload,
                    algorithm=self.algorithm,
                    salt=self.salt,
                    use_rules=self.rules,
                    callback=self._on_progress,
                    external_stop_event=self._stop_event,
                )
            else:
                self.result = self.engine.crack_mask(
                    target_hash=self.target_hash,
                    mask=self.payload,
                    algorithm=self.algorithm,
                    salt=self.salt,
                    callback=self._on_progress,
                    external_stop_event=self._stop_event,
                )
        except Exception as exc:
            self.error = str(exc)
            self.result = {"success": False, "error": self.error}
        finally:
            with self._state_lock:
                self._running = False


def build_john_payload(executor) -> dict:
    """Converte resultado do JohnExecutor para formato JohnResultadoRequest."""
    result = executor.result or {}

    algoritmo = (
        result.get("algorithm")
        or executor.algorithm
        or executor.engine.detect_algorithm(executor.target_hash)
        or "DESCONHECIDO"
    )

    return {
        "hashAlvo": executor.target_hash,
        "algoritmo": algoritmo,
        "salt": executor.salt,
        "senhaEncontrada": result.get("password"),
        "modoAtaque": executor.mode,
        "hashesTestados": executor.total_tested,
        "status": "SUCESSO" if result.get("success") else "FALHA",
    }