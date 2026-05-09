import os
import sys
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
            # tenta idioma atual
            section = L.get("manual", {}).get(key)

            # fallback se não existir
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