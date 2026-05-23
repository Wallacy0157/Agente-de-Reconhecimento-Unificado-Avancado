import logging

from requests.exceptions import ConnectionError, Timeout

from services import api_client

logger = logging.getLogger(__name__)

_ENDPOINT = "/scans"
_TIMEOUT = 30


def _mensagem_erro_http(status_code: int, response=None) -> str:
    if response is not None:
        try:
            body = response.json()
            if "detail" in body:
                return body["detail"]
            if "title" in body:
                return body["title"]
        except Exception:
            pass

    if status_code == 401:
        return "Sessão expirada. Faça login novamente."
    if status_code == 403:
        return "Acesso negado a este recurso."
    if status_code == 404:
        return "Varredura não encontrada."
    if 500 <= status_code < 600:
        return "Erro interno do servidor. Tente novamente."
    return f"Erro inesperado (HTTP {status_code})."


def listar_scans() -> tuple[bool, list[dict] | str]:
    try:
        response = api_client.get(_ENDPOINT, timeout=_TIMEOUT)

        if response.status_code == 200:
            return True, response.json()

        msg = _mensagem_erro_http(response.status_code, response)
        logger.warning("Falha ao listar scans: HTTP %d — %s", response.status_code, msg)
        return False, msg

    except Timeout:
        logger.error("Timeout ao listar scans.")
        return False, "Tempo de conexão esgotado. Verifique sua conexão."

    except ConnectionError:
        logger.error("Erro de conexão ao listar scans.")
        return False, "Não foi possível conectar ao servidor."

    except Exception as exc:
        logger.error("Erro inesperado ao listar scans: %s", exc)
        return False, "Não foi possível conectar ao servidor."


def buscar_scan_detalhe(scan_id: int) -> tuple[bool, dict | str]:
    try:
        response = api_client.get(f"{_ENDPOINT}/{scan_id}", timeout=_TIMEOUT)

        if response.status_code == 200:
            return True, response.json()

        msg = _mensagem_erro_http(response.status_code, response)
        logger.warning(
            "Falha ao buscar detalhe do scan %d: HTTP %d — %s",
            scan_id, response.status_code, msg,
        )
        return False, msg

    except Timeout:
        logger.error("Timeout ao buscar detalhe do scan %d.", scan_id)
        return False, "Tempo de conexão esgotado. Verifique sua conexão."

    except ConnectionError:
        logger.error("Erro de conexão ao buscar detalhe do scan %d.", scan_id)
        return False, "Não foi possível conectar ao servidor."

    except Exception as exc:
        logger.error("Erro inesperado ao buscar detalhe do scan %d: %s", scan_id, exc)
        return False, "Não foi possível conectar ao servidor."
