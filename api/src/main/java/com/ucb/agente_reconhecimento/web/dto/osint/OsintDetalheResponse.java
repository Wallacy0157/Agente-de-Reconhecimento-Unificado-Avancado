package com.ucb.agente_reconhecimento.web.dto.osint;

import java.time.LocalDateTime;
import java.util.List;

public record OsintDetalheResponse(
        Integer id,
        String alvo,
        String modo,
        Integer totalEncontrado,
        LocalDateTime criadoEm,
        List<OsintItemDetalheDTO> resultados
) {
}
