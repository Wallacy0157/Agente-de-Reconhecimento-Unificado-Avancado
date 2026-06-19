import subprocess
import xmltodict
import json
import os
import pytz
import shutil
import re
import threading
from datetime import datetime
from core.reporting import build_report_header

NMAP_BASE_CMD = [
    "nmap",
    "-sV",
    "-O",
    "--script", "vuln",
    "-oX", "-"
]

def parse_targets(raw_targets: str):
    if not raw_targets or not raw_targets.strip():
        return []
    return [item.strip() for item in re.split(r"[,\s]+", raw_targets) if item.strip()]


class NetworkScanExecutor:
    def __init__(self, targets: list[str]):
        self._targets = [target.strip() for target in targets if target and target.strip()]
        self._results = []
        self._error = None
        self._progress_message = ""
        self._stop_event = threading.Event()
        self._state_lock = threading.Lock()
        self._running = False
        self._worker_thread = None

    @property
    def is_running(self):
        with self._state_lock:
            return self._running

    def start(self):
        with self._state_lock:
            if self._running:
                return False
            self._running = True

        self._results = []
        self._error = None
        self._progress_message = "Iniciando varredura..."
        self._stop_event.clear()
        self._worker_thread = threading.Thread(target=self._run, daemon=True)
        self._worker_thread.start()
        return True

    def stop(self):
        self._stop_event.set()

    def get_results(self):
        return list(self._results)

    def get_error(self):
        return self._error

    def get_progress_message(self):
        return self._progress_message

    def _run(self):
        try:
            total = len(self._targets)
            if total == 0:
                self._error = "Nenhum alvo válido informado para varredura."
                return

            for index, ip in enumerate(self._targets, start=1):
                if self._stop_event.is_set():
                    self._progress_message = "Varredura interrompida pelo usuário."
                    break

                self._progress_message = f"🔍 Escaneando {ip} ({index}/{total})"
                self._results.append(scan_single_target(ip))

            if not self._progress_message:
                self._progress_message = "Varredura concluída."

        except Exception as exc:
            self._error = str(exc)
        finally:
            with self._state_lock:
                self._running = False

def classify_services(open_ports):
    profile = {
        "web": False,
        "database": False,
        "remote_access": False,
        "auth_service": False
    }

    for p in open_ports:
        service = p.get("service", "").lower()

        if service in ["http", "https"]:
            profile["web"] = True

        if service in ["mysql", "postgresql", "mssql", "oracle"]:
            profile["database"] = True

        if service in ["ssh", "ftp", "telnet", "rdp"]:
            profile["remote_access"] = True
            profile["auth_service"] = True

    return profile


def suggest_next_steps(service_profile):
    suggestions = []

    if service_profile.get("web"):
        suggestions.append("nikto")

    if service_profile.get("database"):
        suggestions.append("sqlmap")

    if service_profile.get("auth_service"):
        suggestions.append("hydra")

    return suggestions


def scan_network_target(ip_list: list):
    all_results = []

    for ip in ip_list:
        ip = ip.strip()
        if not ip:
            continue

        print(f"[*] Scanning {ip} with Nmap...")

        cmd = build_nmap_command(ip)

        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300
            )

            if result.returncode != 0:
                raise RuntimeError(result.stderr.strip())

            data_dict = xmltodict.parse(result.stdout)
            parsed_hosts = parse_hosts(data_dict)
            all_results.extend(parsed_hosts)

        except subprocess.TimeoutExpired:
            print(f"[!] Timeout scanning {ip}")
            all_results.append({
                "ip": ip,
                "error": "Scan timeout"
            })

        except Exception as e:
            print(f"[ERRO] {ip}: {e}")
            all_results.append({
                "ip": ip,
                "error": str(e)
            })

    return all_results

def scan_single_target(ip: str):
    results = scan_network_target([ip])

    if results:
        return results[0]

    return {
        "ip": ip,
        "error": "Nenhum resultado retornado"
    }


def parse_hosts(data):
    results = []

    nmaprun = data.get("nmaprun", {})

    if "host" not in nmaprun:
        return []

    hosts = nmaprun["host"]

    if isinstance(hosts, dict):
        hosts = [hosts]

    for host in hosts:
        info = {
            "ip": extract_ip(host),
            "os": extract_os(host),
            "open_ports": extract_ports(host)
        }

        info["service_profile"] = classify_services(info["open_ports"])
        info["suggested_tests"] = suggest_next_steps(info["service_profile"])
        info["vulnerabilities"] = extract_vulnerabilities(host)
        info["web_assessment"] = {}

        urls = detect_web_urls(info["ip"], info["open_ports"])

        if urls:
            info["web_assessment"]["detected_urls"] = urls

            # Nikto
            info["web_assessment"]["nikto"] = []
            for url in urls:
                info["web_assessment"]["nikto"].append({
                    "url": url,
                    "result": run_nikto(url)
                })

            # SQLMap
            info["web_assessment"]["sqlmap"] = []
            for url in urls:
                info["web_assessment"]["sqlmap"].append({
                    "url": url,
                    "result": run_sqlmap(url)
                })

        results.append(info)

    return results

def extract_ip(host):
    addresses = host.get("address", [])
    if isinstance(addresses, dict):
        addresses = [addresses]

    for addr in addresses:
        if addr.get("@addrtype") == "ipv4":
            return addr.get("@addr")

    return "N/A"

def extract_os(host):
    os_data = host.get("os", {}).get("osmatch")
    if isinstance(os_data, list):
        return os_data[0].get("@name", "Unknown")
    if isinstance(os_data, dict):
        return os_data.get("@name", "Unknown")
    return "Unknown"

def extract_ports(host):
    ports_data = host.get("ports", {}).get("port", [])
    if isinstance(ports_data, dict):
        ports_data = [ports_data]

    open_ports = []

    for port in ports_data:
        if port.get("state", {}).get("@state") != "open":
            continue

        service = port.get("service", {}).get("@name", "").lower()
        if service in ["tcpwrapped", "tcpwrapper"]:
            continue

        open_ports.append({
            "port": port.get("@portid"),
            "protocol": port.get("@protocol"),
            "service": service,
            "product": port.get("service", {}).get("@product"),
            "version": port.get("service", {}).get("@version"),
            "extra_info": port.get("service", {}).get("@extrainfo"),
        })

    return open_ports

def detect_web_urls(ip, open_ports):
    urls = []

    for p in open_ports:
        service = p["service"].lower()

        if service == "http":
            urls.append(f"http://{ip}:{p['port']}")

        elif service in ["https", "ssl/http"]:
            urls.append(f"https://{ip}:{p['port']}")

    return urls

def run_nikto(url):
    if not shutil.which("nikto"):
        return {"error": "Nikto não está instalado"}

    print(f"[+] Rodando Nikto em {url}...")

    try:
        result = subprocess.run(
            ["nikto", "-h", url],
            capture_output=True,
            text=True,
            timeout=600
        )

        return {
            "status": "executed",
            "output": result.stdout[:8000]
        }

    except subprocess.TimeoutExpired:
        return {"error": "Nikto timeout"}

def run_sqlmap(url):
    if not shutil.which("sqlmap"):
        return {"error": "SQLMap não está instalado"}

    print(f"[+] Preparando SQLMap para {url}...")

    cmd = [
        "sqlmap",
        "-u", url,
        "--batch",
        "--level=1",
        "--risk=1",
        "--crawl=1"
    ]

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=900
        )

        return {
            "status": "executed",
            "output": result.stdout[:8000]
        }

    except subprocess.TimeoutExpired:
        return {"error": "SQLMap timeout"}

def extract_vulnerabilities(host):
    vulns = []
    ports = host.get("ports", {}).get("port", [])
    if isinstance(ports, dict):
        ports = [ports]

    for port in ports:
        scripts = port.get("script", [])
        if isinstance(scripts, dict):
            scripts = [scripts]

        for script in scripts:
            output = script.get("@output", "")
            if any(keyword in output.upper() for keyword in ["VULNERABLE", "CVE-", "EXPLOIT"]):
                vulns.append({
                    "port": port.get("@portid"),
                    "script": script.get("@id"),
                    "details": output
                })

    return vulns

def parse_vulners_output(vulners_data: dict, port: int):
    vulns = []

    for vuln_id, vuln_data in vulners_data.items():
        vulns.append({
            "cve": vuln_id if vuln_id.startswith("CVE") else None,
            "cvss": vuln_data.get("cvss"),
            "source": "vulners",
            "url": vuln_data.get("href"),
            "port": port,
            "exploit_available": vuln_data.get("exploit", False)
        })

    return vulns


def build_nmap_command(ip):
    # Aponta direto para o caminho padrão do Nmap no Windows 🛠️
    cmd = [
        "C:\\Program Files (x86)\\Nmap\\nmap.exe", 
        "-sV", 
        "--script", "vuln,http-enum,http-headers,http-methods", 
        "-oX", "-"
    ]

    # Se NÃO for Windows (ou seja, Linux/Mac), ele volta para o comando padrão
    if os.name != "nt":
        cmd[0] = "nmap"
        if os.geteuid() == 0:
            cmd.insert(1, "-O")
        else:
            print("[!] Rodando sem OS detection (sem privilégios)")
    else:
        print("[!] Usando o caminho absoluto do Nmap no Windows.")

    cmd.append(ip)
    return cmd

def _summarize_open_ports(results):
    ports = []
    for host in results:
        ip = host.get("ip", "N/A")
        for item in host.get("open_ports", []):
            service_parts = [
                item.get("service"),
                item.get("product"),
                item.get("version"),
                item.get("extra_info"),
            ]
            service_detail = " ".join(str(part) for part in service_parts if part)
            port = item.get("port", "N/A")
            protocol = (item.get("protocol") or "").upper() or "N/A"
            ports.append({
                "host": ip,
                "port": port,
                "protocol": protocol,
                "service": item.get("service") or "N/A",
                "product": item.get("product"),
                "version": item.get("version"),
                "description": f"{port}/{protocol} - {service_detail or 'Serviço não identificado'}",
            })
    return ports


def save_json(results, filename, user_context=None):
    tz = pytz.timezone("America/Sao_Paulo")
    now = datetime.now(tz)

    report = {
        "report_header": build_report_header(user_context, now),
        "scan_metadata": {
            "tool": "AURA - Advanced Unified Reconnaissance Agent",
            "scan_date": now.strftime("%Y-%m-%d"),
            "scan_time": now.strftime("%H:%M:%S"),
            "timezone": "America/Sao_Paulo"
        },
        "nmap_summary": {
            "total_hosts": len(results),
            "open_ports": _summarize_open_ports(results),
        },
        "results": results
    }

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=4, ensure_ascii=False)

    return report


def save_and_persist(results, filename, user_context=None):
    import logging
    logger = logging.getLogger(__name__)

    report = save_json(results, filename, user_context=user_context)

    api_response = None
    try:
        from services.scan_client import enviar_resultado_scan

        payload = {
            "metadata": {
                "scanDate": report["scan_metadata"]["scan_date"],
                "scanTime": report["scan_metadata"]["scan_time"],
                "timezone": report["scan_metadata"]["timezone"],
            },
            "results": _convert_results_to_api_format(report["results"]),
        }

        api_response = enviar_resultado_scan(payload)

        if api_response is not None:
            logger.info(
                "Scan persistido no backend com sucesso (ID: %s).",
                api_response.get("id"),
            )
        else:
            logger.warning(
                "Falha ao persistir scan no backend. Resultados salvos apenas localmente em: %s",
                filename,
            )

    except Exception as exc:
        logger.error("Erro inesperado ao tentar persistir scan no backend: %s", exc)
        api_response = None

    return report, api_response


def _convert_results_to_api_format(results: list) -> list:
    api_results = []

    for host in results:
        api_host = {
            "ip": host.get("ip", ""),
            "os": host.get("os"),
            "error": host.get("error"),
            "openPorts": [],
            "serviceProfile": None,
            "suggestedTests": host.get("suggested_tests", []),
            "vulnerabilities": [],
        }

        for port in host.get("open_ports", []):
            api_host["openPorts"].append({
                "port": int(port["port"]) if port.get("port") else None,
                "protocol": port.get("protocol", ""),
                "service": port.get("service", ""),
            })

        sp = host.get("service_profile")
        if sp:
            api_host["serviceProfile"] = {
                "web": sp.get("web", False),
                "database": sp.get("database", False),
                "remoteAccess": sp.get("remote_access", False),
                "authService": sp.get("auth_service", False),
            }

        for vuln in host.get("vulnerabilities", []):
            api_host["vulnerabilities"].append({
                "port": str(vuln.get("port", "")),
                "script": vuln.get("script", ""),
                "details": vuln.get("details", ""),
            })

        api_results.append(api_host)

    return api_results

def is_root():
    if os.name != "nt":
        return os.geteuid() == 0
    else:
        import ctypes
        try:
            return ctypes.windll.shell32.IsUserAnAdmin() != 0
        except Exception:
            return False