package com.ucb.agente_reconhecimento.domain.entities.hydra;

import jakarta.persistence.*;
import lombok.*;

@Builder
@NoArgsConstructor
@AllArgsConstructor
@Getter
@Setter
@Entity
public class HydraAlvo {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer id;

    @ManyToOne(cascade = CascadeType.ALL)
    @JoinColumn(name = "id_ataque_hydra")
    private HydraAtaque hydraAtaque;

    @Column(name = "ip", nullable = false)
    private Integer ip;

}
