import logging

from services import api_client

logger = logging.getLogger(__name__)

_ENDPOINT = "/scans"
_TIMEOUT = 30


def enviar_resultado_scan(resultado: dict) -> dict | None:
    try:
        response = api_client.post(_ENDPOINT, resultado, timeout=_TIMEOUT)

        if response.status_code == 201:
            logger.info("Resultado de scan persistido com sucesso no backend.")
            return response.json()

        logger.warning(
            "Falha ao persistir scan: HTTP %d — %s",
            response.status_code,
            response.text[:200],
        )
        return None

    except Exception as exc:
        logger.error("Erro ao enviar resultado de scan ao backend: %s", exc)
        return None
