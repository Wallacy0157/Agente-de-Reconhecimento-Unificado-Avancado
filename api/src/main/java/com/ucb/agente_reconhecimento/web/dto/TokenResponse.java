package com.ucb.agente_reconhecimento.web.dto;

import java.time.Instant;

public record TokenResponse(
        String token,
        Instant expiraEm
) {
}
