package com.ucb.agente_reconhecimento.domain.entities;

import com.ucb.agente_reconhecimento.domain.enums.Disponibilidade;
import jakarta.persistence.*;
import lombok.*;

import java.time.LocalDateTime;

@Builder
@NoArgsConstructor
@AllArgsConstructor
@Getter
@Setter
@Entity
public class Ferramenta {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer id;

    @Column(nullable = false, length = 50)
    private String nome;

    @Column(nullable = false)
    private String descricao;

    @Enumerated(EnumType.STRING)
    @Column(nullable = false)
    private Disponibilidade disponibilidade;

    private LocalDateTime verificadoEm;
}
