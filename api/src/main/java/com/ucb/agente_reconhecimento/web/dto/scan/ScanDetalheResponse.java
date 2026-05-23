package com.ucb.agente_reconhecimento.web.dto.scan;

import java.util.List;

public record ScanDetalheResponse(
        Integer id,
        ScanMetadataDTO metadata,
        List<HostDetalheDTO> hosts
) {
}
