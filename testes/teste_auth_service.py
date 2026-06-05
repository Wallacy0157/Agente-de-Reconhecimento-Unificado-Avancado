import sys
import os
import unittest
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from services.auth_service import login, registrar, AuthError, _extrair_mensagem_erro
from requests.exceptions import ConnectionError, Timeout


class TestAuthServiceElite(unittest.TestCase):


    def test_extrair_mensagem_erro_todas_ramificacoes(self):
        mock_resp = MagicMock()
        mock_resp.status_code = 400


        mock_resp.json.return_value = {
            "parametros-invalidos": [
                {"campo": "email", "motivo": "Formato inválido"},
                {"campo": "senha", "motivo": "Muito curta"}
            ]
        }
        erro_formatado = _extrair_mensagem_erro(mock_resp)
        self.assertIn("• email: Formato inválido", erro_formatado)
        self.assertIn("• senha: Muito curta", erro_formatado)


        mock_resp.json.return_value = {"detail": "Credenciais incorretas"}
        self.assertEqual(_extrair_mensagem_erro(mock_resp), "Credenciais incorretas")


        mock_resp.json.return_value = {"title": "Acesso Negado"}
        self.assertEqual(_extrair_mensagem_erro(mock_resp), "Acesso Negado")


        mock_resp.json.return_value = {"erro_desconhecido": "fatal"}
        self.assertIn("Erro inesperado (HTTP 400)", _extrair_mensagem_erro(mock_resp))


        mock_resp.json.side_effect = Exception("Not a JSON")
        self.assertIn("Erro inesperado (HTTP 400)", _extrair_mensagem_erro(mock_resp))


    @patch('services.auth_service.api_client')
    def test_falhas_de_conexao_e_timeouts(self, mock_api):

        cenarios_de_rede = [
            (ConnectionError("Recusado"), "Não foi possível conectar ao servidor."),
            (Timeout("Demorou muito"), "Não foi possível conectar ao servidor."),
            (Exception("Crash interno da lib"), "Erro de conexão inesperado.")
        ]

        for excecao_simulada, mensagem_esperada in cenarios_de_rede:
            with self.subTest(erro=excecao_simulada.__class__.__name__):
                mock_api.post.side_effect = excecao_simulada


                with self.assertRaises(AuthError) as ctx_login:
                    login("admin@admin.com", "123")
                self.assertEqual(str(ctx_login.exception), mensagem_esperada)


                with self.assertRaises(AuthError) as ctx_reg:
                    registrar("a@a.com", "A", "user", "1", "1")
                self.assertEqual(str(ctx_reg.exception), mensagem_esperada)


    @patch('services.auth_service.api_client')
    def test_rejeicao_por_regra_de_negocio(self, mock_api):
        mock_resp = MagicMock()
        mock_resp.status_code = 401
        mock_resp.json.return_value = {"detail": "Senha Incorreta"}
        mock_api.post.return_value = mock_resp


        with self.assertRaises(AuthError) as ctx_login:
            login("user@user.com", "senha_errada")
        self.assertEqual(str(ctx_login.exception), "Senha Incorreta")


        mock_resp.json.return_value = {"detail": "E-mail já cadastrado"}
        with self.assertRaises(AuthError) as ctx_reg:
            registrar("a@a.com", "nome", "user", "123", "123")
        self.assertEqual(str(ctx_reg.exception), "E-mail já cadastrado")


    @patch('services.auth_service.api_client')
    def test_registrar_sucesso(self, mock_api):
        mock_api.post.return_value.status_code = 200


        registrar("aluno@ucb.pt", "Aluno", "user", "123", "123")


        chamada_args = mock_api.post.call_args[0]
        self.assertEqual(chamada_args[0], "/usuarios")
        self.assertEqual(chamada_args[1]["email"], "aluno@ucb.pt")

    @patch('services.auth_service.api_client')
    def test_login_sucesso(self, mock_api):
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {"token": "token-jwt-aprovado", "nome": "Admin"}
        mock_api.post.return_value = mock_resp

        resultado = login("admin@admin.com", "senha123")


        mock_api.set_token.assert_called_with("token-jwt-aprovado")
        self.assertEqual(resultado["token"], "token-jwt-aprovado")


if __name__ == '__main__':
    unittest.main()