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
