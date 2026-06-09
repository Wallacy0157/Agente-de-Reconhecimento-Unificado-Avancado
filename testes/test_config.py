import sys
import os
import unittest
import json
from unittest.mock import patch, mock_open

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.config import (
    ThemeManager, load_user_settings, save_user_settings, NEON_DEFAULT,
    sherlock_investigate_button_style, sherlock_result_card_style,
    sherlock_result_button_style, john_start_button_style,
    firewall_description_style, keylogger_toggle_button_style,
    sherlock_mode_selector_style, sherlock_search_box_style,
    themed_console_style, john_common_group_style,
    manual_tab_label_style, status_text_style, main_window_stylesheet
)


class TestConfigFull(unittest.TestCase):
    def test_theme_manager(self):
        manager = ThemeManager({"theme": "light", "neon_color": "#123"})
        manager.set_base_theme("dark")
        manager.set_neon_color("#321")
        self.assertEqual(manager.current_theme, "dark")

    @patch("core.config.os.makedirs")
    @patch("core.config.os.path.exists", return_value=True)
    def test_load_settings_sucesso(self, mock_exists, mock_makedirs):
        with patch("builtins.open", mock_open(read_data='{"language": "en"}')):
            self.assertEqual(load_user_settings("dir")["language"], "en")

    @patch("core.config.os.makedirs")
    @patch("core.config.os.path.exists", return_value=True)
    def test_load_settings_json_corrompido(self, mock_exists, mock_makedirs):
        with patch("builtins.open", mock_open(read_data='{erro}')):
            self.assertEqual(load_user_settings("dir")["language"], "pt")

    @patch("core.config.json.dump")
    @patch("core.config.os.makedirs")
    def test_save_settings_sucesso(self, mock_makedirs, mock_json_dump):
        with patch("builtins.open", mock_open()):
            save_user_settings("dir", {"theme": "dark", "special_theme_active": True})
            args, _ = mock_json_dump.call_args
            self.assertNotIn("special_theme_active", args[0])

    @patch("core.config.os.makedirs")
    @patch("builtins.open", side_effect=IOError("Erro simulado"))
    def test_save_settings_erro_disco(self, mock_file, mock_makedirs):
        save_user_settings("dir", {"theme": "dark"})

    def test_todas_funcoes_css(self):
        self.assertIn("#fff", sherlock_investigate_button_style("#fff"))
        self.assertIn("#111", sherlock_result_card_style("#111"))
        self.assertIn("#222", sherlock_result_button_style("#222"))
        self.assertIn("#333", john_start_button_style("#333"))
        self.assertIn("color", firewall_description_style("dark"))
        self.assertIn("#5c5c5c", firewall_description_style("light"))
        self.assertIn("#551111", keylogger_toggle_button_style("#444", running=True))
        self.assertIn("#444", keylogger_toggle_button_style("#444", running=False))
        self.assertIn("#ffffff", sherlock_mode_selector_style("light", "#fff"))
        self.assertIn("#ffffff", sherlock_search_box_style("light"))
        self.assertIn("#ffffff", themed_console_style("light"))
        self.assertIn("#f5f5f5", john_common_group_style("light"))
        self.assertIn("#1a1a1a", manual_tab_label_style("light"))
        self.assertIn("#5c5c5c", status_text_style("light", "idle"))

        tema_falso = {'bg_main': '#000', 'bg_sidebar': '#111', 'text_main': '#fff',
                      'bg_button': '#222', 'bg_button_hover': '#333', 'border_card': '#444', 'bg_input': '#555'}
        stylesheet = main_window_stylesheet(tema_falso, "#0f0")
        self.assertIn("#000", stylesheet)
        self.assertIn("QCheckBox::indicator", stylesheet)
        self.assertIn("border: 1px solid #3f3f3f", stylesheet)


if __name__ == '__main__':
    unittest.main()
