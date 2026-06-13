package com.ucb.agente_reconhecimento.web.dto.keylogger;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;

import java.time.LocalDateTime;

public record KeyloggerResultadoRequest(
        @NotNull LocalDateTime inicio,
        @NotNull LocalDateTime termino,
        String urlArquivo,
        @NotBlank String textoBruto
) {}