package com.ucb.agente_reconhecimento.web.dto.osint;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Size;

public record OsintItemRequest(
        @NotBlank String site,
        @NotBlank String url,
        @Size(max = 500) String titulo,
        @Size(max = 100) String fonte
) {
}
