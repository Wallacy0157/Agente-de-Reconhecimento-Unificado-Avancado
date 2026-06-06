package com.ucb.agente_reconhecimento.web.dto.osint;

import java.time.Instant;
import java.util.List;

public record OsintResultadoRequest(
        String alvo,
        String modo,
        Integer totalEncontrado,
        Instant inicio,
        Instant fim,
        List<OsintItemRequest> resultados
) {
}
