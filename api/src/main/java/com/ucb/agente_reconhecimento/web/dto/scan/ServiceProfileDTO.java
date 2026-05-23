package com.ucb.agente_reconhecimento.web.dto.scan;

public record ServiceProfileDTO(
        boolean web,
        boolean database,
        boolean remoteAccess,
        boolean authService
) {
}
