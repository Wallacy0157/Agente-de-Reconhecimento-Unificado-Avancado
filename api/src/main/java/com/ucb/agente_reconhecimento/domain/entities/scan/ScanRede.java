package com.ucb.agente_reconhecimento.domain.entities.scan;

import com.ucb.agente_reconhecimento.domain.entities.EntidadeAuditavel;
import com.ucb.agente_reconhecimento.domain.entities.Execucao;
import jakarta.persistence.*;
import lombok.*;

@Builder
@NoArgsConstructor
@AllArgsConstructor
@Getter
@Setter
@Entity
public class ScanRede extends EntidadeAuditavel {

    @ManyToOne(cascade = CascadeType.ALL)
    @JoinColumn(name = "id_execucao")
    private Execucao execucao;
}
