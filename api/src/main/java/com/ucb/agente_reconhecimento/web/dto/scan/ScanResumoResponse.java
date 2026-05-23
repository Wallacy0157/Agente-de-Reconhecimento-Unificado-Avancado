package com.ucb.agente_reconhecimento.web.dto.scan;

public record ScanResumoResponse(
        Integer id,
        String scanDate,
        String scanTime,
        int totalHosts,
        int totalVulnerabilities,
        String status
) {
}
