package com.ucb.agente_reconhecimento.web.dto.stress;

import java.time.LocalDateTime;
import java.util.List;

public record StressTestDetalheResponse(
        Integer id,
        String ipAlvo,
        Integer portaAlvo,
        Integer rpsLimite,
        Integer duracaoConfiguracao,
        Integer totalEnviado,
        Integer quantidadeSucesso,
        Integer quantidadeErros,
        LocalDateTime criadoEm,
        List<StressTestCenarioDetalheDTO> cenarios
) {
}
