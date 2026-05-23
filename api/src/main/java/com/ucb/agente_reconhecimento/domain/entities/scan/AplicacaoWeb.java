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
public class AplicacaoWeb extends EntidadeAuditavel {

    @Column(name = "url", nullable = false)
    private String url;
}
