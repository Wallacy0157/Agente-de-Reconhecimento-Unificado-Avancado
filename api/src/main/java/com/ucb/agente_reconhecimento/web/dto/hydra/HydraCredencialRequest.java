package com.ucb.agente_reconhecimento.web.dto.hydra;

import jakarta.validation.constraints.NotBlank;

public record HydraCredencialRequest(
        @NotBlank String username,
        @NotBlank String password
) {
}
