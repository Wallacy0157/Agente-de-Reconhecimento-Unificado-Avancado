package com.ucb.agente_reconhecimento.service;

import com.ucb.agente_reconhecimento.domain.entities.Usuario;
import com.ucb.agente_reconhecimento.domain.entities.UsuarioPreferencia;
import com.ucb.agente_reconhecimento.infra.exception.ConflitoCadastroException;
import com.ucb.agente_reconhecimento.infra.exception.CredenciaisInvalidasException;
import com.ucb.agente_reconhecimento.infra.exception.SenhasNaoCoincidemException;
import com.ucb.agente_reconhecimento.repository.UsuarioRepository;
import com.ucb.agente_reconhecimento.web.dto.TokenResponse;
import com.ucb.agente_reconhecimento.web.dto.UsuarioCadastroDTO;
import com.ucb.agente_reconhecimento.web.dto.UsuarioLoginDTO;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.security.oauth2.jwt.JwtClaimsSet;
import org.springframework.security.oauth2.jwt.JwtEncoder;
import org.springframework.security.oauth2.jwt.JwtEncoderParameters;
import org.springframework.stereotype.Service;

import java.time.Instant;
import java.util.Objects;

@Service
public class UsuarioService {

    private final UsuarioRepository usuarioRepository;
    private final JwtEncoder jwtEncoder;
    private final PasswordEncoder passwordEncoder;

    public UsuarioService (UsuarioRepository usuarioRepository, JwtEncoder jwtEncoder, PasswordEncoder passwordEncoder) {
        this.usuarioRepository = usuarioRepository;
        this.jwtEncoder = jwtEncoder;
        this.passwordEncoder = passwordEncoder;
    }

    public void salvarUsuario(UsuarioCadastroDTO usuarioCadastroDTO) {
        validarUsuarioDto(usuarioCadastroDTO);

        String senhaHash = passwordEncoder.encode(usuarioCadastroDTO.senha());

        Usuario novoUsuario = usuarioCadastroDTO.toEntity();
        novoUsuario.setSenhaHash(senhaHash);
        novoUsuario.setAtivo(true);
        novoUsuario.setUsuarioPreferencia(UsuarioPreferencia.getDefault());

        usuarioRepository.save(novoUsuario);
    }

    private void validarUsuarioDto(UsuarioCadastroDTO usuarioCadastroDTO) {
        if (!Objects.equals(usuarioCadastroDTO.senha(), usuarioCadastroDTO.confirmaSenha())) {
            throw new SenhasNaoCoincidemException();
        }

        if (usuarioRepository.existsByEmail(usuarioCadastroDTO.email())) {
            throw new ConflitoCadastroException("Email", usuarioCadastroDTO.email());
        }

        if (usuarioRepository.existsByUsername(usuarioCadastroDTO.username())) {
            throw new ConflitoCadastroException("Username", usuarioCadastroDTO.username());
        }
    }

    public TokenResponse autenticarUsuario(UsuarioLoginDTO usuarioLoginDTO) {
        Usuario usuario = usuarioRepository.findByEmail(usuarioLoginDTO.email())
                .orElseThrow(CredenciaisInvalidasException::new);

        if (!passwordEncoder.matches(usuarioLoginDTO.senha(), usuario.getSenhaHash())) {
            throw new CredenciaisInvalidasException();
        }

        Instant agora = Instant.now();
        Instant expiraEm = agora.plusSeconds(60 * 60 * 2);

        JwtClaimsSet claims = JwtClaimsSet.builder()
                .issuer("agente-reconhecimento")
                .notBefore(agora)
                .issuedAt(agora)
                .expiresAt(expiraEm)
                .subject(String.valueOf(usuario.getId()))
                .claim("email", usuario.getEmail())
                .claim("scope", "USUARIO")
                .build();

        String token = jwtEncoder.encode(JwtEncoderParameters.from(claims)).getTokenValue();
        return new TokenResponse(token, expiraEm);
    }
}
