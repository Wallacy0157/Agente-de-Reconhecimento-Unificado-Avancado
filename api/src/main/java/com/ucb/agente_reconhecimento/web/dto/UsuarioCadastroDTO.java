package com.ucb.agente_reconhecimento.web.dto;

import com.ucb.agente_reconhecimento.domain.entities.Usuario;

import static java.util.Optional.ofNullable;

public record UsuarioCadastroDTO (
        String nome,
        String email,
        String username,
        String senha
) {

    public Usuario toEntity() {
        Usuario usuario = new Usuario();

        usuario.setNome(ofNullable(nome()).map(String::trim).orElse(null));
        usuario.setEmail(ofNullable(email()).map(String::trim).orElse(null));
        usuario.setUsername(ofNullable(username()).map(String::trim).orElse(null));
        usuario.setSenhaHash(senha());

        return usuario;
    }
}
