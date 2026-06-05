import sys
import os
import unittest
from unittest.mock import patch

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from services import api_client


class TestApiClientFull(unittest.TestCase):

    def setUp(self):
        api_client.session.headers.pop("Authorization", None)

    def test_set_token(self):
        api_client.set_token("meu_token_jwt")
        self.assertEqual(api_client.session.headers.get("Authorization"), "Bearer meu_token_jwt")

    @patch('services.api_client.requests.Session.request')
    def test_get_com_e_sem_token(self, mock_request):
        mock_request.return_value.status_code = 200

        api_client.get("/endpoint_privado")
        mock_request.assert_called_with("GET", f"{api_client.BASE_URL}/endpoint_privado")

        api_client.set_token("token_secreto")
        api_client.get("/usuarios/login")
        kwargs_chamada = mock_request.call_args[1]
        self.assertNotIn("Authorization", kwargs_chamada.get("headers", {}))

    @patch('services.api_client.requests.Session.request')
    def test_post(self, mock_request):
        mock_request.return_value.status_code = 201
        res = api_client.post("/login", {"user": "admin"})
        mock_request.assert_called_once()
        self.assertEqual(res.status_code, 201)


    @patch('services.api_client.requests.Session.request', side_effect=Exception("Servidor Offline"))
    def test_request_exception(self, mock_request):
        with self.assertRaises(Exception):
            api_client.get("/api/teste")