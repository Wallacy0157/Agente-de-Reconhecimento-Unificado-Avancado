package com.ucb.agente_reconhecimento.domain.entities;

import jakarta.persistence.*;
import lombok.*;

@Builder
@NoArgsConstructor
@AllArgsConstructor
@Getter
@Setter
@Entity
public class UsuarioPreferencia {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer id;

    @OneToOne(mappedBy = "usuarioPreferencia")
    @JoinColumn(name = "id_usuario", nullable = false)
    private Usuario usuario;

    @Column(nullable = false)
    private String idioma;

    @Column(nullable = false)
    private String tema;

    @Column(nullable = false)
    private String corNeon;

}
