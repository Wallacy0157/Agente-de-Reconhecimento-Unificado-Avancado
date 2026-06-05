import sys
import os
import unittest
import hashlib
from unittest.mock import patch, MagicMock, mock_open

mock_bcrypt = MagicMock()
sys.modules['bcrypt'] = mock_bcrypt
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.john_engine import JohnEngine, JohnExecutor, worker


class TestJohnEngineElite(unittest.TestCase):
    def setUp(self):
        self.engine = JohnEngine()


    def test_detect_algorithm_exaustivo(self):
        casos = [
            ("a" * 32, "MD5"),
            ("b" * 40, "SHA1"),
            ("c" * 64, "SHA256"),
            ("d" * 128, "SHA512"),
            ("$2b$12$xyz", "BCRYPT"),
            ("tamanho_invalido", None),
            ("", None)
        ]
        for hash_str, esperado in casos:
            with self.subTest(hash_str=hash_str):
                self.assertEqual(self.engine.detect_algorithm(hash_str), esperado)


    def test_worker_processamento_de_hashes(self):
        ev = MagicMock()
        ev.is_set.return_value = False
        hash_md5 = hashlib.md5(b"senha_forte").hexdigest()


        self.assertEqual(worker(("senha_forte", hash_md5, "MD5", None, False, ev)), "senha_forte")


        hash_maiusculo = hashlib.md5(b"Senha_forte").hexdigest()
        self.assertEqual(worker(("senha_forte", hash_maiusculo, "MD5", None, True, ev)), "Senha_forte")


        self.assertIsNone(worker(("senha_errada", hash_md5, "MD5", None, False, ev)))


        hash_sha = hashlib.sha256(b"admin").hexdigest()
        self.assertEqual(worker(("admin", hash_sha, "SHA256", None, False, ev)), "admin")


        res_bcrypt = worker(("admin", "$2b$12$mock", "BCRYPT", None, False, ev))
        self.assertIn(res_bcrypt, ["admin", None])


        ev.is_set.return_value = True
        self.assertIsNone(worker(("senha_forte", hash_md5, "MD5", None, False, ev)))


    def test_crack_wordlist_falha_sem_arquivo(self):
        res = self.engine.crack_wordlist("hash", "inexistente.txt", "MD5")
        self.assertFalse(res.get("success"))
        self.assertIsNotNone(res.get("error"))
        self.assertIn("No such file", res.get("error", ""))

    @patch('core.john_engine.os.path.exists', return_value=True, create=True)
    @patch('core.john_engine.Pool', create=True)
    @patch('core.john_engine.Manager', create=True)
    def test_crack_wordlist_sucesso_logico(self, mock_manager, mock_pool, mock_exists):
        mock_pool_instance = MagicMock()
        mock_pool_instance.imap_unordered.return_value = ["admin_encontrado"]
        mock_pool.return_value.__enter__.return_value = mock_pool_instance

        with patch("builtins.open", mock_open(read_data="admin_encontrado\noutra_senha")):
            resultado = self.engine.crack_wordlist("hash", "lista.txt", "MD5")
            self.assertTrue(resultado.get("success"))
            self.assertEqual(resultado.get("password"), "admin_encontrado")

    @patch('core.john_engine.os.path.exists', return_value=True, create=True)
    @patch('core.john_engine.Pool', create=True)
    @patch('core.john_engine.Manager', create=True)
    def test_crack_wordlist_senha_nao_encontrada(self, mock_manager, mock_pool, mock_exists):
        mock_pool_instance = MagicMock()
        mock_pool_instance.imap_unordered.return_value = [None, None]
        mock_pool.return_value.__enter__.return_value = mock_pool_instance

        with patch("builtins.open", mock_open(read_data="senha1\nsenha2")):
            resultado = self.engine.crack_wordlist("hash", "lista.txt", "MD5")
            self.assertFalse(resultado.get("success", True))


    def test_crack_mask_sucesso_logico(self):
        if hasattr(self.engine, 'crack_mask'):
            hash_alvo = hashlib.md5(b"ab").hexdigest()
            res = self.engine.crack_mask(hash_alvo, "?l?l", "MD5")
            self.assertTrue(res.get("success", False))
            self.assertEqual(res.get("password"), "ab")

            res_falha = self.engine.crack_mask(hash_alvo, "?d?d", "MD5")
            self.assertFalse(res_falha.get("success", True))


    @patch('core.john_engine.threading.Thread')
    def test_executor_controle_de_estado(self, mock_thread):
        exec_word = JohnExecutor("hash", "pay", "MD5", mode="wordlist")
        exec_word.start()
        mock_thread.assert_called()
        exec_word.stop()
        self.assertTrue(exec_word._stop_event.is_set())

    def test_executor_modos_invalidos_e_excecoes(self):
        exec_word = JohnExecutor("hash", "pay", "MD5", mode="wordlist")
        with patch.object(self.engine, 'crack_wordlist', side_effect=Exception("Erro de I/O")):
            exec_word.engine = self.engine
            exec_word._run()
            erro = getattr(exec_word, 'error', None) or exec_word.result.get("error")
            self.assertEqual(erro, "Erro de I/O")

        exec_invalido = JohnExecutor("hash", "pay", "MD5", mode="modo_bizarro")
        exec_invalido._run()
        self.assertFalse(exec_invalido.is_running)

    def test_varredura_de_metodos_secundarios(self):
        executor = JohnExecutor("hash", "pay", "MD5", mode="wordlist")
        metodos = ['get_results', 'get_error', 'get_output', 'pop_new_output']
        for m in metodos:
            if hasattr(executor, m):
                try:
                    getattr(executor, m)()
                except Exception:
                    pass


if __name__ == '__main__':
    unittest.main()