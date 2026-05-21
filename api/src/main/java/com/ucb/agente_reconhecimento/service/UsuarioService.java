package com.ucb.agente_reconhecimento.service;

import com.ucb.agente_reconhecimento.domain.entities.Usuario;
import com.ucb.agente_reconhecimento.domain.entities.UsuarioPreferencia;
import com.ucb.agente_reconhecimento.repository.UsuarioRepository;
import com.ucb.agente_reconhecimento.web.dto.UsuarioCadastroDTO;
import com.ucb.agente_reconhecimento.web.dto.UsuarioLoginDTO;
import org.springframework.stereotype.Service;

import java.util.Objects;

@Service
public class UsuarioService {

    private final UsuarioRepository usuarioRepository;

    public UsuarioService (UsuarioRepository usuarioRepository) {
        this.usuarioRepository = usuarioRepository;
    }

    public void salvarUsuario(UsuarioCadastroDTO usuarioCadastroDTO) {
        validarUsuarioDto(usuarioCadastroDTO);

        //TODO: Hashar senha quando incluir dependência spring-security

        Usuario novoUsuario = usuarioCadastroDTO.toEntity();
        novoUsuario.setAtivo(true);
        novoUsuario.setUsuarioPreferencia(UsuarioPreferencia.getDefault());

        usuarioRepository.save(novoUsuario);
    }

    private void validarUsuarioDto(UsuarioCadastroDTO usuarioCadastroDTO) {
        if (!Objects.equals(usuarioCadastroDTO.senha(), usuarioCadastroDTO.confirmaSenha())) {
            throw new RuntimeException("Senhas não coincidem");
        }

        if (usuarioRepository.existsByEmail(usuarioCadastroDTO.email())) {
            throw new RuntimeException("Email já cadastrado");
        }

        if (usuarioRepository.existsByUsername(usuarioCadastroDTO.username())) {
            throw new RuntimeException("Username já cadastrado");
        }
    }

    public void autenticarUsuario(UsuarioLoginDTO usuarioLoginDTO) {
        //TODO: Comparar senha em texto puro com hash ao criar feature de hash de senha

        Usuario usuario = usuarioRepository.findByEmail(usuarioLoginDTO.email()).orElseThrow();

        if (!Objects.equals(usuario.getSenhaHash(), usuarioLoginDTO.senha())) {
            throw new RuntimeException("Credenciais inválidas");
        }

        //TODO: Retornar Token JWT quando implementado a lógica do spring-security
    }
}
