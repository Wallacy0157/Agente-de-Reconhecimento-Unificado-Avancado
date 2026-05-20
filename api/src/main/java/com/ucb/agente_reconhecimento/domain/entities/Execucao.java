package com.ucb.agente_reconhecimento.domain.entities;

import jakarta.persistence.*;
import lombok.*;
import org.hibernate.annotations.JdbcTypeCode;
import org.hibernate.type.SqlTypes;

import java.util.Map;

@Builder
@NoArgsConstructor
@AllArgsConstructor
@Getter
@Setter
@Entity
public class Execucao {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer id;

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
    private String inicio;

    @Column(nullable = false)
    private String fim;

    @Column(nullable = false)
    private String gravidade;

    @JdbcTypeCode(SqlTypes.JSON)
    @Column(columnDefinition = "jsonb")
    private Map<String, String> parametros;

    @Column(name = "resumo")
    private String resumo;

}
