package com.ucb.agente_reconhecimento.web.dto.hydra;

import java.time.LocalDateTime;
import java.util.List;

public record HydraDetalheResponse(
        Integer id,
        String servico,
        Integer porta,
        String tipoAtaque,
        Boolean sucesso,
        LocalDateTime criadoEm,
        List<String> alvos,
        List<HydraCredencialDTO> credenciaisEncontradas
) {
}
