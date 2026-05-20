package com.ucb.agente_reconhecimento.domain.entities.osint;

import jakarta.persistence.*;
import lombok.*;

@Builder
@NoArgsConstructor
@AllArgsConstructor
@Getter
@Setter
@Entity
public class OsintResultado {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer id;

    @ManyToOne(cascade = CascadeType.ALL)
    @JoinColumn(name = "id_investigacao_osint")
    private Osint osint;

    @Column(name = "site")
    private String site;

    @Column(name = "url")
    private String url;

    @Column(name = "titulo")
    private String titulo;

    @Column(name = "fonte")
    private String fonte;
}
