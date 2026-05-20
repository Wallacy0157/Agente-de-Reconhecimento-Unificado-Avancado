package com.ucb.agente_reconhecimento.domain.entities.hydra;

import jakarta.persistence.*;
import lombok.*;

@Builder
@NoArgsConstructor
@AllArgsConstructor
@Getter
@Setter
@Entity
public class HydraCredencialEncontrada {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer id;

    @ManyToOne(cascade = CascadeType.ALL)
    @JoinColumn(name = "id_ataque_hydra")
    private HydraAtaque hydraAtaque;

    @Column(name = "username")
    private String username;

    @Column(name = "password")
    private String password;
}
