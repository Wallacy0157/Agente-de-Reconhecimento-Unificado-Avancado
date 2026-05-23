package com.ucb.agente_reconhecimento.domain.entities.keylogger;

import com.ucb.agente_reconhecimento.domain.entities.EntidadeAuditavel;
import com.ucb.agente_reconhecimento.domain.entities.Execucao;
import jakarta.persistence.*;
import lombok.*;

import java.time.LocalDateTime;

@Builder
@NoArgsConstructor
@AllArgsConstructor
@Getter
@Setter
@Entity
public class KeyLogger extends EntidadeAuditavel {

    @ManyToOne(cascade = CascadeType.ALL)
    @JoinColumn(name = "id_execucao")
    private Execucao execucao;

    @Column(name = "inicio", nullable = false)
    private LocalDateTime inicio;

    @Column(name = "termino")
    private LocalDateTime termino;

    @Column(name = "url_arquivo")
    private String urlArquivo;

}
