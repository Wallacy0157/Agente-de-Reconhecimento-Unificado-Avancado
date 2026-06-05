import sys
import os
import unittest
import json
import subprocess
import shutil
from unittest.mock import patch, MagicMock, mock_open

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import core.sherlock
from core.sherlock import SherlockExecutor


class TestSherlockGodMode(unittest.TestCase):
    def setUp(self):
        self.executor = SherlockExecutor("alvo_teste", "username")


    @patch("core.sherlock.os.name", "nt")
    @patch("shutil.which", return_value="sherlock")
    @patch("subprocess.Popen")
    def test_run_ambiente_windows(self, mock_popen, mock_which):
        mock_process = MagicMock()
        mock_process.poll.return_value = 0
        mock_popen.return_value = mock_process
        self.executor._run()

    @patch("core.sherlock.os.name", "posix")
    @patch("shutil.which", return_value="sherlock")
    @patch("subprocess.Popen")
    def test_run_ambiente_linux(self, mock_popen, mock_which):
        mock_process = MagicMock()
        mock_process.poll.return_value = 0
        mock_popen.return_value = mock_process
        self.executor._run()


    @patch("os.path.exists", return_value=True)
    @patch("os.remove", side_effect=PermissionError("Sem permissão para apagar txt"))
    @patch("shutil.which", return_value="sherlock")
    @patch("subprocess.Popen")
    def test_arquivos_quebrados_e_erros_de_os(self, mock_popen, mock_which, mock_remove, mock_exists):
        mock_process = MagicMock()
        mock_process.poll.return_value = 0
        mock_popen.return_value = mock_process


        json_quebrado = "{isso_nao_e_json: verdadeiro]"

        def open_bizarro(nome_arquivo, *args, **kwargs):
            if nome_arquivo.endswith('.json'):
                return mock_open(read_data=json_quebrado).return_value
            return mock_open(read_data="").return_value

        with patch("builtins.open", side_effect=open_bizarro):
            self.executor._run()


    @patch("shutil.which", return_value="sherlock")
    @patch("subprocess.Popen")
    def test_timeout_do_sherlock(self, mock_popen, mock_which):
        mock_process = MagicMock()
        mock_process.wait.side_effect = subprocess.TimeoutExpired(cmd="sherlock", timeout=60)
        mock_popen.return_value = mock_process

        self.executor._run()
        self.assertFalse(self.executor.is_running)


    def test_alvos_invalidos(self):
        alvos_bizarros = ["", "   ", None, "!@#$%", ["lista", "falsa"]]
        for alvo in alvos_bizarros:
            exec_invalido = SherlockExecutor(alvo, "username")
            exec_invalido._run()


    @patch("threading.Thread")
    def test_bombardeio_de_metodos(self, mock_thread):
        self.executor.start()
        self.executor.stop()


        municao = [None, "", "teste", 123, [], {}, True]


        for nome_atributo in dir(self.executor):
            if not nome_atributo.startswith('__') and nome_atributo not in ['_run', 'start', 'stop']:
                metodo = getattr(self.executor, nome_atributo)
                if callable(metodo):
                    for bala in municao:
                        try:
                            metodo(bala)
                        except Exception:
                            pass
                        try:
                            metodo()
                        except Exception:
                            pass


        for nome_funcao in dir(core.sherlock):
            if not nome_funcao.startswith('__'):
                obj = getattr(core.sherlock, nome_funcao)
                if callable(obj) and obj.__module__ == 'core.sherlock':
                    for bala in municao:
                        try:
                            obj(bala)
                        except Exception:
                            pass
                        try:
                            obj()
                        except Exception:
                            pass


if __name__ == '__main__':
    unittest.main()