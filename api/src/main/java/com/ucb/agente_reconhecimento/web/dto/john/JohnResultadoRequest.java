package com.ucb.agente_reconhecimento.web.dto.john;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;

public record JohnResultadoRequest(
        @NotBlank String hashAlvo,
        @NotBlank String algoritmo,
        String salt,
        String senhaEncontrada,
        @NotBlank String modoAtaque,
        @NotNull Integer hashesTestados,
        @NotBlank String status
) {}