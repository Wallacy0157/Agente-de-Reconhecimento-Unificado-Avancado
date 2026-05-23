package com.ucb.agente_reconhecimento.web.dto.scan;

import java.util.List;

public record HostDetalheDTO(
        Integer id,
        String ip,
        String os,
        String error,
        boolean temWeb,
        boolean temDatabase,
        boolean temAcessoRemoto,
        boolean temServicoAuth,
        List<PortaDTO> openPorts,
        List<VulnerabilidadeDTO> vulnerabilities,
        List<String> suggestedTests
) {
}
