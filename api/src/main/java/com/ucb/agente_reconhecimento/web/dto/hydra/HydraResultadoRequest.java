package com.ucb.agente_reconhecimento.web.dto.hydra;

import jakarta.validation.Valid;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Size;

import java.time.Instant;
import java.util.List;

public record HydraResultadoRequest(
        @NotBlank String servico,
        @NotNull Integer porta,
        @NotBlank String tipoAtaque,
        @NotNull Boolean sucesso,
        @NotNull Instant inicio,
        @NotNull Instant fim,
        @NotNull @Size(min = 1, max = 100) List<String> alvos,
        @Size(max = 500) List<@Valid HydraCredencialRequest> credenciaisEncontradas
) {
}
