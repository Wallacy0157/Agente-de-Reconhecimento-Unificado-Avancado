package com.ucb.agente_reconhecimento.domain.entities;

import jakarta.persistence.*;
import lombok.*;

import java.time.LocalDateTime;

@Builder
@NoArgsConstructor
@AllArgsConstructor
@Getter
@Setter
@Entity
public class Usuario extends EntidadeAuditavel {

    @OneToOne(cascade = CascadeType.ALL)
    @JoinColumn(name = "id_usuario_preferencia")
    private UsuarioPreferencia usuarioPreferencia;

    @Column(nullable = false, length = 150)
    private String nome;

    @Column(nullable = false, unique = true)
    private String email;

    @Column(nullable = false, unique = true)
    private String username;

    @Column(nullable = false)
    private String senhaHash;

    @Column(nullable = false)
    private boolean ativo;

    private LocalDateTime ultimoLogin;
}
