package com.ucb.agente_reconhecimento.web.dto.osint;

import java.time.LocalDateTime;

public record OsintResumoResponse(
        Integer id,
        String alvo,
        String modo,
        Integer totalEncontrado,
        LocalDateTime criadoEm
) {
}
