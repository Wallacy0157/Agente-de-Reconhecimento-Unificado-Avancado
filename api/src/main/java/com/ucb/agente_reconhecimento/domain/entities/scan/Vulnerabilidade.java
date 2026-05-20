package com.ucb.agente_reconhecimento.domain.entities.scan;

import com.ucb.agente_reconhecimento.domain.enums.Gravidade;
import jakarta.persistence.*;
import lombok.*;

@Builder
@NoArgsConstructor
@AllArgsConstructor
@Getter
@Setter
@Entity
public class Vulnerabilidade {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer id;

    @ManyToOne(cascade = CascadeType.ALL)
    @JoinColumn(name = "id_porta_aberta")
    private PortaAberta portaAberta;

    @Column(name = "detalhes")
    private String detalhes;

    @Column(name = "cve")
    private String cve;

    @Enumerated(EnumType.STRING)
    private Gravidade gravidade;

    @Column(name = "observacao")
    private String observacao;
}
