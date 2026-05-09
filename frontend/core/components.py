import json
import os
import sys

from PyQt6.QtCore import Qt, QSize, QThread, pyqtSignal, QTimer, QLocale
from PyQt6.QtGui import QFont, QColor, QPainter, QBrush, QPen, QPalette
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame,
    QGraphicsDropShadowEffect, QGroupBox, QRadioButton,
    QComboBox, QPushButton, QColorDialog,
    QScrollArea
)
from core.config import THEMES, NEON_DEFAULT


def load_language_json(lang_code, base_dir=None):
    """Carrega o arquivo JSON para o código de idioma fornecido."""

    if base_dir is None:
        if getattr(sys, 'frozen', False):
            base_dir = os.path.dirname(sys.executable)
        else:
            base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

    lang_path = os.path.join(base_dir, "languages", f"{lang_code}.json")

    if not os.path.exists(lang_path):
        print(f"[WARN] Arquivo de idioma {lang_code}.json não encontrado em {lang_path}. Usando pt.json como fallback.")
        lang_path = os.path.join(base_dir, "languages", "pt.json")

    try:
        with open(lang_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"[ERROR] Falha ao carregar JSON de idioma: {e}. Retornando dicionário vazio.")
        return {}


def lang_get(L: dict, key: str, fallback: str):
    """Obtém um valor traduzido usando uma chave pontilhada (ex: 'sidebar.home')."""
    parts = key.split('.')
    value = L
    for part in parts:
        value = value.get(part)
        if value is None:
            return fallback
    return value if isinstance(value, str) else fallback


class NeonCard(QFrame):
    """Um QFrame estilizado com sombra e cor neon personalizável."""

    def __init__(self, icon, title, subtitle, neon_color, theme_manager, parent=None):
        super().__init__(parent)
        self.neon_color = neon_color
        self.theme_manager = theme_manager

        self.current_theme_key = theme_manager.current_theme

        self.setFrameShape(QFrame.Shape.StyledPanel)
        self.setFrameShadow(QFrame.Shadow.Raised)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setFixedSize(QSize(280, 160))
        self.setObjectName("NeonCard")

        self.effect = QGraphicsDropShadowEffect(self)
        self._apply_shadow()

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(20, 15, 20, 15)
        self.layout.setSpacing(8)

        self.icon_label = QLabel(icon)
        self.icon_label.setFont(QFont("Arial", 28))
        self.layout.addWidget(self.icon_label)

        self.title_label = QLabel(title)
        self.title_label.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        self.layout.addWidget(self.title_label)

        self.subtitle_label = QLabel(subtitle)
        self.subtitle_label.setFont(QFont("Arial", 10))
        self.subtitle_label.setWordWrap(True)
        self.layout.addWidget(self.subtitle_label)

        self.layout.addStretch()

        self.on_card_activated = lambda: None

        self.on_card_activated = lambda: None

    def mousePressEvent(self, event):
        """Trata o clique de forma segura para o PyQt6."""
        if event.button() == Qt.MouseButton.LeftButton:
            if self.on_card_activated:
                self.on_card_activated()

        event.accept()

    def _get_style_sheet(self, theme_key):
        T = THEMES.get(theme_key, THEMES['dark'])
        return f"""
            QFrame#NeonCard {{
                background-color: {T['bg_card']};
                border: 2px solid {self.neon_color}; 
                border-radius: 12px;
            }}
            QFrame#NeonCard:hover {{
                background-color: {T['bg_card']};
                border: 2px solid {T['text_main']}; 
            }}
            QFrame#NeonCard QLabel {{
                color: {T['text_main']};
            }}
            QFrame#NeonCard QLabel:last-child {{ 
                color: {T['text_secondary']};
            }}
        """

    def _apply_shadow(self):
        self.effect.setBlurRadius(18)
        self.effect.setColor(QColor(self.neon_color))
        self.effect.setOffset(0, 0)
        self.setGraphicsEffect(self.effect)

    def set_neon_color(self, color, theme_key):
        self.neon_color = color
        self.current_theme_key = theme_key

        self._apply_shadow()
        self.setStyleSheet(self._get_style_sheet(theme_key))

    def set_texts(self, title, subtitle):
        self.title_label.setText(title)
        self.subtitle_label.setText(subtitle)