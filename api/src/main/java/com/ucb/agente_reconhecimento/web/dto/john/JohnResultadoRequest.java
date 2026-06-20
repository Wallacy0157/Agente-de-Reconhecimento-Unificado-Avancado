package com.ucb.agente_reconhecimento.web.dto.john;

public record JohnResultadoRequest(
        String hashAlvo,
        String algoritmo,
        String salt,
        String senhaEncontrada,
        String modoAtaque,
        Integer hashesTestados,
        String status
) {}