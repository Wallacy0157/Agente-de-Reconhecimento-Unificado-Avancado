from requests.exceptions import ConnectionError, Timeout

from services import api_client


class AuthError(Exception):
    pass


def _extrair_mensagem_erro(response) -> str:
    try:
        body = response.json()

        params = body.get("parametros-invalidos", [])
        if params:
            msgs = [f"• {p['campo']}: {p['motivo']}" for p in params]
            return "\n".join(msgs)

        if "detail" in body:
            return body["detail"]

        if "title" in body:
            return body["title"]
    except Exception:
        pass
    return f"Erro inesperado (HTTP {response.status_code})"


def registrar(email: str, nome: str, username: str, senha: str, confirma_senha: str) -> None:
    payload = {
        "email": email,
        "nome": nome,
        "username": username,
        "senha": senha,
        "confirmaSenha": confirma_senha,
    }

    try:
        response = api_client.post("/usuarios", payload)
    except (ConnectionError, Timeout):
        raise AuthError("Não foi possível conectar ao servidor.")
    except Exception:
        raise AuthError("Erro de conexão inesperado.")

    if response.status_code == 200:
        return

    raise AuthError(_extrair_mensagem_erro(response))


def login(email: str, senha: str) -> dict:
    try:
        response = api_client.post("/usuarios/login", {"email": email, "senha": senha})
    except (ConnectionError, Timeout):
        raise AuthError("Não foi possível conectar ao servidor.")
    except Exception:
        raise AuthError("Erro de conexão inesperado.")

    if response.status_code == 200:
        data = response.json()
        api_client.set_token(data["token"])
        return data

    raise AuthError(_extrair_mensagem_erro(response))
