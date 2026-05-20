package com.ucb.agente_reconhecimento.domain.entities.stress;

import jakarta.persistence.*;
import lombok.*;

import java.math.BigDecimal;

@Builder
@NoArgsConstructor
@AllArgsConstructor
@Getter
@Setter
@Entity
public class TesteStressRequisicao {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer id;

    @ManyToOne(cascade = CascadeType.ALL)
    @JoinColumn(name = "id_teste_stress")
    private TesteStress testeStress;

    @Column(name = "porta", nullable = false)
    private Integer porta;

    @Column(name = "status")
    private String status;

    @Column(name = "latencia_ms")
    private BigDecimal latenciaMs;
}
