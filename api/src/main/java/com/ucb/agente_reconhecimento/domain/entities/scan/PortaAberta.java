package com.ucb.agente_reconhecimento.domain.entities.scan;

import com.ucb.agente_reconhecimento.domain.entities.EntidadeAuditavel;
import jakarta.persistence.*;
import lombok.*;

@Builder
@NoArgsConstructor
@AllArgsConstructor
@Getter
@Setter
@Entity
public class PortaAberta extends EntidadeAuditavel {

    @ManyToOne(cascade = CascadeType.ALL)
    @JoinColumn(name = "id_host_descoberto")
    private HostDescoberto hostDescoberto;

    @Column(name = "porta")
    private Integer porta;

    @Column(name = "protocolo")
    private String protocolo;

    @Column(name = "servico")
    private String servico;
}
