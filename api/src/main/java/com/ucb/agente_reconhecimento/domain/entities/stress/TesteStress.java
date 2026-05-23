package com.ucb.agente_reconhecimento.domain.entities.stress;

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
public class TesteStress extends EntidadeAuditavel {

    @ManyToOne(cascade = CascadeType.ALL)
    @JoinColumn(name = "id_execucao")
    private Execucao execucao;

    @Column(name = "ip_alvo", nullable = false)
    private String ipAlvo;

    @Column(name = "porta_alvo")
    private Integer portaAlvo;

    @Column(name = "rps_limite")
    private Integer rpsLimite;

    @Column(name = "duracao_configuracao")
    private Integer duracaoConfiguracao;

    @Column(name = "total_enviado")
    private Integer totalEnviado;

    @Column(name = "quantidade_sucesso")
    private Integer quantidadeSucesso;

    @Column(name = "quantidade_erros")
    private Integer quantidadeErros;

}
