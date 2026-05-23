package com.ucb.agente_reconhecimento.domain.entities.scan;

import com.ucb.agente_reconhecimento.domain.entities.EntidadeAuditavel;
import com.ucb.agente_reconhecimento.domain.entities.Ferramenta;
import jakarta.persistence.*;
import lombok.*;

@Builder
@NoArgsConstructor
@AllArgsConstructor
@Getter
@Setter
@Entity
public class SugestaoTeste extends EntidadeAuditavel {

    @ManyToOne(cascade = CascadeType.ALL)
    @JoinColumn(name = "id_host_descoberto")
    private HostDescoberto hostDescoberto;

    @ManyToOne(cascade = CascadeType.ALL)
    @JoinColumn(name = "id_ferramenta_sugerida")
    private Ferramenta ferramentaSugerida;

    @Column(name = "motivo")
    private String motivo;
}
