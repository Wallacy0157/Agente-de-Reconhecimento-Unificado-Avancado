import logging

from services import api_client

logger = logging.getLogger(__name__)

_ENDPOINT = "/osint"
_TIMEOUT = 30


def enviar_resultado_osint(resultado: dict) -> dict | None:
    """Envia resultado da investigação OSINT ao backend. Retorna resposta ou None em caso de falha."""
    try:
        response = api_client.post(_ENDPOINT, resultado, timeout=_TIMEOUT)

        if response.status_code == 201:
            logger.info("Resultado OSINT persistido com sucesso no backend.")
            return response.json()

        logger.warning(
            "Falha ao persistir OSINT: HTTP %d — %s",
            response.status_code,
            response.text[:200],
        )
        return None

    except Exception as exc:
        logger.error("Erro ao enviar resultado OSINT ao backend: %s", exc)
        return None
