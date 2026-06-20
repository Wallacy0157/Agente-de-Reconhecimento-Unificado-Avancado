package com.ucb.agente_reconhecimento.web.dto.keylogger;

import java.time.LocalDateTime;

public record KeyloggerResultadoRequest(
        LocalDateTime inicio,
        LocalDateTime termino,
        String urlArquivo,
        String textoBruto
) {}