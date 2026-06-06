package com.ucb.agente_reconhecimento.web.dto.stress;

import jakarta.validation.Valid;
import jakarta.validation.constraints.Max;
import jakarta.validation.constraints.Min;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Size;

import java.time.Instant;
import java.util.List;

public record StressTestResultadoRequest(
        @NotBlank String ipAlvo,
        @NotNull @Min(1) @Max(65535) Integer portaAlvo,
        @NotNull @Min(1) @Max(100000) Integer rpsLimite,
        @NotNull @Min(1) @Max(3600) Integer duracaoConfiguracao,
        @NotNull @Min(0) Integer totalEnviado,
        @NotNull @Min(0) Integer quantidadeSucesso,
        @NotNull @Min(0) Integer quantidadeErros,
        @NotNull Instant inicio,
        @NotNull Instant fim,
        @NotNull @Size(max = 1000) List<@Valid StressTestCenarioRequest> cenarios
) {
}
