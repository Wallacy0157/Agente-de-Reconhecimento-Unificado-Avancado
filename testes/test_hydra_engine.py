import sys
import os
import unittest
from unittest.mock import patch, MagicMock, mock_open

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from core.hydra_engine import HydraExecutor


class TestHydraEngineFull(unittest.TestCase):
    def setUp(self):
        self.exec_valid = HydraExecutor(["127.0.0.1"], "ssh", "admin", "123", None, None, 22, 4, True, True)

    def test_validacao_completa(self):
        vazio = HydraExecutor([], None, None, None, None, None, None, None, None, None)
        self.assertEqual(vazio._validate(), "Informe ao menos um alvo.")

        sem_servico = HydraExecutor(["10.0.0.1"], None, None, None, None, None, None, None, None, None)
        self.assertEqual(sem_servico._validate(), "Informe o serviço.")

        http_falta = HydraExecutor(["10.0.0.1"], "http-post-form", None, None, None, None, None, None, None, None)
        self.assertEqual(http_falta._validate(), "Preencha todos os campos do HTTP POST.")

        http_errado = HydraExecutor(["10.0.0.1"], "http-post-form", None, None, None, None, None, None, None, None,
                                    "/l", "user=1", "F")
        self.assertEqual(http_errado._validate(), "Use ^USER^ e ^PASS^ nos parâmetros.")

    def test_montagem_comando(self):
        cmd = self.exec_valid._build_command()
        self.assertIn("-V", cmd)
        self.assertIn("-f", cmd)
        self.assertIn("-t", cmd)
        self.assertIn("ssh", cmd)

    @patch('core.hydra_engine.shutil.which', return_value="hydra")
    @patch('core.hydra_engine.subprocess.Popen')
    def test_run_sucesso(self, mock_popen, mock_which):
        mock_proc = MagicMock()
        mock_proc.stdout = ["Tentando admin:123", "Sucesso!"]
        mock_proc.poll.return_value = None
        mock_proc.wait.return_value = 0
        mock_popen.return_value = mock_proc

        self.exec_valid._run()
        self.assertEqual(self.exec_valid.return_code, 0)
        self.assertIn("Sucesso!", self.exec_valid.get_output()[-1])

    @patch('core.hydra_engine.os.makedirs')
    @patch('core.hydra_engine.json.dump')
    def test_save_log(self, mock_json, mock_makedirs):
        self.exec_valid.return_code = 0
        with patch("builtins.open", mock_open()):
            log = self.exec_valid.save_log("dir")
            self.assertIn("hydra", log)

    def test_start_stop(self):
        self.exec_valid.start()
        self.assertTrue(self.exec_valid.is_running)
        self.exec_valid.stop()
        self.assertTrue(self.exec_valid._stop_requested)
        self.exec_valid.pop_new_output()


if __name__ == '__main__':
    unittest.main()