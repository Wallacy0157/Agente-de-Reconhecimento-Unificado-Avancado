import os
import sys
import webbrowser
from auth_ui import AuthWindow
from PyQt6.QtCore import (
    Qt, QTimer
)
from PyQt6.QtGui import (
    QFont
)
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel, QStackedWidget,
    QVBoxLayout, QHBoxLayout, QFrame, QPushButton, QSpacerItem,
    QSizePolicy, QScrollArea, 
    QGridLayout, QSpacerItem, 
    QSizePolicy, QTabWidget
)
from random import randint
from core.components import (
    NeonCard, ConfigPage, 
    load_language_json, lang_get 
) 
from core.config import (
    THEMES, load_user_settings,
    save_user_settings, ThemeManager, MANUAL_STYLES, main_window_stylesheet,
)

# --- DIAGNOSTICO ---
class EnvironmentDiagnosticsPage(QWidget):
    TOOL_CHECKS = [
        ("Nmap", "nmap"),
        ("Nikto", "nikto"),
        ("SQLMap", "sqlmap"),
    ]

    def __init__(self, parent_window):
        super().__init__()
        self.parent_window = parent_window
        self.last_results = {}
        self.L = getattr(parent_window, 'L', {})
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)

        self.title_label = QLabel(lang_get(self.L, "diagnostics_page.title", "Diagnóstico do Ambiente"))
        self.title_label.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        layout.addWidget(self.title_label)

        self.description_label = QLabel(
            lang_get(self.L, "diagnostics_page.install_description",
                     "Verifica se as ferramentas principais já estão instaladas no sistema.")
        )
        self.description_label.setWordWrap(True)
        layout.addWidget(self.description_label)

        self.run_button = QPushButton(lang_get(self.L, "diagnostics_page.run_diagnostic", "Executar diagnóstico"))
        self.run_button.clicked.connect(self.run_diagnostics)
        layout.addWidget(self.run_button)

        self.result_box = QTextEdit()
        self.result_box.setReadOnly(True)
        self.result_box.setMinimumHeight(220)
        self.result_box.setObjectName("ResultBox")
        self.result_box.setText(lang_get(self.L, "diagnostics_page.description",
                                         "Clique em 'Executar diagnóstico' para verificar o ambiente."))
        layout.addWidget(self.result_box)

        self.install_button = QPushButton(
            lang_get(self.L, "diagnostics_page.install_missing", "Instalar dependências faltantes (Linux/apt)"))
        self.install_button.setEnabled(False)
        self.install_button.clicked.connect(self.install_missing_tools)
        layout.addWidget(self.install_button)

        layout.addStretch()

    def update_ui_language(self, L):
        self.L = L
        self.title_label.setText(lang_get(self.L, "diagnostics_page.title", "Diagnóstico do Ambiente"))
        self.description_label.setText(
            lang_get(
                self.L,
                "diagnostics_page.install_description",
                "Verifica se as ferramentas principais já estão instaladas no sistema.",
            )
        )
        self.run_button.setText(lang_get(self.L, "diagnostics_page.run_diagnostic", "Executar diagnóstico"))
        self.install_button.setText(
            lang_get(
                self.L,
                "diagnostics_page.install_missing",
                "Instalar dependências faltantes (Linux/apt)",
            )
        )

    def run_diagnostics(self):
        lines = [lang_get(self.L, "diagnostics_page.tools_diagnostic", "--- Diagnóstico de Ferramentas ---")]
        missing_tools = []
        self.last_results = {}

        for tool_name, cmd in self.TOOL_CHECKS:
            detected = shutil.which(cmd) is not None
            self.last_results[tool_name] = detected

            if detected:
                lines.append(lang_get(self.L, "diagnostics_page.detected", "✔ {tool_name} detectado").format(
                    tool_name=tool_name))
            else:
                lines.append(lang_get(self.L, "diagnostics_page.not_found", "❌ {tool_name} não encontrado").format(
                    tool_name=tool_name))
                missing_tools.append(cmd)

        if missing_tools:
            lines.append("\n" + lang_get(self.L, "diagnostics_page.install_auto",
                                         "Você pode instalar itens faltantes automaticamente no Linux (apt)."))
        else:
            lines.append(
                "\n" + lang_get(self.L, "diagnostics_page.environment_ready", "Ambiente pronto: tudo detectado."))

        self.result_box.setText("\n".join(lines))
        self.install_button.setEnabled(bool(missing_tools))

    def install_missing_tools(self):
        missing = [cmd for name, cmd in self.TOOL_CHECKS if not self.last_results.get(name, False)]
        if not missing:
            QMessageBox.information(self, lang_get(self.L, "diagnostics_page.diagnostic_label", "Diagnóstico"),
                                    lang_get(self.L, "diagnostics_page.no_missing_tools",
                                             "Nenhuma ferramenta faltando para instalação."))
            return

        if platform.system().lower() != "linux":
            QMessageBox.warning(
                self,
                lang_get(self.L, "diagnostics_page.installation_unavailable", "Instalação indisponível"),
                lang_get(self.L, "diagnostics_page.installation_linux_only",
                         "Instalação automática disponível apenas para Linux com apt."),
            )
            return

        cmd = ["pkexec", "apt-get", "install", "-y", *missing]
        self.result_box.append("\n" + lang_get(self.L, "diagnostics_page.running", "Executando:") + " " + " ".join(cmd))
        try:
            proc = subprocess.run(cmd, capture_output=True, text=True)
            if proc.stdout.strip():
                self.result_box.append("\n" + lang_get(self.L, "diagnostics_page.output_label",
                                                       "--- Saída ---") + "\n" + proc.stdout.strip())

            if proc.returncode == 0:
                self.result_box.append("\n" + lang_get(self.L, "diagnostics_page.installation_completed",
                                                       "✔ Instalação concluída. Execute o diagnóstico novamente."))
            else:
                err = proc.stderr.strip() or lang_get(self.L, "diagnostics_page.unknown_failure", "Falha desconhecida")
                self.result_box.append("\n" + lang_get(self.L, "diagnostics_page.installation_failure",
                                                       "❌ Falha na instalação:") + " " + err)
        except FileNotFoundError:
            self.result_box.append("\n" + lang_get(self.L, "diagnostics_page.pkexec_not_found",
                                                   "❌ 'pkexec' não encontrado. Use manualmente: sudo apt-get install -y"))

    def update_ui_language(self, L):
        """Atualiza a linguagem da página."""
        self.L = L
        self.title_label.setText(lang_get(self.L, "diagnostics_page.title", "Diagnóstico do Ambiente"))
        self.description_label.setText(lang_get(self.L, "diagnostics_page.install_description",
                                                "Verifica se as ferramentas principais já estão instaladas no sistema."))
        self.run_button.setText(lang_get(self.L, "diagnostics_page.run_diagnostic", "Executar diagnóstico"))
        self.install_button.setText(
            lang_get(self.L, "diagnostics_page.install_missing", "Instalar dependências faltantes (Linux/apt)"))


        if not self.last_results:
            self.result_box.setText(lang_get(self.L, "diagnostics_page.description",
                                             "Clique em 'Executar diagnóstico' para verificar o ambiente."))
            
# --- SCANNER ---
class ScannerPage(QWidget):
    def __init__(self, parent_window):
        super().__init__()
        self.parent_window = parent_window
        self.last_results = None
        self.vulnerable_targets = []
        self.executor = None
        self.scan_timer = QTimer()
        self.scan_timer.timeout.connect(self._poll_scan_state)
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)

        self.L = getattr(self.parent_window, 'L', {})

        self.ip_group = QGroupBox(lang_get(self.L, "scanner_page.targets_group", "Alvos de Varredura (IPs/Ranges)"))
        self.ip_group.setObjectName("targets_group")

        ip_layout = QVBoxLayout()

        self.ip_input = QLineEdit()
        self.ip_input.setPlaceholderText(lang_get(self.L, "scanner_page.ip_placeholder", "Ex: 192.168.1.1, 10.0.0.0/24, 172.16.1.1-10"))
        ip_layout.addWidget(self.ip_input)

        self.start_button = QPushButton(lang_get(self.L, "scanner_page.start_scan", "Iniciar Varredura"))
        self.start_button.clicked.connect(self.start_scan)
        ip_layout.addWidget(self.start_button)

        self.ip_group.setLayout(ip_layout)
        layout.addWidget(self.ip_group)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)

        self.result_group = QGroupBox(lang_get(self.L, "scanner_page.results_group", "Resultados"))
        self.result_group.setObjectName("results_group")
        result_layout = QVBoxLayout()

        self.results_text = QLabel(lang_get(self.L, "scanner_page.awaiting_scan", "Aguardando varredura..."))
        self.results_text.setObjectName("ResultsLabel")
        self.results_text.setWordWrap(True)
        self.results_text.setAlignment(
            Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft
        )
        self.results_text.setSizePolicy(
            QSizePolicy.Policy.Preferred,
            QSizePolicy.Policy.MinimumExpanding
        )

        result_layout.addWidget(self.results_text)
        self.result_group.setLayout(result_layout)
        scroll_area.setWidget(self.result_group)
        layout.addWidget(scroll_area)

        self.save_button = QPushButton(lang_get(self.L, "scanner_page.save_results", "Salvar Resultados no Logs/Relatórios"))
        self.save_button.setEnabled(False)
        self.save_button.clicked.connect(self.save_results)
        layout.addWidget(self.save_button)

        self.send_hydra_button = QPushButton(lang_get(self.L, "scanner_page.send_hydra", "Enviar IPs Vulneráveis para Hydra"))
        self.send_hydra_button.setEnabled(False)
        self.send_hydra_button.clicked.connect(self.send_vulnerable_targets_to_hydra)
        layout.addWidget(self.send_hydra_button)

        layout.addStretch()
        self.setLayout(layout)

    def update_ui_language(self, L):
        self.L = L
        self.ip_group.setTitle(lang_get(L, "scanner_page.targets_group", "Alvos de Varredura (IPs/Ranges)"))
        self.ip_input.setPlaceholderText(lang_get(L, "scanner_page.ip_placeholder", "Ex: 192.168.1.1, 10.0.0.0/24, 172.16.1.1-10"))
        self.start_button.setText(lang_get(L, "scanner_page.start_scan", "Iniciar Varredura"))
        self.result_group.setTitle(lang_get(L, "scanner_page.results_group", "Resultados"))
        self.save_button.setText(lang_get(L, "scanner_page.save_results", "Salvar Resultados no Logs/Relatórios"))
        self.send_hydra_button.setText(lang_get(L, "scanner_page.send_hydra", "Enviar IPs Vulneráveis para Hydra"))
        
        if not self.last_results:
            self.results_text.setText(lang_get(L, "scanner_page.awaiting_scan", "Aguardando varredura..."))

    def start_scan(self):
        ip_list = network_scanner.parse_targets(self.ip_input.text())

        if not ip_list:
            self.results_text.setText(lang_get(self.L, "scanner_page.please_enter_target", "Por favor, insira pelo menos um IP ou range."))
            return

        self.start_button.setEnabled(False)
        self.save_button.setEnabled(False)

        self.results_text.setText(
            f"{lang_get(self.L, 'scanner_page.scan_initiated', 'Iniciando varredura em {count} alvo(s)...').format(count=len(ip_list))}<br>"
            f"<i>{lang_get(self.L, 'scanner_page.scan_message', 'Isso pode demorar alguns minutos.')}</i>"
        )
        self.parent_window.status_label.setText(lang_get(self.L, "scanner_page.scanning", "Varrendo rede..."))

        self.executor = network_scanner.NetworkScanExecutor(ip_list)
        self.executor.start()
        self.scan_timer.start(250)

    def update_progress(self, message):
        self.parent_window.status_label.setText(message)

    def _poll_scan_state(self):
        if not self.executor:
            return

        progress_message = self.executor.get_progress_message()
        if progress_message:
            self.update_progress(progress_message)

        if self.executor.is_running:
            return

        self.scan_timer.stop()
        error = self.executor.get_error()
        if error:
            self.scan_error(error)
            return

        self.scan_finished(self.executor.get_results())

    def scan_finished(self, results: list):
        self.last_results = results
        self.vulnerable_targets = []
        self.start_button.setEnabled(True)
        self.save_button.setEnabled(True)

        self.parent_window.status_label.setText(lang_get(self.L, "scanner_page.scan_completed", "Varredura concluída ✔"))

        display_text = f"<b>{lang_get(self.L, 'scanner_page.scan_finished', '✔ Varredura finalizada')}</b><br><br>"

        for host in results:
            if host.get("error"):
                display_text += (
                    f"<b>{lang_get(self.L, 'scanner_page.error_scan', '--- ERRO em {ip} ---').format(ip=host.get('ip', 'N/A'))}</b><br>"
                    f"{host['error']}<br><br>"
                )
                continue

            display_text += f"<b>{lang_get(self.L, 'scanner_page.host_info', '--- IP: {ip} ---').format(ip=host.get('ip', 'N/A'))}</b><br>"

            os_name = host.get("os", lang_get(self.L, "scanner_page.unknown", "Desconhecido"))
            if os_name == "Unknown" or os_name == lang_get(self.L, "scanner_page.unknown", "Desconhecido"):
                display_text += f"<b>{lang_get(self.L, 'scanner_page.os_label', 'SO:')}</b> {lang_get(self.L, 'scanner_page.requires_root', 'Desconhecido (requer privilégios de root)')}<br>"
            else:
                display_text += f"<b>{lang_get(self.L, 'scanner_page.os_label', 'SO:')}</b> {os_name}<br>"

            ports = host.get("open_ports", [])
            if ports:
                display_text += f"<i>{lang_get(self.L, 'scanner_page.open_ports', 'Portas Abertas:')}</i><br>"
                for p in ports:
                    display_text += (
                        f"&nbsp; - <b>{p['port']}/{p['protocol']}</b>: "
                        f"{p['service']}<br>"
                    )
            else:
                display_text += f"{lang_get(self.L, 'scanner_page.no_open_ports', 'Nenhuma porta aberta encontrada.')}<br>"

            vulns = host.get("vulnerabilities", [])
            if vulns:
                self.vulnerable_targets.append(host.get('ip', '').strip())
                display_text += f"<i>{lang_get(self.L, 'scanner_page.potential_vuln', 'Vulnerabilidades Potenciais:')}</i><br>"
                for i, v in enumerate(vulns):
                    if isinstance(v, dict):
                        details = str(v.get("details", ""))
                        port = v.get("port", "?")
                        script = v.get("script", lang_get(self.L, "scanner_page.port_unknown", "desconhecido"))
                        v_short = details.replace("\n", " ").strip()
                        display_text += (
                            f"&nbsp; - <b>{lang_get(self.L, 'scanner_page.vuln_label', 'VULN {i}').format(i=i+1)}</b> "
                            f"({lang_get(self.L, 'scanner_page.port_label', 'Porta')} {port}, {script}): "
                            f"{v_short[:120]}...<br>"
                        )
                    else:
                        v_short = str(v).replace("\n", " ").strip()
                        display_text += (
                            f"&nbsp; - <b>{lang_get(self.L, 'scanner_page.vuln_label', 'VULN {i}').format(i=i+1)}</b>: "
                            f"{v_short[:120]}...<br>"
                        )

            display_text += "<br>"

        self.results_text.setText(display_text)
        self.send_hydra_button.setEnabled(bool(self.vulnerable_targets))

    def scan_error(self, message):
        self.start_button.setEnabled(True)
        self.parent_window.status_label.setText(lang_get(self.L, "scanner_page.error_during_scan", "Erro durante varredura ❌"))
        self.results_text.setText(
            f"{lang_get(self.L, 'scanner_page.unexpected_error', 'Um erro inesperado ocorreu:')}<br><b>{message}</b><br>"
            f"{lang_get(self.L, 'scanner_page.nmap_check', 'Verifique se o Nmap está instalado e se você tem permissões de sudo.')}"
        )
        self.last_results = None
        self.send_hydra_button.setEnabled(False)

    def save_results(self):
        if not self.last_results:
            return

        log_dir = os.path.join(self.parent_window.base_dir, "logs")
        os.makedirs(log_dir, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.join(log_dir, f"scan_report_{timestamp}.json")

        try:
            network_scanner.save_json(self.last_results, filename)

            self.parent_window.status_label.setText(
                lang_get(self.L, "scanner_page.report_saved", "Relatório salvo em logs/{filename} ✔").format(filename=os.path.basename(filename))
            )
            self.save_button.setEnabled(False)

        except Exception as e:
            self.parent_window.status_label.setText(
                f"{lang_get(self.L, 'scanner_page.failed_save', 'Falha ao salvar relatório:')} {type(e).__name__}"
            )
            print("ERRO AO SALVAR RELATÓRIO:", e)

    def send_vulnerable_targets_to_hydra(self):
        targets = [ip for ip in self.vulnerable_targets if ip]
        if not targets:
            QMessageBox.information(self, "Hydra", lang_get(self.L, "scanner_page.no_vulnerable_ips", "Nenhum IP vulnerável disponível para enviar."))
            return
        self.parent_window.open_hydra_with_targets(targets)

# --- SHERLOCK ---
class SherlockPage(QWidget):
    def __init__(self, parent_window):
        super().__init__()
        self.parent_window = parent_window
        self.executor = None
        self.L = getattr(parent_window, 'L', {})
        self.sherlock_timer = QTimer()
        self.sherlock_timer.timeout.connect(self._poll_sherlock_state)
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)

        self.title_label = QLabel(lang_get(self.L, "sherlock_page.title", "🔍 Sherlock OSINT Pro"))
        self.title_label.setFont(QFont("Arial", 22, QFont.Weight.Bold))
        layout.addWidget(self.title_label)

        self.subtitle_label = QLabel(lang_get(self.L, "sherlock_page.subtitle", "Busca avançada por Nickname, Nome Completo e Vazamentos."))
        self.subtitle_label.setStyleSheet(SHERLOCK_STYLES["subtitle"])
        layout.addWidget(self.subtitle_label)

        mode_container = QHBoxLayout()
        self.mode_label = QLabel(lang_get(self.L, "sherlock_page.mode_label", "Tipo de Alvo:"))
        self.mode_label.setStyleSheet(SHERLOCK_STYLES["mode_label"])
        
        self.mode_selector = QComboBox()
        self.mode_selector.addItems([
            lang_get(self.L, "sherlock_page.mode_nickname", "Nickname"),
            lang_get(self.L, "sherlock_page.mode_fullname", "Nome Completo")
        ])
        self.mode_selector.setCursor(Qt.CursorShape.PointingHandCursor)
        self.mode_selector.setStyleSheet(SHERLOCK_STYLES["mode_selector"])
        mode_container.addWidget(self.mode_label)
        mode_container.addWidget(self.mode_selector)
        mode_container.addStretch()
        layout.addLayout(mode_container)

        search_box = QFrame()
        search_box.setStyleSheet(SHERLOCK_STYLES["search_box"])
        search_layout = QHBoxLayout(search_box)

        self.user_input = QLineEdit()
        self.user_input.setPlaceholderText(lang_get(self.L, "sherlock_page.placeholder", "Digite o alvo aqui..."))
        self.user_input.setStyleSheet(SHERLOCK_STYLES["user_input"])
        
        self.btn_investigate = QPushButton(lang_get(self.L, "sherlock_page.investigate", "INVESTIGAR"))
        self.btn_investigate.setCursor(Qt.CursorShape.PointingHandCursor)
        neon = self.parent_window.theme_manager.neon_color
        self.btn_investigate.setStyleSheet(sherlock_investigate_button_style(neon))
        self.btn_investigate.clicked.connect(self.run_sherlock)

        search_layout.addWidget(self.user_input)
        search_layout.addWidget(self.btn_investigate)
        layout.addWidget(search_box)

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setStyleSheet(SHERLOCK_STYLES["scroll"])
        self.results_container = QWidget()
        self.results_layout = QVBoxLayout(self.results_container)
        self.results_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.scroll.setWidget(self.results_container)
        layout.addWidget(self.scroll)

    def run_sherlock(self):
        target = self.user_input.text().strip()
        if not target: return

        mode = "nickname" if self.mode_selector.currentIndex() == 0 else "full_name"

        for i in reversed(range(self.results_layout.count())): 
            widget = self.results_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)

        self.btn_investigate.setEnabled(False)
        self.btn_investigate.setText(lang_get(self.L, "sherlock_page.searching", "BUSCANDO..."))
        
        self.executor = SherlockExecutor(target, mode)
        self.executor.start()
        self.sherlock_timer.start(250)

    def _poll_sherlock_state(self):
        if not self.executor:
            return

        for item in self.executor.pop_new_results():
            self.add_result_card(item["site"], item["url"])

        if self.executor.is_running:
            return

        self.sherlock_timer.stop()
        error = self.executor.get_error()
        if error:
            self.btn_investigate.setEnabled(True)
            self.btn_investigate.setText(lang_get(self.L, "sherlock_page.investigate", "INVESTIGAR"))
            self.parent_window.status_label.setText(lang_get(self.L, "sherlock_page.error_title", "Falha durante investigação Sherlock ❌"))
            QMessageBox.warning(self, lang_get(self.L, "sherlock_page.error_label", "Erro"), lang_get(self.L, "sherlock_page.search_failed", "Falha durante busca:") + f"\n{error}")
            return

        self.finalize_search(self.executor.target, self.executor.get_results())

    def finalize_search(self, username, results):
        self.btn_investigate.setEnabled(True)
        self.btn_investigate.setText(lang_get(self.L, "sherlock_page.investigate", "INVESTIGAR"))
        
        if results:
            path = self.executor.save_results(self.parent_window.base_dir) if self.executor else SherlockEngine().save_to_json(username, results, self.parent_window.base_dir)
            
            filename = os.path.basename(path) if path else "report.json"
            self.parent_window.status_label.setText(lang_get(self.L, "sherlock_page.report_saved", "Relatório salvo: {filename}").format(filename=filename))
            
            msg = QMessageBox(self)
            msg.setWindowTitle(lang_get(self.L, "sherlock_page.search_completed", "Busca Concluída"))
            msg.setIcon(QMessageBox.Icon.Information)
            msg.setText(lang_get(self.L, "sherlock_page.investigation_complete", "A investigação de '{username}' foi concluída!").format(username=username))
            msg.setInformativeText(lang_get(self.L, "sherlock_page.file_generated", "O arquivo foi gerado com sucesso em:") + f"\n\n{path}")
            
            msg.setStyleSheet(SHERLOCK_STYLES["finished_msg_box"])
            msg.exec()
            
        else:
            self.parent_window.status_label.setText(lang_get(self.L, "sherlock_page.no_results", "Nenhum resultado encontrado."))
            QMessageBox.warning(self, lang_get(self.L, "sherlock_page.warning_title", "Aviso"), lang_get(self.L, "sherlock_page.no_networks", "Nenhuma rede social encontrada para este username."))

    def add_result_card(self, site, url):
        card = QFrame()
        
        color_map = {
            "DuckDuckGo": "#ff8c00",
            "OSINT-Search": "#ff8c00",
            "Webmii": "#00ced1",
            "PeekYou": "#00ced1",
            "TruePeople": "#00ced1",
            "📄 Documento": "#ff4444",
            "Potential Leak/Doc": "#ff4444",
            "Gravatar": "#da70d6"
        }
        
        neon = self.parent_window.theme_manager.neon_color
        border_color = color_map.get(site, neon)
        
        card.setStyleSheet(sherlock_result_card_style(border_color))
        
        l = QHBoxLayout(card)
        
        display_url = (url[:65] + '...') if len(url) > 65 else url
        label_text = f"""
            <div style='color: white;'>
                <b style='font-size: 14px;'>{site}</b><br>
                <span style='color: #888; font-size: 12px;'>{display_url}</span>
            </div>
        """
        
        info_label = QLabel(label_text)
        l.addWidget(info_label)
        
        l.addStretch()
        
        btn = QPushButton(lang_get(self.L, "sherlock_page.view_button", "VISUALIZAR"))
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        btn.setFixedWidth(100)
        btn.setStyleSheet(sherlock_result_button_style(border_color))
        btn.clicked.connect(lambda: webbrowser.open(url))
        l.addWidget(btn)
        
        self.results_layout.insertWidget(0, card)

    def update_ui_language(self, L):
        self.L = L
        self.title_label.setText(lang_get(L, "sherlock_page.title", "🔍 Sherlock OSINT Pro"))
        self.subtitle_label.setText(lang_get(L, "sherlock_page.subtitle", "Busca avançada por Nickname, Nome Completo e Vazamentos."))
        self.mode_label.setText(lang_get(L, "sherlock_page.mode_label", "Tipo de Alvo:"))
        self.mode_selector.setItemText(0, lang_get(L, "sherlock_page.mode_nickname", "Nickname"))
        self.mode_selector.setItemText(1, lang_get(L, "sherlock_page.mode_fullname", "Nome Completo"))
        self.user_input.setPlaceholderText(lang_get(L, "sherlock_page.placeholder", "Digite o alvo aqui..."))
        self.btn_investigate.setText(lang_get(L, "sherlock_page.investigate", "INVESTIGAR"))

# --- Hydra ---
class HydraPage(QWidget):
    def __init__(self, parent_window):
        super().__init__()
        self.parent_window = parent_window
        self.user_list_path = ""
        self.pass_list_path = ""
        self.executor = None
        self.hydra_timer = QTimer()
        self.hydra_timer.timeout.connect(self._poll_hydra_state)

        scroll = QScrollArea(self)
        scroll.setWidgetResizable(True)

        container = QWidget()
        self.main_layout = QVBoxLayout(container)

        scroll.setWidget(container)

        outer_layout = QVBoxLayout(self)
        outer_layout.addWidget(scroll)

        self._setup_ui()

    def _setup_ui(self):
        layout = self.main_layout
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(15)

        self.L = getattr(self.parent_window, 'L', {})

        self.title_label = QLabel(lang_get(self.L, "hydra_page.title", "🧰 Hydra - Teste de Credenciais"))
        self.title_label.setFont(QFont("Arial", 22, QFont.Weight.Bold))
        layout.addWidget(self.title_label)

        self.warning_label = QLabel(lang_get(self.L, "hydra_page.warning", "⚠️ Use somente em ambientes autorizados."))
        self.warning_label.setStyleSheet(HYDRA_STYLES["warning"])
        layout.addWidget(self.warning_label)

        self.targets_group = QGroupBox(lang_get(self.L, "hydra_page.targets_group", "Alvos"))
        targets_layout = QVBoxLayout()
        self.targets_input = QTextEdit()
        self.targets_input.setPlaceholderText(lang_get(self.L, "hydra_page.targets_placeholder", "Ex: 192.168.0.10\n192.168.0.20"))
        self.targets_input.setFixedHeight(80)
        targets_layout.addWidget(self.targets_input)
        self.targets_group.setLayout(targets_layout)
        layout.addWidget(self.targets_group)

        self.service_group = QGroupBox(lang_get(self.L, "hydra_page.service_and_port", "Serviço e Porta"))
        service_layout = QHBoxLayout()

        self.service_combo = QComboBox()
        self.service_combo.setEditable(True)
        self.service_combo.addItems([
            "ssh", "ftp", "telnet", "smb", "rdp",
            "http-get", "http-post-form",
            "mysql", "postgres", "vnc"
        ])
        self.service_combo.currentTextChanged.connect(self._on_service_changed)

        self.port_input = QSpinBox()
        self.port_input.setRange(0, 65535)
        self.port_input.setValue(0)

        self.service_label = QLabel(lang_get(self.L, "hydra_page.service_label", "Serviço:"))
        self.port_label = QLabel(lang_get(self.L, "hydra_page.port_label", "Porta:"))
        service_layout.addWidget(self.service_label)
        service_layout.addWidget(self.service_combo, 2)
        service_layout.addWidget(self.port_label)
        service_layout.addWidget(self.port_input, 1)

        self.service_group.setLayout(service_layout)
        layout.addWidget(self.service_group)

        self.http_group = QGroupBox(lang_get(self.L, "hydra_page.http_config", "Configuração HTTP POST"))
        self.http_group.setVisible(False)

        http_layout = QVBoxLayout()

        self.http_path = QLineEdit()
        self.http_path.setPlaceholderText(lang_get(self.L, "hydra_page.form_path_placeholder", "/login.php"))

        self.http_params = QLineEdit()
        self.http_params.setPlaceholderText(lang_get(self.L, "hydra_page.post_params_placeholder", "username=^USER^&password=^PASS^"))

        self.http_fail = QLineEdit()
        self.http_fail.setPlaceholderText(lang_get(self.L, "hydra_page.fail_string_placeholder", "Texto de falha (ex: Invalid login)"))

        self.http_form_path_label = QLabel(lang_get(self.L, "hydra_page.form_path", "Caminho do formulário"))
        self.http_post_params_label = QLabel(lang_get(self.L, "hydra_page.post_params", "Parâmetros POST"))
        self.http_fail_string_label = QLabel(lang_get(self.L, "hydra_page.fail_string", "String de falha"))
        http_layout.addWidget(self.http_form_path_label)
        http_layout.addWidget(self.http_path)
        http_layout.addWidget(self.http_post_params_label)
        http_layout.addWidget(self.http_params)
        http_layout.addWidget(self.http_fail_string_label)
        http_layout.addWidget(self.http_fail)

        self.http_group.setLayout(http_layout)
        layout.addWidget(self.http_group)

        self.creds_group = QGroupBox(lang_get(self.L, "hydra_page.credentials_group", "Credenciais"))
        creds_layout = QVBoxLayout()

        user_row = QHBoxLayout()
        self.user_input = QLineEdit()
        self.user_input.setPlaceholderText(lang_get(self.L, "hydra_page.single_username", "Usuário único"))
        self.user_list_button = QPushButton(lang_get(self.L, "hydra_page.username_list", "Lista de Usuários"))
        self.user_list_button.clicked.connect(self.select_user_list)
        user_row.addWidget(self.user_input, 2)
        user_row.addWidget(self.user_list_button, 1)

        pass_row = QHBoxLayout()
        self.pass_input = QLineEdit()
        self.pass_input.setPlaceholderText(lang_get(self.L, "hydra_page.single_password", "Senha única"))
        self.pass_list_button = QPushButton(lang_get(self.L, "hydra_page.password_list", "Lista de Senhas"))
        self.pass_list_button.clicked.connect(self.select_pass_list)
        pass_row.addWidget(self.pass_input, 2)
        pass_row.addWidget(self.pass_list_button, 1)

        creds_layout.addLayout(user_row)
        creds_layout.addLayout(pass_row)
        self.creds_group.setLayout(creds_layout)
        layout.addWidget(self.creds_group)

        self.options_group = QGroupBox(lang_get(self.L, "hydra_page.options_group", "Opções"))
        options_layout = QHBoxLayout()

        self.tasks_input = QSpinBox()
        self.tasks_input.setRange(1, 64)
        self.tasks_input.setValue(4)

        self.stop_on_success = QCheckBox(lang_get(self.L, "hydra_page.stop_on_success", "Parar ao encontrar credencial"))
        self.verbose_check = QCheckBox(lang_get(self.L, "hydra_page.verbose", "Verbose"))

        self.threads_label = QLabel(lang_get(self.L, "hydra_page.threads_label", "Threads (-t):"))
        options_layout.addWidget(self.threads_label)
        options_layout.addWidget(self.tasks_input)
        options_layout.addWidget(self.stop_on_success)
        options_layout.addWidget(self.verbose_check)

        self.options_group.setLayout(options_layout)
        layout.addWidget(self.options_group)

        button_row = QHBoxLayout()

        self.start_button = QPushButton(lang_get(self.L, "hydra_page.start_button", "INICIAR"))
        self.start_button.clicked.connect(self.start_hydra)

        self.stop_button = QPushButton(lang_get(self.L, "hydra_page.stop_button", "PARAR"))
        self.stop_button.setEnabled(False)
        self.stop_button.clicked.connect(self.stop_hydra)

        button_row.addWidget(self.start_button)
        button_row.addWidget(self.stop_button)
        layout.addLayout(button_row)

        self.console = QTextEdit()
        self.console.setReadOnly(True)
        self.console.setStyleSheet(HYDRA_STYLES["console"])
        layout.addWidget(self.console)

    def _on_service_changed(self, service):
        self.http_group.setVisible(service.strip() == "http-post-form")

    def select_user_list(self):
        file, _ = QFileDialog.getOpenFileName(self, lang_get(self.L, "hydra_page.user_list_title", "Lista de Usuários"), "", "*.txt")
        if file:
            self.user_list_path = file
            self.user_list_button.setText(os.path.basename(file))

    def select_pass_list(self):
        file, _ = QFileDialog.getOpenFileName(self, lang_get(self.L, "hydra_page.password_list_title", "Lista de Senhas"), "", "*.txt")
        if file:
            self.pass_list_path = file
            self.pass_list_button.setText(os.path.basename(file))

    def start_hydra(self):
        if self.executor and self.executor.is_running:
            QMessageBox.information(self, lang_get(self.L, "hydra_page.already_running", "Hydra"), lang_get(self.L, "hydra_page.already_running_msg", "Já existe uma execução em andamento."))
            return

        targets = HydraExecutor.parse_targets(self.targets_input.toPlainText())
        if not targets:
            QMessageBox.warning(self, lang_get(self.L, "hydra_page.no_targets", "Hydra"), lang_get(self.L, "hydra_page.no_targets_msg", "Informe ao menos um alvo."))
            return

        service = self.service_combo.currentText().strip()
        if not service:
            QMessageBox.warning(self, lang_get(self.L, "hydra_page.no_service", "Hydra"), lang_get(self.L, "hydra_page.no_service_msg", "Informe o serviço."))
            return

        if service == "http-post-form":
            if not all([
                self.http_path.text().strip(),
                self.http_params.text().strip(),
                self.http_fail.text().strip()
            ]):
                QMessageBox.warning(self, lang_get(self.L, "hydra_page.http_required", "Hydra"), lang_get(self.L, "hydra_page.http_required_msg", "Preencha todos os campos do HTTP POST."))
                return
            if "^USER^" not in self.http_params.text() and "^PASS^" not in self.http_params.text():
                QMessageBox.warning(self, lang_get(self.L, "hydra_page.params_error", "Hydra"), lang_get(self.L, "hydra_page.params_error_msg", "Use ^USER^ e ^PASS^ nos parâmetros."))
                return

        self.console.clear()
        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)

        self.executor = HydraExecutor(
            targets=targets,
            service=service,
            username=self.user_input.text().strip(),
            password=self.pass_input.text().strip(),
            user_list=self.user_list_path,
            pass_list=self.pass_list_path,
            port=self.port_input.value(),
            tasks=self.tasks_input.value(),
            stop_on_success=self.stop_on_success.isChecked(),
            verbose=self.verbose_check.isChecked(),
            http_path=self.http_path.text().strip(),
            http_params=self.http_params.text().strip(),
            http_fail=self.http_fail.text().strip(),
        )
        self.executor.start()
        self.hydra_timer.start(250)

    def stop_hydra(self):
        if self.executor and self.executor.is_running:
            self.executor.stop()
            self.console.append(lang_get(self.L, "hydra_page.interruption_requested", "[INFO] Interrupção solicitada."))
        self.stop_button.setEnabled(False)

    def _poll_hydra_state(self):
        if not self.executor:
            return

        for line in self.executor.pop_new_output():
            self.console.append(line)

        if self.executor.is_running:
            return

        self.hydra_timer.stop()
        if self.executor.error:
            self.console.append(f"[ERROR] {self.executor.error}")
        self.finish_hydra(self.executor.return_code if self.executor.return_code is not None else 1)

    def finish_hydra(self, code):
        success = (code == 0)

        self.console.append(f"{lang_get(self.L, 'hydra_page.completed', '[INFO] Hydra finalizado com código')} {code}.")

        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        if self.executor:
            filepath = self.executor.save_log(self.parent_window.base_dir)
            self.console.append(f"{lang_get(self.L, 'hydra_page.log_saved', '[INFO] Log salvo em')} {filepath}")
        self.executor = None

    def set_targets(self, targets):
        """Define os alvos a partir de uma lista."""
        if targets:
            self.targets_input.setPlainText("\n".join(targets))

    def update_ui_language(self, L):
        """Atualiza a linguagem da página."""
        self.L = L
        self.title_label.setText(lang_get(L, "hydra_page.title", "🧰 Hydra - Teste de Credenciais"))
        self.warning_label.setText(lang_get(L, "hydra_page.warning", "⚠️ Use somente em ambientes autorizados."))
        self.targets_group.setTitle(lang_get(L, "hydra_page.targets_group", "Alvos"))
        self.service_group.setTitle(lang_get(L, "hydra_page.service_and_port", "Serviço e Porta"))
        self.service_label.setText(lang_get(L, "hydra_page.service_label", "Serviço:"))
        self.port_label.setText(lang_get(L, "hydra_page.port_label", "Porta:"))
        self.http_group.setTitle(lang_get(L, "hydra_page.http_config", "Configuração HTTP POST"))
        self.http_form_path_label.setText(lang_get(L, "hydra_page.form_path", "Caminho do formulário"))
        self.http_post_params_label.setText(lang_get(L, "hydra_page.post_params", "Parâmetros POST"))
        self.http_fail_string_label.setText(lang_get(L, "hydra_page.fail_string", "String de falha"))
        self.creds_group.setTitle(lang_get(L, "hydra_page.credentials_group", "Credenciais"))
        self.user_input.setPlaceholderText(lang_get(L, "hydra_page.single_username", "Usuário único"))
        self.user_list_button.setText(lang_get(L, "hydra_page.username_list", "Lista de Usuários"))
        self.pass_input.setPlaceholderText(lang_get(L, "hydra_page.single_password", "Senha única"))
        self.pass_list_button.setText(lang_get(L, "hydra_page.password_list", "Lista de Senhas"))
        self.options_group.setTitle(lang_get(L, "hydra_page.options_group", "Opções"))
        self.threads_label.setText(lang_get(L, "hydra_page.threads_label", "Threads (-t):"))
        self.stop_on_success.setText(lang_get(L, "hydra_page.stop_on_success", "Parar ao encontrar credencial"))
        self.start_button.setText(lang_get(L, "hydra_page.start_button", "INICIAR"))
        self.stop_button.setText(lang_get(L, "hydra_page.stop_button", "PARAR"))
        
# --- CLASSE DA PAGINA DE MANUAL ---
class ManualScannerPage(QWidget):
    def __init__(self, main_window):
        print("[DEBUG] refresh_manual_content chamado")
        super().__init__()
        self.main_window = main_window
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)

        self.tabs = QTabWidget()
        self.tabs.setObjectName("ManualTabs")
        self.refresh_manual_content()
        print("[DEBUG] ManualScannerPage criada")

        layout.addWidget(self.tabs)
    
    def refresh_manual_content(self):
        self.tabs.clear()

        L = self.main_window.L

        fallback_L = load_language_json("pt", self.main_window.base_dir)

        sections = [
            "manifesto",
            "scanner",
            "ddos",
            "auditoria",
            "sherlock",
            "john",
            "keylogger",
            "hydra",
        ]

        print("[DEBUG] Idioma atual:", self.main_window.current_lang_code)
        print("[DEBUG] Manual keys:", list(self.main_window.L.get("manual", {}).keys()))

        for key in sections:
            section = L.get("manual", {}).get(key)

            if not section:
                section = fallback_L.get("manual", {}).get(key, {})

            title = section.get("title", key.upper())
            content = section.get("content", "Conteúdo não disponível.")

            self.tabs.addTab(
                self._create_scrollable_tab(content),
                title
            )

    def _create_scrollable_tab(self, markdown_text):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        label = QLabel(markdown_text)
        label.setWordWrap(True)
        label.setTextFormat(Qt.TextFormat.MarkdownText)
        label.setStyleSheet(MANUAL_STYLES["tab_label"])
        label.setAlignment(Qt.AlignmentFlag.AlignTop)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(label)
        scroll.setStyleSheet(MANUAL_STYLES["tab_scroll"])
        
        layout.addWidget(scroll)
        return widget

# --- AUDITORIA DE SEGURANÇA ---
class FirewallPage(QWidget):
    def __init__(self, parent_window):
        super().__init__()
        self.parent_window = parent_window
        self.L = getattr(parent_window, 'L', {})
        self.executor = None
        self.audit_timer = QTimer()
        self.audit_timer.timeout.connect(self._poll_audit_state)
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        self.title_label = QLabel(lang_get(self.L, "firewall_page.audit_title", "🛡️ Auditoria de Segurança"))
        self.title_label.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        layout.addWidget(self.title_label)

        self.description_label = QLabel(lang_get(self.L, "firewall_page.description", "Este teste realiza uma auditoria profunda no host local, verificando permissões críticas, processos suspeitos, integridade de arquivos e conformidade do firewall."))
        self.description_label.setWordWrap(True)
        self.description_label.setStyleSheet(firewall_description_style("dark"))
        layout.addWidget(self.description_label)

        self.action_group = QGroupBox(lang_get(self.L, "firewall_page.execution_test", "Execução do Teste"))
        action_layout = QVBoxLayout()

        self.btn_local = QPushButton(lang_get(self.L, "firewall_page.start_audit", "Iniciar Auditoria Local"))
        self.btn_local.setFixedHeight(45)
        self.btn_local.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_local.clicked.connect(self.run_local_test)

        action_layout.addWidget(self.btn_local)
        self.action_group.setLayout(action_layout)
        layout.addWidget(self.action_group)

        self.log_output = QLabel(lang_get(self.L, "firewall_page.waiting", "Aguardando comando..."))
        self.log_output.setStyleSheet(FIREWALL_STYLES["log_output"])
        self.log_output.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.log_output.setWordWrap(True)
        layout.addWidget(self.log_output)

        layout.addStretch()
        self.setLayout(layout)

    def run_local_test(self):
        if self.executor and self.executor.is_running:
            QMessageBox.information(self, lang_get(self.L, "firewall_page.audit_label", "Auditoria"), lang_get(self.L, "firewall_page.audit_running", "A auditoria já está em andamento."))
            return

        self.btn_local.setEnabled(False)
        self.btn_local.setText(lang_get(self.L, "firewall_page.audit_in_progress", "Auditoria em Andamento..."))
        self.log_output.setText(f"<b>{lang_get(self.L, 'firewall_page.metadata_collection', '[INFO] Iniciando coleta de metadados e análise de processos...')}</b>")
        self.parent_window.status_label.setText(lang_get(self.L, "firewall_page.running_audit", "Executando Auditoria de Segurança..."))

        self.executor = InteractionTestExecutor(self.parent_window.base_dir)
        self.executor.start()
        self.audit_timer.start(250)

    def _poll_audit_state(self):
        if not self.executor:
            return

        if self.executor.is_running:
            return

        self.audit_timer.stop()
        if self.executor.error:
            self._update_ui_error(self.executor.error)
            self.executor = None
            return

        self._update_ui(self.executor.results or [], self.executor.meta or {}, self.executor.log_path)
        self.executor = None

    def _update_ui_error(self, msg):
        self.btn_local.setEnabled(True)
        self.btn_local.setText(lang_get(self.L, "firewall_page.start_audit", "Iniciar Auditoria Local"))
        self.log_output.setText(f"<span style='color:red;'><b>{lang_get(self.L, 'firewall_page.error_label', 'ERRO')}</b>: {msg}</span>")

    def _update_ui(self, results, meta, log_path):
        self.btn_local.setEnabled(True)
        self.btn_local.setText(lang_get(self.L, "firewall_page.start_audit", "Iniciar Auditoria Local"))
        self.update_log_view(log_path)

        res_str = "\n".join(results)
        QMessageBox.information(
            self,
            lang_get(self.L, "firewall_page.report_generated", "Relatório Gerado"),
            f"{lang_get(self.L, 'firewall_page.audit_completed', 'Auditoria concluída na estação: {hostname}').format(hostname=meta.get('hostname', lang_get(self.L, 'firewall_page.unknown', 'Desconhecido')))}\n"
            f"{lang_get(self.L, 'firewall_page.audit_user', 'Usuário: {user}').format(user=meta.get('user', lang_get(self.L, 'firewall_page.unknown', 'Desconhecido')))}\n\n"
            f"{lang_get(self.L, 'firewall_page.summary', 'Resumo dos achados:')}\n{res_str}"
        )

    def update_log_view(self, path):
        try:
            if os.path.exists(path):
                with open(path, "r", encoding="utf-8") as f:
                    content = f.read()
                    self.log_output.setText(f"<pre style='color:#00ff00;'>{content[-1200:]}</pre>")
            else:
                self.log_output.setText(f"<b>{lang_get(self.L, 'firewall_page.report_saved', '[INFO] Relatório assinado e salvo com sucesso.')}</b>")
        except Exception as e:
            self.log_output.setText(f"<b>{lang_get(self.L, 'firewall_page.error_reading', '[ERRO] ao ler log:')}</b> {e}")

    def update_ui_language(self, L):
        self.L = L
        self.title_label.setText(lang_get(L, "firewall_page.audit_title", "🛡️ Auditoria de Segurança"))
        self.description_label.setText(lang_get(L, "firewall_page.description", "Este teste realiza uma auditoria profunda no host local, verificando permissões críticas, processos suspeitos, integridade de arquivos e conformidade do firewall."))
        self.action_group.setTitle(lang_get(L, "firewall_page.execution_test", "Execução do Teste"))
        self.btn_local.setText(lang_get(L, "firewall_page.start_audit", "Iniciar Auditoria Local"))
        self.log_output.setText(lang_get(L, "firewall_page.waiting", "Aguardando comando..."))
    
# --- CLASSE PRINCIPAL (MainWindow) ---
class MainWindow(QMainWindow):
    PAGE_HOME = 0
    PAGE_TOOLS = 1
    PAGE_MANUAL_SCANNER = 2
    PAGE_SCANNER = 3
    PAGE_SCRIPTS = 4
    PAGE_LOGS = 5
    PAGE_CONFIG = 6
    PAGE_FIREWALL = 7
    PAGE_PAYLOAD = 8
    PAGE_LISTENER = 9
    PAGE_STRESS = 10
    PAGE_OSINT = 11
    PAGE_JOHN = 12
    PAGE_KEYLOGGER = 13
    PAGE_HYDRA = 14

    def safe_change_page(self, index):
        if 0 <= index < self.pages.count():
            self.pages.setCurrentIndex(index)
            self.status_label.setText(lang_get(self.L, "header.status_page_loaded", "Status: Página {index} carregada").format(index=index))

    def open_hydra_with_targets(self, targets):
        self.hydra_page.set_targets(targets)
        self.safe_change_page(self.PAGE_HYDRA)

    def __init__(self, base_dir):
        super().__init__()
        self.base_dir = base_dir

        self.user_settings = load_user_settings(self.base_dir)
        self.theme_manager = ThemeManager(self.user_settings)
        self.current_lang_code = self.user_settings.get('language', 'pt')
        self.L = load_language_json(self.current_lang_code, self.base_dir)

        self.setWindowTitle(lang_get(self.L, "app.window_title", "AURA Security Toolkit"))
        self.setGeometry(100, 100, 1200, 800)

        self._build_ui()
        self._apply_theme(self.theme_manager.current_theme)
        self.update_ui_language(self.L)

        self.show()
        QApplication.processEvents()
        self._refresh_neon_fix()

    def _refresh_neon_fix(self):
        neon_color = self.theme_manager.neon_color
        for card in self.findChildren(NeonCard):
            card.set_neon_color(neon_color, self.theme_manager.current_theme)
            card.update()

    def _build_placeholder_page(self, text):
        page = QWidget()
        layout = QVBoxLayout(page)
        label = QLabel(text)
        label.setWordWrap(True)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setObjectName("PlaceholderLabel")
        layout.addStretch()
        layout.addWidget(label)
        layout.addStretch()
        return page

    def _build_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        self.sidebar = QFrame()
        self.sidebar.setFixedWidth(200)
        self.sidebar.setObjectName("Sidebar")
        sidebar_layout = QVBoxLayout(self.sidebar)
        sidebar_layout.setContentsMargins(10, 20, 10, 10)
        sidebar_layout.setSpacing(10)

        self.title_label = QLabel("AURA")
        self.title_label.setFont(QFont("Arial", 24, QFont.Weight.Bold))
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_label.setObjectName("AuraTitle")
        sidebar_layout.addWidget(self.title_label)

        self.btn_home = self._make_sidebar_button(lang_get(self.L, "sidebar.home", "Início"), "🏠")
        self.btn_tools = self._make_sidebar_button(lang_get(self.L, "sidebar.diagnostic", "Diagnóstico"), "🧪")
        self.btn_scanner = self._make_sidebar_button(lang_get(self.L, "sidebar.scanner", "Informações"), "🛰️")
        self.btn_scripts = self._make_sidebar_button(lang_get(self.L, "sidebar.scripts", "Scripts"), "📜")
        self.btn_logs = self._make_sidebar_button(lang_get(self.L, "sidebar.logs", "Logs"), "📁")
        self.btn_config = self._make_sidebar_button(lang_get(self.L, "sidebar.settings", "Configurações"), "⚙️")

        self.sidebar_buttons = [self.btn_home, self.btn_tools, self.btn_scanner, self.btn_scripts, self.btn_logs, self.btn_config]
        for btn in self.sidebar_buttons:
            sidebar_layout.addWidget(btn)

        sidebar_layout.addItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))
        self.status_label = QLabel(lang_get(self.L, "header.status_ready", "Status: Pronto"))
        sidebar_layout.addWidget(self.status_label)
        main_layout.addWidget(self.sidebar)

        self.content_frame = QFrame()
        self.content_frame.setObjectName("ContentFrame")
        content_v_layout = QVBoxLayout(self.content_frame)
        content_v_layout.setContentsMargins(0, 0, 0, 0)

        self.pages = QStackedWidget()

        home_page = QWidget()
        home_layout = QVBoxLayout(home_page)
        self.welcome_label = QLabel(lang_get(self.L, "home_page.welcome", "Bem-vindo ao AURA Security Toolkit!"))
        self.welcome_label.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        home_layout.addWidget(self.welcome_label)

        card_grid = QGridLayout()
        self.card_scanner = NeonCard("🛰️", lang_get(self.L, "home_page.cards.scanner.title", "Varredura"), lang_get(self.L, "home_page.cards.scanner.subtitle", "Identifica hosts."), self.theme_manager.neon_color, self.theme_manager)
        self.card_scanner.on_card_activated = lambda: self.safe_change_page(self.PAGE_SCANNER) 

        self.card_stress = NeonCard("🔥", lang_get(self.L, "home_page.cards.stress.title", "Stress Test"), lang_get(self.L, "home_page.cards.stress.subtitle", "Simulação DoS."), self.theme_manager.neon_color, self.theme_manager)
        self.card_stress.on_card_activated = lambda: self.safe_change_page(self.PAGE_STRESS)

        self.card_firewall = NeonCard("🛡️", lang_get(self.L, "home_page.cards.firewall.title", "Firewall"), lang_get(self.L, "home_page.cards.firewall.subtitle", "Verifica regras."), self.theme_manager.neon_color, self.theme_manager)
        self.card_firewall.on_card_activated = lambda: self.safe_change_page(self.PAGE_FIREWALL)

        self.card_osint = NeonCard("🔍", lang_get(self.L, "home_page.cards.sherlock.title", "Sherlock"), lang_get(self.L, "home_page.cards.sherlock.subtitle", "OSINT Social."), self.theme_manager.neon_color, self.theme_manager)
        self.card_osint.on_card_activated = lambda: self.safe_change_page(self.PAGE_OSINT)

        self.card_john = NeonCard("💀", lang_get(self.L, "home_page.cards.john.title", "John Ripper"), lang_get(self.L, "home_page.cards.john.subtitle", "Quebra hashes."), self.theme_manager.neon_color, self.theme_manager)
        self.card_john.on_card_activated = lambda: self.safe_change_page(self.PAGE_JOHN)

        self.card_keylogger = NeonCard("⌨️", lang_get(self.L, "home_page.cards.keylogger.title", "Key Auditor"), lang_get(self.L, "home_page.cards.keylogger.subtitle", "Log de teclado."), self.theme_manager.neon_color, self.theme_manager)
        self.card_keylogger.on_card_activated = lambda: self.safe_change_page(self.PAGE_KEYLOGGER)

        self.card_hydra = NeonCard("🧰", lang_get(self.L, "home_page.cards.hydra.title", "Hydra"), lang_get(self.L, "home_page.cards.hydra.subtitle", "Teste credenciais."), self.theme_manager.neon_color, self.theme_manager)
        self.card_hydra.on_card_activated = lambda: self.safe_change_page(self.PAGE_HYDRA)

        card_grid.addWidget(self.card_scanner, 0, 0); card_grid.addWidget(self.card_stress, 0, 1); card_grid.addWidget(self.card_firewall, 0, 2)
        card_grid.addWidget(self.card_osint, 1, 0); card_grid.addWidget(self.card_john, 1, 1); card_grid.addWidget(self.card_keylogger, 1, 2)
        card_grid.addWidget(self.card_hydra, 2, 0)
        home_layout.addLayout(card_grid)
        home_layout.addStretch()
        self.pages.addWidget(home_page)

        self.diagnostics_page = EnvironmentDiagnosticsPage(self)
        self.pages.addWidget(self.diagnostics_page)

        self.manual_scanner_page = ManualScannerPage(self)
        self.pages.addWidget(self.manual_scanner_page)

        self.scanner_page = ScannerPage(self)
        self.pages.addWidget(self.scanner_page)

        self.scripts_placeholder_page = self._build_placeholder_page(lang_get(self.L, "placeholder_pages.scripts", "Página de scripts em consolidação."))
        self.pages.addWidget(self.scripts_placeholder_page)

        self.logs_placeholder_page = self._build_placeholder_page(lang_get(self.L, "placeholder_pages.logs", "Página de logs em consolidação."))
        self.pages.addWidget(self.logs_placeholder_page)

        self.config_page = ConfigPage(self)
        self.pages.addWidget(self.config_page)

        self.firewall_page = FirewallPage(self)
        self.pages.addWidget(self.firewall_page)

        self.payload_page = PayloadPage(self)
        self.pages.addWidget(self.payload_page)

        self.listener_page = ListenerPage(self)
        self.pages.addWidget(self.listener_page)

        self.stress_page = StressTestPage(self)
        self.pages.addWidget(self.stress_page)

        self.osint_page = SherlockPage(self)
        self.pages.addWidget(self.osint_page)

        self.john_page = JohnPage(self)
        self.pages.addWidget(self.john_page)

        self.key_auditor_page = KeyloggerPage(self)
        self.pages.addWidget(self.key_auditor_page)

        self.hydra_page = HydraPage(self)
        self.pages.addWidget(self.hydra_page)

        content_v_layout.addWidget(self.pages)
        main_layout.addWidget(self.content_frame)

        self.btn_home.clicked.connect(lambda: self.safe_change_page(self.PAGE_HOME))
        self.btn_tools.clicked.connect(lambda: self.safe_change_page(self.PAGE_TOOLS))
        self.btn_scanner.clicked.connect(lambda: self.safe_change_page(self.PAGE_MANUAL_SCANNER))
        self.btn_scripts.clicked.connect(lambda: self.safe_change_page(self.PAGE_SCRIPTS))
        self.btn_logs.clicked.connect(lambda: self.safe_change_page(self.PAGE_LOGS))
        self.btn_config.clicked.connect(lambda: self.safe_change_page(self.PAGE_CONFIG))

    def _make_sidebar_button(self, text, icon):
        btn = QPushButton(f"  {icon} {text}")
        btn.setObjectName("SidebarButton")
        btn.setFixedHeight(45)
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        return btn

    def get_theme_colors(self, theme_key=None):
        return THEMES.get(theme_key or self.theme_manager.current_theme, THEMES['dark'])

    def _apply_theme(self, theme_key):
        T = self.get_theme_colors(theme_key)
        neon_color = self.theme_manager.neon_color
        self.setStyleSheet(main_window_stylesheet(T, neon_color))

        for card in self.findChildren(NeonCard):
            card.set_neon_color(neon_color, self.theme_manager.current_theme)

    def apply_base_theme(self, theme_name):
        self.theme_manager.set_base_theme(theme_name)
        self._apply_theme(theme_name)
        self.user_settings['theme'] = theme_name
        save_user_settings(self.base_dir, self.user_settings)

    def set_global_neon_color(self, color):
        self.theme_manager.set_neon_color(color)
        self._apply_theme(self.theme_manager.current_theme)
        self.user_settings['neon_color'] = color
        save_user_settings(self.base_dir, self.user_settings)

    def apply_language(self, lang_name):
        lang_map = {
            "Português": "pt",
            "Inglês": "en",
            "Espanhol": "es",
            "Francês": "fr",
            "Alemão": "de",
            "Italiano": "it",
            "Russo": "ru",
            "Chinês": "zh",
            "Coreano": "ko",
            "Japonês": "ja",
            "Árabe": "ar",
        }

        lang_code = lang_map.get(lang_name, "pt")

        self.L = load_language_json(lang_code, self.base_dir)
        self.current_lang_code = lang_code
        self.update_ui_language(self.L)

        self.user_settings['language'] = lang_code
        save_user_settings(self.base_dir, self.user_settings)

        if hasattr(self, "manual_scanner_page"):
            self.manual_scanner_page.refresh_manual_content()

        QTimer.singleShot(50, self._refresh_neon_fix)

    def update_ui_language(self, L):
        self.btn_home.setText("  🏠 " + lang_get(L, "sidebar.home", "Início"))
        self.btn_tools.setText("  🧪 " + lang_get(L, "sidebar.tools", "Ferramentas"))
        self.btn_scanner.setText("  📜 " + lang_get(L, "sidebar.scanner", "Informações"))
        self.btn_scripts.setText("  📜 " + lang_get(L, "sidebar.scripts", "Scripts"))
        self.btn_logs.setText("  📁 " + lang_get(L, "sidebar.logs", "Logs"))
        self.btn_config.setText("  ⚙️ " + lang_get(L, "sidebar.settings", "Configurações"))
        self.status_label.setText(lang_get(L, "header.status_ready", "Status: Pronto"))

        scripts_label = self.scripts_placeholder_page.findChild(QLabel)
        if scripts_label:
            scripts_label.setText(lang_get(L, "placeholder_pages.scripts", "Página de scripts em consolidação."))
        
        logs_label = self.logs_placeholder_page.findChild(QLabel)
        if logs_label:
            logs_label.setText(lang_get(L, "placeholder_pages.logs", "Página de logs em consolidação."))

        self.config_page.update_ui_language(L)
        self.scanner_page.update_ui_language(L)
        self.diagnostics_page.update_ui_language(L)
        self.stress_page.update_ui_language(L)
        self.osint_page.update_ui_language(L)
        self.john_page.update_ui_language(L)
        self.key_auditor_page.update_ui_language(L)
        self.firewall_page.update_ui_language(L)
        self.hydra_page.update_ui_language(L)

        if hasattr(self.manual_scanner_page, "refresh_manual_content"):
            self.manual_scanner_page.main_window = self
            self.manual_scanner_page.refresh_manual_content()

        self.welcome_label.setText(
            lang_get(L, "home_page.welcome", "Bem-vindo ao AURA Security Toolkit!")
        )

        self.card_scanner.title_label.setText(lang_get(L, "home_page.cards.scanner.title", "Varredura"))
        self.card_scanner.subtitle_label.setText(lang_get(L, "home_page.cards.scanner.subtitle", "Identifica hosts."))
        self.card_stress.title_label.setText(lang_get(L, "home_page.cards.stress.title", "Stress Test"))
        self.card_stress.subtitle_label.setText(lang_get(L, "home_page.cards.stress.subtitle", "Simulação DoS."))
        self.card_firewall.title_label.setText(lang_get(L, "home_page.cards.firewall.title", "Firewall"))
        self.card_firewall.subtitle_label.setText(lang_get(L, "home_page.cards.firewall.subtitle", "Verifica regras."))
        self.card_osint.title_label.setText(lang_get(L, "home_page.cards.sherlock.title", "Sherlock"))
        self.card_osint.subtitle_label.setText(lang_get(L, "home_page.cards.sherlock.subtitle", "OSINT Social."))
        self.card_john.title_label.setText(lang_get(L, "home_page.cards.john.title", "John Ripper"))
        self.card_john.subtitle_label.setText(lang_get(L, "home_page.cards.john.subtitle", "Quebra hashes."))
        self.card_keylogger.title_label.setText(lang_get(L, "home_page.cards.keylogger.title", "Key Auditor"))
        self.card_keylogger.subtitle_label.setText(lang_get(L, "home_page.cards.keylogger.subtitle", "Log de teclado."))
        self.card_hydra.title_label.setText(lang_get(L, "home_page.cards.hydra.title", "Hydra"))
        self.card_hydra.subtitle_label.setText(lang_get(L, "home_page.cards.hydra.subtitle", "Teste credenciais."))

    def closeEvent(self, event):
        if hasattr(self, 'stress_page') and self.stress_page.executor:
            self.stress_page.executor.stop()

        self.user_settings['language'] = self.current_lang_code
        self.user_settings['theme'] = self.theme_manager.current_theme
        self.user_settings['neon_color'] = self.theme_manager.neon_color

        save_user_settings(self.base_dir, self.user_settings)

        super().closeEvent(event)



# --- EXECUÇÃO PRINCIPAL ---
def iniciar_toolkit(username):
    global main_dashboard

    print(f"Acesso garantido para: {username}")

    base_dir = os.path.dirname(os.path.abspath(__file__))

    main_dashboard = MainWindow(base_dir)

    main_dashboard.setWindowTitle(lang_get(main_dashboard.L, "app.session_title", "AURA Security - Auditoria Ativa ({username})").format(username=username))
    main_dashboard.show()

if __name__ == "__main__":

    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    auth_screen = AuthWindow()
    main_dashboard = None

    auth_screen.login_successful.connect(iniciar_toolkit)

    auth_screen.show()
    sys.exit(app.exec())