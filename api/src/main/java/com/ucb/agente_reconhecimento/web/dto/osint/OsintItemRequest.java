package com.ucb.agente_reconhecimento.web.dto.osint;

public record OsintItemRequest(
        String site,
        String url,
        String titulo,
        String fonte
) {
}
