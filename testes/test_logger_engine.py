import sys
import os
import unittest
from unittest.mock import patch, MagicMock, mock_open

sys.modules['pynput'] = MagicMock()
sys.modules['pynput.keyboard'] = MagicMock()
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.logger_engine import KeyloggerEngine


class TestLoggerEngineFull(unittest.TestCase):
    def setUp(self):
        self.engine = KeyloggerEngine("dir", flush_size=2)

    @patch("core.logger_engine.socket.socket")
    def test_get_ip_and_sys_info(self, mock_socket):
        mock_instance = MagicMock()
        mock_instance.getsockname.return_value = ["1.1.1.1"]
        mock_socket.return_value = mock_instance
        info = self.engine._get_system_info()
        self.assertEqual(info["ip"], "1.1.1.1")

    @patch("core.logger_engine.platform.system", return_value="Windows")
    def test_get_active_window(self, mock_sys):
        win = self.engine._get_active_window()
        self.assertEqual(win, "Generic Window")

    def test_on_press_todas_teclas(self):
        self.engine._set_running(True)
        from pynput import keyboard


        del keyboard.Key.space.char
        del keyboard.Key.ctrl.char
        del keyboard.Key.alt.char
        del keyboard.Key.tab.char
        del keyboard.Key.esc.char
        del keyboard.Key.backspace.char
        del keyboard.Key.enter.char

        self.engine._on_press(keyboard.Key.space)
        self.engine._on_press(keyboard.Key.ctrl)
        self.engine._on_press(keyboard.Key.alt)
        self.engine._on_press(keyboard.Key.tab)
        self.engine._on_press(keyboard.Key.esc)
        self.assertIn("[CTRL]", self.engine.line_buffer)

        self.engine._on_press(keyboard.Key.backspace)
        self.engine._on_press(keyboard.Key.enter)
        self.assertEqual(self.engine.stats["enters"], 1)

    @patch("core.logger_engine.os.makedirs")
    @patch("core.logger_engine.keyboard.Listener")
    @patch("core.logger_engine.threading.Thread")
    def test_start_and_stop(self, mock_thread, mock_listener, mock_makedirs):
        with patch("builtins.open", mock_open()):
            file = self.engine.start()
            self.assertIn("audit_", file)
            self.assertTrue(self.engine.is_running)

            self.engine.stats["top_keys"] = {"a": 1}
            self.engine.stop()
            self.assertFalse(self.engine.is_running)


if __name__ == '__main__':
    unittest.main()