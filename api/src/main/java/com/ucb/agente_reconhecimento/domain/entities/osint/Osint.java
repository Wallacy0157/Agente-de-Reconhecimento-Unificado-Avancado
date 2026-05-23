package com.ucb.agente_reconhecimento.domain.entities.osint;

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
public class Osint extends EntidadeAuditavel {

    @ManyToOne(cascade = CascadeType.ALL)
    @JoinColumn(name = "id_execucao")
    private Execucao execucao;

    @Column(name = "alvo", nullable = false)
    private String alvo;

    @Column(name = "modo", nullable = false)
    private String modo;

    @Column(name = "total_encontrado")
    private Integer totalEncontrado;
}
