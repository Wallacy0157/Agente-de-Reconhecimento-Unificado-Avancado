package com.ucb.agente_reconhecimento.web.dto.scan;

import jakarta.validation.constraints.NotEmpty;

import java.util.List;

public record ScanResultadoRequest(
        ScanMetadataDTO metadata,
        @NotEmpty List<HostResultDTO> results
) {
}
