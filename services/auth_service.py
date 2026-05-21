from services import api_client


def registrar(email: str, nome: str, username: str, senha: str, confirma_senha: str) -> None:
    payload = {
        "email": email,
        "nome": nome,
        "username": username,
        "senha": senha,
        "confirmaSenha": confirma_senha,
    }
    response = api_client.post("/usuarios", payload)
    response.raise_for_status()


def login(email: str, senha: str) -> dict:
    response = api_client.post("/usuarios/login", {"email": email, "senha": senha})
    response.raise_for_status()
    data = response.json()
    api_client.set_token(data["token"])
    return data
