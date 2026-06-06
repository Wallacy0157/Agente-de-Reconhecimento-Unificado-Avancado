package com.ucb.agente_reconhecimento.web.dto.osint;

import jakarta.validation.Valid;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Size;

import java.time.Instant;
import java.util.List;

public record OsintResultadoRequest(
        @NotBlank String alvo,
        @NotBlank String modo,
        @NotNull Integer totalEncontrado,
        @NotNull Instant inicio,
        @NotNull Instant fim,
        @NotNull @Size(max = 500) List<@Valid OsintItemRequest> resultados
) {
}
