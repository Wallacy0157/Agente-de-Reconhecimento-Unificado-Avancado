package com.ucb.agente_reconhecimento.domain.entities.firewall;

import com.ucb.agente_reconhecimento.domain.entities.EntidadeAuditavel;
import com.ucb.agente_reconhecimento.domain.entities.Execucao;
import jakarta.persistence.*;
import lombok.*;

@Builder
@NoArgsConstructor
@AllArgsConstructor
@Getter
@Setter
@Entity
public class TesteFirewall extends EntidadeAuditavel {

    @ManyToOne(cascade = CascadeType.ALL)
    @JoinColumn(name = "id_execucao")
    private Execucao execucao;

    @Column(name = "acesso_pasta")
    private String acessoPasta;

    @Column(name = "alvo_pasta")
    private String alvoPasta;

    @Column(name = "abas_abertas")
    private Integer abasAbertas;

    @Column(name = "abas_status")
    private String abasStatus;
}
