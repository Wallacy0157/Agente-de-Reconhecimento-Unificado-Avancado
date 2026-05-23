package com.ucb.agente_reconhecimento.web.dto;

import com.ucb.agente_reconhecimento.domain.entities.Usuario;
import jakarta.validation.constraints.Email;
import jakarta.validation.constraints.Min;
import jakarta.validation.constraints.NotBlank;

import static java.util.Optional.ofNullable;

public record UsuarioCadastroDTO (
        String nome,
        @Email
        @NotBlank
        String email,
        @NotBlank
        String username,
        @Min(value = 6)
        @NotBlank
        String senha,
        @Min(value = 6)
        @NotBlank
        String confirmaSenha
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
