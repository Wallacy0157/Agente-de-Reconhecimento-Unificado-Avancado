package com.ucb.agente_reconhecimento.domain.entities;

import jakarta.persistence.*;
import lombok.*;

@Builder
@NoArgsConstructor
@AllArgsConstructor
@Getter
@Setter
@Entity
public class Alvo extends EntidadeAuditavel {

    @ManyToOne(cascade = CascadeType.ALL)
    @JoinColumn(name = "id_projeto")
    private Projeto projeto;

    @Column(nullable = false)
    private String tipo;

    @Column(nullable = false)
    private String valor;

    @Column(nullable = false)
    private String descricao;

}
