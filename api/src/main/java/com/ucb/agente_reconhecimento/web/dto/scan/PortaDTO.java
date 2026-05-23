package com.ucb.agente_reconhecimento.web.dto.scan;

public record PortaDTO(
        Integer port,
        String protocol,
        String service
) {
}
