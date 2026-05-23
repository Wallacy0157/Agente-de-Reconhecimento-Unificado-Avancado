package com.ucb.agente_reconhecimento.web.dto.scan;

import java.util.List;

public record HostResultDTO(
        String ip,
        String os,
        String error,
        List<PortaDTO> openPorts,
        ServiceProfileDTO serviceProfile,
        List<VulnerabilidadeDTO> vulnerabilities,
        List<String> suggestedTests
) {
}
