package com.ucb.agente_reconhecimento.web.dto.stress;

import java.math.BigDecimal;

public record StressTestCenarioDetalheDTO(
        Integer porta,
        String status,
        BigDecimal latenciaMs
) {
}
