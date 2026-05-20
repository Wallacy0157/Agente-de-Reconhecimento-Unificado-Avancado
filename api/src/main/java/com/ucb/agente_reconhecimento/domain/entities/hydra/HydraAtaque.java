package com.ucb.agente_reconhecimento.domain.entities.hydra;

import com.ucb.agente_reconhecimento.domain.entities.Execucao;
import jakarta.persistence.*;
import lombok.*;

@Builder
@NoArgsConstructor
@AllArgsConstructor
@Getter
@Setter
@Entity
public class HydraAtaque {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer id;

    @ManyToOne(cascade = CascadeType.ALL)
    @JoinColumn(name = "id_execucao")
    private Execucao execucao;

    @Column(name = "servico", nullable = false)
    private String servico;

    @Column(name = "porta", nullable = false)
    private Integer porta;

    @Column(name = "tipo_ataque", nullable = false)
    private String tipoAtaque;

    @Column(name = "sucesso")
    private Boolean sucesso;

}
