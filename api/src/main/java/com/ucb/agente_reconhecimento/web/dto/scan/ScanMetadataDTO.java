package com.ucb.agente_reconhecimento.web.dto.scan;

public record ScanMetadataDTO(
        String scanDate,
        String scanTime,
        String timezone
) {
}
