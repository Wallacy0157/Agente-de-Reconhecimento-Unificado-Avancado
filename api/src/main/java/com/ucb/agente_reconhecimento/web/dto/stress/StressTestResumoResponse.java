package com.ucb.agente_reconhecimento.web.dto.stress;

import java.time.LocalDateTime;

public record StressTestResumoResponse(
        Integer id,
        String ipAlvo,
        Integer portaAlvo,
        Integer rpsLimite,
        Integer duracaoConfiguracao,
        Integer totalEnviado,
        Integer quantidadeSucesso,
        Integer quantidadeErros,
        LocalDateTime criadoEm
) {
}
