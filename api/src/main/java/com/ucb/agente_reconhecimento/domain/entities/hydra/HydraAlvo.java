package com.ucb.agente_reconhecimento.domain.entities.hydra;

import com.ucb.agente_reconhecimento.domain.entities.EntidadeAuditavel;
import jakarta.persistence.*;
import lombok.*;

@Builder
@NoArgsConstructor
@AllArgsConstructor
@Getter
@Setter
@Entity
public class HydraAlvo extends EntidadeAuditavel {

    @ManyToOne(cascade = CascadeType.ALL)
    @JoinColumn(name = "id_ataque_hydra")
    private HydraAtaque hydraAtaque;

    @Column(name = "ip", nullable = false)
    private String ip;

}
