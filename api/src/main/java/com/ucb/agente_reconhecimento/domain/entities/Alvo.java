package com.ucb.agente_reconhecimento.domain.entities;

import jakarta.persistence.*;
import lombok.*;

@Builder
@NoArgsConstructor
@AllArgsConstructor
@Getter
@Setter
@Entity
public class Alvo {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer id;

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
