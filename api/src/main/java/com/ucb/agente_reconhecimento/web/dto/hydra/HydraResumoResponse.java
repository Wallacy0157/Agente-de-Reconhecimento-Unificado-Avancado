package com.ucb.agente_reconhecimento.web.dto.hydra;

import java.time.LocalDateTime;

public record HydraResumoResponse(
        Integer id,
        String servico,
        Integer porta,
        String tipoAtaque,
        Boolean sucesso,
        Integer totalAlvos,
        Integer totalCredenciais,
        LocalDateTime criadoEm
) {
}
