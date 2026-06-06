package com.ucb.agente_reconhecimento.web.dto.stress;

import jakarta.validation.constraints.DecimalMin;
import jakarta.validation.constraints.Max;
import jakarta.validation.constraints.Min;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Size;

import java.math.BigDecimal;

public record StressTestCenarioRequest(
        @NotBlank String nome,
        @NotNull @Min(1) @Max(65535) Integer porta,
        @Size(max = 50) String status,
        @NotNull @DecimalMin("0") BigDecimal latenciaP95Ms
) {
}
