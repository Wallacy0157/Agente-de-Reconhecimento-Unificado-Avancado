package com.ucb.agente_reconhecimento.service;

import com.ucb.agente_reconhecimento.domain.entities.Usuario;
import com.ucb.agente_reconhecimento.domain.entities.UsuarioPreferencia;
import com.ucb.agente_reconhecimento.repository.UsuarioRepository;
import com.ucb.agente_reconhecimento.web.dto.UsuarioCadastroDTO;
import org.springframework.stereotype.Service;

@Service
public class UsuarioService {

    private final UsuarioRepository usuarioRepository;

    public UsuarioService (UsuarioRepository usuarioRepository) {
        this.usuarioRepository = usuarioRepository;
    }

    public void salvarUsuario(UsuarioCadastroDTO usuarioCadastroDTO) {
        if (usuarioRepository.existsByEmail(usuarioCadastroDTO.email())) {
            throw new RuntimeException("Email já cadastrado");
        }

        if (usuarioRepository.existsByUsername(usuarioCadastroDTO.username())) {
            throw new RuntimeException("Username já cadastrado");
        }

        //TODO: Hashar senha quando incluir dependência spring-security

        Usuario novoUsuario = usuarioCadastroDTO.toEntity();
        novoUsuario.setAtivo(true);
        novoUsuario.setUsuarioPreferencia(UsuarioPreferencia.getDefault());

        usuarioRepository.save(novoUsuario);
    }

}
