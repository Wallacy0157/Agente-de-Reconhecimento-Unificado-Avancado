import sys
import os
import unittest
import subprocess
import tempfile
from unittest.mock import patch, MagicMock, mock_open

sys.modules['services.scan_client'] = MagicMock()
sys.modules['ctypes'] = MagicMock()
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.network_scanner import (
    parse_targets, classify_services, suggest_next_steps,
    extract_ip, extract_os, extract_ports, detect_web_urls,
    extract_vulnerabilities, parse_vulners_output, run_nikto, run_sqlmap,
    build_nmap_command, scan_network_target, scan_single_target, parse_hosts,
    save_json, save_and_persist, _convert_results_to_api_format, is_root,
    NetworkScanExecutor
)


class TestNetworkScannerForcaBruta(unittest.TestCase):

    def test_parse_targets(self):
        self.assertEqual(parse_targets("10.0.0.1, 10.0.0.2"), ["10.0.0.1", "10.0.0.2"])
        self.assertEqual(parse_targets("  \n  "), [])
        self.assertEqual(parse_targets(None), [])

    def test_extract_ip(self):
        self.assertEqual(extract_ip({"address": {"@addrtype": "ipv4", "@addr": "1.1.1.1"}}), "1.1.1.1")
        self.assertEqual(extract_ip({"address": [{"@addrtype": "ipv4", "@addr": "1.1.1.1"}]}), "1.1.1.1")
        self.assertEqual(extract_ip({"address": [{"@addrtype": "mac", "@addr": "00:00"}]}), "N/A")
        self.assertEqual(extract_ip({}), "N/A")

    def test_extract_os(self):
        self.assertEqual(extract_os({"os": {"osmatch": {"@name": "Linux"}}}), "Linux")
        self.assertEqual(extract_os({"os": {"osmatch": [{"@name": "Windows"}]}}), "Windows")
        self.assertEqual(extract_os({}), "Unknown")

    def test_extract_ports(self):

        xml_ports = {
            "ports": {"port": [
                {"@portid": "80", "state": {"@state": "open"}, "service": {"@name": "http"}},
                {"@portid": "22", "state": {"@state": "open"}, "service": {"@name": "tcpwrapped"}},
                {"@portid": "23", "state": {"@state": "open"}, "service": {"@name": "tcpwrapper"}},
                {"@portid": "443", "state": {"@state": "closed"}}
            ]}
        }
        portas = extract_ports(xml_ports)
        self.assertEqual(len(portas), 1)
        self.assertEqual(portas[0]["port"], "80")


        xml_single = {"ports": {"port": {"@portid": "80", "state": {"@state": "open"}, "service": {"@name": "http"}}}}
        self.assertEqual(len(extract_ports(xml_single)), 1)

    def test_classificacao_e_sugestao_total(self):

        portas = [{"service": "http"}, {"service": "https"}, {"service": "mysql"},
                  {"service": "postgresql"}, {"service": "mssql"}, {"service": "oracle"},
                  {"service": "ssh"}, {"service": "ftp"}, {"service": "telnet"}, {"service": "rdp"}]
        perfil = classify_services(portas)
        self.assertTrue(perfil["web"] and perfil["database"] and perfil["remote_access"] and perfil["auth_service"])

        sugestoes = suggest_next_steps(perfil)
        self.assertIn("nikto", sugestoes)
        self.assertIn("sqlmap", sugestoes)
        self.assertIn("hydra", sugestoes)


    def test_detect_web_urls(self):
        portas = [{"service": "http", "port": "80"}, {"service": "ssl/http", "port": "443"},
                  {"service": "ssh", "port": "22"}]
        urls = detect_web_urls("10.0.0.1", portas)
        self.assertEqual(len(urls), 2)

    def test_extract_vulnerabilities_e_parse(self):
        # Lista e Dicionário
        host_vuln = {
            "ports": {"port": [{"@portid": "80", "script": [{"@id": "vulners", "@output": "VULNERABLE: CVE-2021"}]}]}
        }
        self.assertEqual(len(extract_vulnerabilities(host_vuln)), 1)

        vulners_data = {"CVE-123": {"cvss": 9.8, "href": "url", "exploit": True}, "NONCVE-1": {}}
        parsed = parse_vulners_output(vulners_data, 80)
        self.assertEqual(parsed[0]["cve"], "CVE-123")
        self.assertIsNone(parsed[1]["cve"])

    @patch("core.network_scanner.shutil.which")
    @patch("core.network_scanner.subprocess.run")
    def test_ferramentas_web_todos_retornos(self, mock_run, mock_which):
        mock_which.return_value = None
        self.assertIn("não está instalado", run_nikto("http://alvo")["error"])
        self.assertIn("não está instalado", run_sqlmap("http://alvo")["error"])


        mock_which.return_value = "/usr/bin/tool"
        mock_run.side_effect = subprocess.TimeoutExpired(cmd="tool", timeout=10)
        self.assertIn("timeout", run_nikto("http://alvo")["error"])
        self.assertIn("timeout", run_sqlmap("http://alvo")["error"])


        mock_run.side_effect = None
        mock_run.return_value = MagicMock(stdout="Encontrado")
        self.assertEqual(run_nikto("http://alvo")["status"], "executed")
        self.assertEqual(run_sqlmap("http://alvo")["status"], "executed")


    def test_build_nmap_command(self):
        with patch("core.network_scanner.os.name", "nt"):
            self.assertIn("nmap.exe", build_nmap_command("10.0.0.1")[0])

        with patch("core.network_scanner.os.name", "posix"):
            with patch("core.network_scanner.os.geteuid", return_value=0, create=True):
                self.assertIn("-O", build_nmap_command("10.0.0.1"))
            with patch("core.network_scanner.os.geteuid", return_value=1000, create=True):
                self.assertNotIn("-O", build_nmap_command("10.0.0.1"))

    def test_is_root_exaustivo(self):
        with patch("core.network_scanner.os.name", "posix"):
            with patch("core.network_scanner.os.geteuid", return_value=0, create=True):
                self.assertTrue(is_root())


        with patch("core.network_scanner.os.name", "nt"):
            import ctypes
            ctypes.windll.shell32.IsUserAnAdmin.side_effect = None
            ctypes.windll.shell32.IsUserAnAdmin.return_value = 1
            self.assertTrue(is_root())


        with patch("core.network_scanner.os.name", "nt"):
            import ctypes
            ctypes.windll.shell32.IsUserAnAdmin.side_effect = Exception("DLL Quebrada")
            self.assertFalse(is_root())


            ctypes.windll.shell32.IsUserAnAdmin.side_effect = None


    @patch("core.network_scanner.run_nikto")
    @patch("core.network_scanner.run_sqlmap")
    def test_parse_hosts(self, mock_sql, mock_nikto):
        mock_nikto.return_value = {"status": "ok"}
        mock_sql.return_value = {"status": "ok"}


        xml_data = {
            "nmaprun": {
                "host": {"address": {"@addr": "1.1.1.1", "@addrtype": "ipv4"},
                         "ports": {
                             "port": {"@portid": "80", "state": {"@state": "open"}, "service": {"@name": "http"}}}}
            }
        }
        res = parse_hosts(xml_data)
        self.assertIn("nikto", res[0]["web_assessment"])


        self.assertEqual(parse_hosts({"nmaprun": {}}), [])

    @patch("core.network_scanner.subprocess.run")
    def test_scan_network_target_falhas_e_sucessos(self, mock_run):
        scan_network_target(["  "])


        mock_run.return_value = MagicMock(returncode=1, stderr="Erro fatal")
        self.assertIn("Erro fatal", scan_network_target(["10.0.0.1"])[0]["error"])


        mock_run.side_effect = subprocess.TimeoutExpired(cmd="nmap", timeout=10)
        self.assertEqual(scan_network_target(["10.0.0.1"])[0]["error"], "Scan timeout")


        mock_run.side_effect = None
        mock_run.return_value = MagicMock(returncode=0,
                                          stdout="<nmaprun><host><address addr='1.1.1.1' addrtype='ipv4'/></host></nmaprun>")
        self.assertEqual(scan_network_target(["1.1.1.1"])[0]["ip"], "1.1.1.1")

    @patch("core.network_scanner.scan_network_target")
    def test_scan_single_target(self, mock_scan):
        mock_scan.return_value = [{"ip": "10.0.0.1"}]
        self.assertEqual(scan_single_target("10.0.0.1")["ip"], "10.0.0.1")

        mock_scan.return_value = []
        self.assertIn("Nenhum resultado", scan_single_target("10.0.0.1")["error"])


    def test_formatacao_api(self):
        dados = [
            {"ip": "10.0.0.1", "open_ports": [{"port": "80", "protocol": "tcp"}], "vulnerabilities": [{"port": "80"}]}]
        form = _convert_results_to_api_format(dados)
        self.assertEqual(form[0]["openPorts"][0]["port"], 80)

    def test_save_json_real(self):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".json") as tmp:
            tmp_name = tmp.name
        try:
            rep = save_json([], tmp_name)
            self.assertIn("scan_metadata", rep)
        finally:
            os.remove(tmp_name)

    @patch("core.network_scanner.save_json")
    @patch("services.scan_client.enviar_resultado_scan")
    def test_save_and_persist_api(self, mock_enviar, mock_save):
        mock_save.return_value = {"scan_metadata": {"scan_date": "d", "scan_time": "t", "timezone": "z"}, "results": []}


        mock_enviar.return_value = {"id": 123}
        rep, api = save_and_persist([], "fake.json")
        self.assertEqual(api["id"], 123)


        mock_enviar.return_value = None
        rep, api2 = save_and_persist([], "fake.json")
        self.assertIsNone(api2)

        # Exceção Grave na Requisição API
        mock_enviar.side_effect = Exception("API Offline Brutal")
        rep, api3 = save_and_persist([], "fake.json")
        self.assertIsNone(api3)


    @patch("core.network_scanner.scan_single_target")
    def test_executor_logica_completa(self, mock_scan):

        ex_vazio = NetworkScanExecutor([])
        ex_vazio._run()
        self.assertEqual(ex_vazio.get_error(), "Nenhum alvo válido informado para varredura.")


        mock_scan.side_effect = Exception("Falha Catastrófica de Memória")
        ex_crash = NetworkScanExecutor(["1.1.1.1"])
        ex_crash._run()  # Chamando o método _run diretamente para evitar problemas de concorrência no teste
        self.assertEqual(ex_crash.get_error(), "Falha Catastrófica de Memória")


        mock_scan.side_effect = None
        mock_scan.return_value = {"ip": "1.1.1.1"}
        ex_stop = NetworkScanExecutor(["1.1.1.1", "2.2.2.2"])
        ex_stop.stop()
        ex_stop._run()
        self.assertIn("interrompida", ex_stop.get_progress_message())


if __name__ == '__main__':
    unittest.main()