import json
import os

NEON_DEFAULT = "#7b4dff"

THEMES = {
    "dark": {
        "bg_main": "#0d0d0d",
        "bg_sidebar": "#0f0f11",
        "bg_card": "#131313",
        "text_main": "#e6eef7",
        "text_secondary": "#9aa7b8",
        "border_card": "#2a2a2a",
        "bg_search": "#0b0b0c",
        "border_search": "#232428",
        "bg_button": "#1b1b1b",
        "bg_button_hover": "#232325",
        "bg_input": "#1b1b1b",
    },
    "light": {
        "bg_main": "#f5f5f5",
        "bg_sidebar": "#e0e0e0",
        "bg_card": "#ffffff",
        "text_main": "#1a1a1a",
        "text_secondary": "#5c5c5c",
        "border_card": "#d3d3d3",
        "bg_search": "#ffffff",
        "border_search": "#cccccc",
        "bg_button": "#e9e9e9",
        "bg_button_hover": "#dedede",
        "bg_input": "#ffffff",
    },
}

SHERLOCK_STYLES = {
    "subtitle": "color: #888; margin-bottom: 10px;",
    "mode_label": "color: white; font-weight: bold;",
    "mode_selector": """
        QComboBox {
            background: #1a1a1a;
            color: #0f0;
            border: 1px solid #0f0;
            padding: 5px 15px;
            border-radius: 5px;
            min-width: 150px;
        }
        QComboBox QAbstractItemView {
            background-color: #1a1a1a;
            color: #0f0;
            selection-background-color: #0f0;
            selection-color: #000;
        }
    """,
    "search_box": "background: #1a1a1a; border-radius: 10px; padding: 5px; border: 1px solid #333;",
    "user_input": "border: none; background: transparent; padding: 10px; font-size: 16px; color: white;",
    "scroll": "border: none; background: transparent; margin-top: 10px;",
    "finished_msg_box": """
        QMessageBox { background-color: #1a1a1a; }
        QLabel { color: white; }
        QPushButton {
            background-color: #333; color: white;
            padding: 5px 15px; border-radius: 3px;
        }
    """,
}

HYDRA_STYLES = {
    "warning": "color: #ffaa00; font-weight: bold;",
    "console": "background:#000;color:#0f0;font-family:Courier New;",
}

JOHN_STYLES = {
    "common_group": "QGroupBox { color: #888; border: 1px solid #333; margin-top: 10px; padding: 10px; }",
    "console": "background: #000; color: #0f0; font-family: 'Courier New';",
}

FIREWALL_STYLES = {
    "log_output": """
        background-color: #050505;
        border: 1px solid #2a2a2a;
        padding: 10px;
        font-family: 'Consolas', 'Monospace';
        color: #00ff00;
    """,
}

KEYLOGGER_STYLES = {
    "status_box": "background: #111; border: 1px solid #333; border-radius: 8px;",
    "dot_idle": "color: #444; font-size: 20px;",
    "status_idle": "color: #888; font-weight: bold;",
    "live_console": "background: #000; color: #0f0; font-family: 'Courier New'; border: 1px solid #222;",
    "open_folder_button": "padding: 15px;",
    "status_running": "color: #ff3333;",
    "status_finished": "color: #00ff00;",
    "dot_running": "color: #ff3333;",
    "dot_finished": "color: #00ff00;",
}

STRESS_TEST_STYLES = {
    "metrics_box": "background: black; color: #00ff00; font-family: Consolas; font-size: 14px;",
}

MANUAL_STYLES = {
    "tab_label": "font-size: 15px; padding: 15px; color: #DDDDDD;",
    "tab_scroll": "border: none; background: transparent;",
}

def sherlock_investigate_button_style(neon_color):
    return f"""
        QPushButton {{
            background-color: transparent; border: 2px solid {neon_color};
            color: {neon_color}; padding: 10px 25px; border-radius: 5px; font-weight: bold;
        }}
        QPushButton:hover {{ background-color: {neon_color}; color: #000; }}
        QPushButton:disabled {{ border-color: #555; color: #555; }}
    """


def sherlock_result_card_style(border_color):
    return f"""
        QFrame {{
            background: #222;
            border-left: 5px solid {border_color};
            border-radius: 5px;
            margin-bottom: 8px;
            padding: 10px;
        }}
        QFrame:hover {{
            background: #2a2a2a;
        }}
    """


def sherlock_result_button_style(border_color):
    return f"""
        QPushButton {{
            background: #333; color: white; border-radius: 3px; padding: 5px; font-size: 11px;
        }}
        QPushButton:hover {{ background: #444; color: {border_color}; }}
    """


def john_start_button_style(neon_color):
    return f"background: {neon_color}; color: black; font-weight: bold;"


def firewall_description_style(theme_key="dark"):
    text_color = THEMES.get(theme_key, THEMES["dark"]).get("text_secondary", "#9aa7b8")
    return f"color: {text_color};"


def keylogger_toggle_button_style(neon_color, running=False):
    if running:
        return "background: #551111; color: white; font-weight: bold;"
    return f"background: {neon_color}; color: black; font-weight: bold;"


def main_window_stylesheet(theme_colors, neon_color):
    return f"""
    QMainWindow {{
        background-color: {theme_colors['bg_main']};
    }}
    QFrame#Sidebar {{
        background-color: {theme_colors['bg_sidebar']};
    }}
    QFrame#ContentFrame, QWidget#PageWidget {{
        background-color: {theme_colors['bg_main']};
    }}
    QLabel {{
        color: {theme_colors['text_main']};
    }}
    QLabel#AuraTitle {{
        color: {neon_color};
    }}
    QPushButton#SidebarButton {{
        background-color: {theme_colors['bg_button']};
        color: {theme_colors['text_main']};
        border: none;
        border-radius: 8px;
        padding-left: 15px;
    }}
    QPushButton#SidebarButton:hover {{
        background-color: {theme_colors['bg_button_hover']};
        color: {theme_colors['text_main']};
    }}
    QGroupBox {{
        color: {theme_colors['text_main']};
        border: 1px solid {theme_colors['border_card']};
        border-radius: 10px;
        padding-top: 20px;
        margin-top: 10px;
        background-color: {theme_colors['bg_main']};
    }}
    QLineEdit {{
        background-color: {theme_colors['bg_input']};
        color: {theme_colors['text_main']};
        border: 1px solid {theme_colors['border_card']};
        border-radius: 5px;
        padding: 5px;
    }}
    QScrollArea {{
        background-color: {theme_colors['bg_main']};
        border: none;
    }}
    QScrollArea QWidget {{
        background-color: {theme_colors['bg_main']};
    }}
    QComboBox {{
        background-color: {theme_colors['bg_input']};
        color: {theme_colors['text_main']};
        border: 1px solid {theme_colors['border_card']};
        border-radius: 5px;
        padding: 3px;
    }}
    QRadioButton {{
        color: {theme_colors['text_main']};
        background-color: {theme_colors['bg_main']};
    }}
    QPushButton {{
        background-color: {theme_colors['bg_button']};
        color: {theme_colors['text_main']};
        border: none;
        border-radius: 5px;
        padding: 8px 15px;
    }}
    QPushButton:hover {{
        background-color: {theme_colors['bg_button_hover']};
    }}
    QTabWidget::pane {{
        border: 1px solid #333333;
        background: transparent;
    }}
    QTabBar::tab {{
        background: #1A1A1A;
        color: #888888;
        padding: 10px 20px;
        border-top-left-radius: 8px;
        border-top-right-radius: 8px;
        margin-right: 2px;
    }}
    QTabBar::tab:selected {{
        background: #252525;
        color: {neon_color};
        border-bottom: 2px solid {neon_color};
    }}
    QTabBar::tab:hover {{
        background: #333333;
        color: white;
    }}
    """

class ThemeManager:
    def __init__(self, initial_settings):
        self.current_theme = initial_settings.get("theme", "dark")
        self.neon_color = initial_settings.get("neon_color", NEON_DEFAULT)

    def set_base_theme(self, theme_key):
        self.current_theme = theme_key

    def set_neon_color(self, color):
        self.neon_color = color
        
def load_user_settings(base_dir):
    settings_path = os.path.join(base_dir, "config", "user_settings.json")
    default_settings = {
        "language": "pt", 
        "theme": "dark",
        "neon_color": NEON_DEFAULT,
    }
    
    os.makedirs(os.path.dirname(settings_path), exist_ok=True)
    
    if os.path.exists(settings_path):
        try:
            with open(settings_path, "r", encoding="utf-8") as f:
                settings = json.load(f)
                settings.pop("special_theme_active", None)
                settings.pop("special_theme_key", None)
                return {**default_settings, **settings} 
        except (json.JSONDecodeError, IOError):
            print("[WARN] Erro ao carregar user_settings.json. Usando padrão.")
            
    return default_settings

def save_user_settings(base_dir, settings):
    settings_to_save = {k: v for k, v in settings.items() if k not in ["special_theme_active", "special_theme_key"]}
    settings_path = os.path.join(base_dir, "config", "user_settings.json")
    try:
        with open(settings_path, "w", encoding="utf-8") as f:
            json.dump(settings_to_save, f, indent=4, ensure_ascii=False)
    except IOError as e:
        print(f"[ERROR] Falha ao salvar user_settings.json: {e}")
