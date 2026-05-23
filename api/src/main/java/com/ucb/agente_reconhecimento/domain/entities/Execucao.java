package com.ucb.agente_reconhecimento.domain.entities;

import jakarta.persistence.*;
import lombok.*;
import org.hibernate.annotations.JdbcTypeCode;
import org.hibernate.type.SqlTypes;

import java.time.LocalDateTime;
import java.util.Map;

@Builder
@NoArgsConstructor
@AllArgsConstructor
@Getter
@Setter
@Entity
public class Execucao extends EntidadeAuditavel {

    @ManyToOne(cascade = CascadeType.ALL)
    @JoinColumn(name = "id_projeto")
    private Projeto projeto;

    @ManyToOne(cascade = CascadeType.ALL)
    @JoinColumn(name = "id_ferramenta")
    private Ferramenta ferramenta;

    @Column(nullable = false)
    private String tipo;

    @Column(nullable = false)
    private String status;

    @Column(nullable = false)
    private LocalDateTime inicio;

    @Column(nullable = false)
    private LocalDateTime fim;

    @Column(nullable = false)
    private String gravidade;

    //TODO: Descomentar quando for para produção, pois o h2 não suporta esse tipo de coluna
//    @JdbcTypeCode(SqlTypes.JSON)
//    @Column(columnDefinition = "jsonb")
//    private Map<String, String> parametros;

    @Column(name = "resumo")
    private String resumo;

}
