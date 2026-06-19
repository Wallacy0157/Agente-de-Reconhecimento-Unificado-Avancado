import ctypes
import os
import sys


ICON_DIR = os.path.join("assets", "icons")
PREFERRED_ICON_NAMES = (
    "aura.ico",
    "aura.png",
    "aura.jpg",
    "aura.jpeg",
    "aura.webp",
    "app.ico",
    "app.png",
)
SUPPORTED_EXTENSIONS = (".ico", ".png", ".jpg", ".jpeg", ".webp")
WINDOWS_APP_ID = "Wallacy0157.AURA.SecurityToolkit"


def configure_windows_app_id(app_id=WINDOWS_APP_ID):
    """Ajuda o Windows a usar o icone do AURA na barra de tarefas."""
    if not sys.platform.startswith("win"):
        return
    try:
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(app_id)
    except Exception:
        pass


def find_app_icon(base_dir):
    icons_dir = os.path.join(base_dir, ICON_DIR)
    if not os.path.isdir(icons_dir):
        return None

    for filename in PREFERRED_ICON_NAMES:
        path = os.path.join(icons_dir, filename)
        if os.path.isfile(path):
            return path

    for filename in sorted(os.listdir(icons_dir)):
        if filename.lower().endswith(SUPPORTED_EXTENSIONS):
            path = os.path.join(icons_dir, filename)
            if os.path.isfile(path):
                return path

    return None


def apply_app_icon(target, base_dir):
    icon_path = find_app_icon(base_dir)
    if not icon_path:
        return None

    try:
        from PyQt6.QtGui import QIcon

        icon = QIcon(icon_path)
        if icon.isNull():
            return None
        target.setWindowIcon(icon)
        return icon
    except Exception:
        return None
