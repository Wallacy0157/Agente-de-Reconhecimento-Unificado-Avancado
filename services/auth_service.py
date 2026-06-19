import base64
import json

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


def _decode_token_claims(token: str) -> dict:
    try:
        payload = token.split(".")[1]
        payload += "=" * (-len(payload) % 4)
        decoded = base64.urlsafe_b64decode(payload.encode("utf-8"))
        claims = json.loads(decoded.decode("utf-8"))
    except Exception:
        return {}

    return {
        key: claims.get(key)
        for key in ("email", "nome", "username")
        if claims.get(key)
    }


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


def login(username: str, senha: str) -> dict:
    try:
        response = api_client.post("/usuarios/login", {"username": username, "senha": senha})
    except (ConnectionError, Timeout):
        raise AuthError("Não foi possível conectar ao servidor.")
    except Exception:
        raise AuthError("Erro de conexão inesperado.")

    if response.status_code == 200:
        data = response.json()
        api_client.set_token(data["token"])
        data.update(_decode_token_claims(data["token"]))
        data.setdefault("username", username)
        return data

    raise AuthError(_extrair_mensagem_erro(response))