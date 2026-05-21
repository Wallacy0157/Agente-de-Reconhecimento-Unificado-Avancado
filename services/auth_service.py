from services import api_client


def registrar(email: str, nome: str, username: str, senha: str, confirma_senha: str) -> dict:
    payload = {
        "email": email,
        "nome": nome,
        "username": username,
        "senha": senha,
        "confirmaSenha": confirma_senha,
    }
    response = api_client.post("/usuarios", payload)
    response.raise_for_status()
    return response.json() if response.content else {}
