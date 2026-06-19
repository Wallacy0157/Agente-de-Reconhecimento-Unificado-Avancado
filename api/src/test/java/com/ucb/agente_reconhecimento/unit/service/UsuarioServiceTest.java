package com.ucb.agente_reconhecimento.unit.service;

import com.ucb.agente_reconhecimento.domain.entities.Usuario;
import com.ucb.agente_reconhecimento.infra.exception.ConflitoCadastroException;
import com.ucb.agente_reconhecimento.infra.exception.CredenciaisInvalidasException;
import com.ucb.agente_reconhecimento.infra.exception.SenhasNaoCoincidemException;
import com.ucb.agente_reconhecimento.repository.UsuarioRepository;
import com.ucb.agente_reconhecimento.service.UsuarioService;
import com.ucb.agente_reconhecimento.web.dto.TokenResponse;
import com.ucb.agente_reconhecimento.web.dto.UsuarioCadastroDTO;
import com.ucb.agente_reconhecimento.web.dto.UsuarioLoginDTO;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Nested;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.ArgumentCaptor;
import org.mockito.Captor;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.security.oauth2.jwt.Jwt;
import org.springframework.security.oauth2.jwt.JwtEncoder;
import org.springframework.security.oauth2.jwt.JwtEncoderParameters;

import java.time.Instant;
import java.util.Optional;

import static org.assertj.core.api.Assertions.*;
import static org.mockito.Mockito.*;

@ExtendWith(MockitoExtension.class)
class UsuarioServiceTest {

    @Mock
    UsuarioRepository usuarioRepository;

    @Mock
    JwtEncoder jwtEncoder;

    @Mock
    PasswordEncoder passwordEncoder;

    @InjectMocks
    UsuarioService usuarioService;

    @Captor
    ArgumentCaptor<Usuario> usuarioCaptor;

    @Nested
    class salvarUsuario {

        @Test
        @DisplayName("Deveria salvar o usuário com senha codificada e ativo=true")
        void deveriaSalvarUsuarioComSenhaCodificada() {
            // Arrange
            var dto = new UsuarioCadastroDTO("João", "joao@email.com", "joao123", "senha123", "senha123");

            doReturn(false).when(usuarioRepository).existsByEmail(dto.email());
            doReturn(false).when(usuarioRepository).existsByUsername(dto.username());
            doReturn("hash_encoded").when(passwordEncoder).encode(dto.senha());

            // Act
            usuarioService.salvarUsuario(dto);

            // Assert
            verify(usuarioRepository).save(usuarioCaptor.capture());
            var usuarioSalvo = usuarioCaptor.getValue();

            assertThat(usuarioSalvo.getNome()).isEqualTo("João");
            assertThat(usuarioSalvo.getEmail()).isEqualTo("joao@email.com");
            assertThat(usuarioSalvo.getUsername()).isEqualTo("joao123");
            assertThat(usuarioSalvo.getSenhaHash()).isEqualTo("hash_encoded");
            assertThat(usuarioSalvo.isAtivo()).isTrue();
            assertThat(usuarioSalvo.getUsuarioPreferencia()).isNotNull();
        }

        @Test
        @DisplayName("Deveria chamar o save do repository exatamente uma vez")
        void deveriaChamarSaveUmaVez() {
            // Arrange
            var dto = new UsuarioCadastroDTO("Maria", "maria@email.com", "maria99", "abc123", "abc123");

            doReturn(false).when(usuarioRepository).existsByEmail(dto.email());
            doReturn(false).when(usuarioRepository).existsByUsername(dto.username());
            doReturn("hash").when(passwordEncoder).encode(dto.senha());

            // Act
            usuarioService.salvarUsuario(dto);

            // Assert
            verify(usuarioRepository, times(1)).save(any(Usuario.class));
            verify(passwordEncoder, times(1)).encode(dto.senha());
        }

        @Test
        @DisplayName("Deveria lançar SenhasNaoCoincidemException quando senhas divergem")
        void deveriaLancarExcecaoQuandoSenhasNaoCoincidem() {
            // Arrange
            var dto = new UsuarioCadastroDTO("João", "joao@email.com", "joao123", "senha123", "outra456");

            // Act & Assert
            assertThatThrownBy(() -> usuarioService.salvarUsuario(dto))
                    .isInstanceOf(SenhasNaoCoincidemException.class);

            verify(usuarioRepository, never()).save(any());
        }

        @Test
        @DisplayName("Deveria lançar ConflitoCadastroException quando email já existe")
        void deveriaLancarExcecaoQuandoEmailJaExiste() {
            // Arrange
            var dto = new UsuarioCadastroDTO("João", "joao@email.com", "joao123", "senha123", "senha123");

            doReturn(true).when(usuarioRepository).existsByEmail(dto.email());

            // Act & Assert
            assertThatThrownBy(() -> usuarioService.salvarUsuario(dto))
                    .isInstanceOf(ConflitoCadastroException.class);

            verify(usuarioRepository, never()).save(any());
        }

        @Test
        @DisplayName("Deveria lançar ConflitoCadastroException quando username já existe")
        void deveriaLancarExcecaoQuandoUsernameJaExiste() {
            // Arrange
            var dto = new UsuarioCadastroDTO("João", "joao@email.com", "joao123", "senha123", "senha123");

            doReturn(false).when(usuarioRepository).existsByEmail(dto.email());
            doReturn(true).when(usuarioRepository).existsByUsername(dto.username());

            // Act & Assert
            assertThatThrownBy(() -> usuarioService.salvarUsuario(dto))
                    .isInstanceOf(ConflitoCadastroException.class);

            verify(usuarioRepository, never()).save(any());
        }
    }

    @Nested
    class autenticarUsuario {

        @Test
        @DisplayName("Deveria retornar TokenResponse quando credenciais são válidas")
        void deveriaRetornarTokenQuandoCredenciaisValidas() {
            // Arrange
            var loginDto = new UsuarioLoginDTO("joao123", "senha123");

            var usuario = new Usuario();
            usuario.setId(1);
            usuario.setNome("João");
            usuario.setEmail("joao@email.com");
            usuario.setUsername("joao123");
            usuario.setSenhaHash("hash_encoded");

            doReturn(Optional.of(usuario)).when(usuarioRepository).findByUsername(loginDto.username());
            doReturn(true).when(passwordEncoder).matches(loginDto.senha(), usuario.getSenhaHash());

            var jwtMock = mock(Jwt.class);
            doReturn("token_gerado_123").when(jwtMock).getTokenValue();
            doReturn(jwtMock).when(jwtEncoder).encode(any(JwtEncoderParameters.class));

            // Act
            TokenResponse response = usuarioService.autenticarUsuario(loginDto);

            // Assert
            assertThat(response).isNotNull();
            assertThat(response.token()).isEqualTo("token_gerado_123");
            assertThat(response.expiraEm()).isAfter(Instant.now());
        }

        @Test
        @DisplayName("Deveria lançar CredenciaisInvalidasException quando username não existe")
        void deveriaLancarExcecaoQuandoUsernameNaoExiste() {
            // Arrange
            var loginDto = new UsuarioLoginDTO("inexistente", "senha123");

            doReturn(Optional.empty()).when(usuarioRepository).findByUsername(loginDto.username());

            // Act & Assert
            assertThatThrownBy(() -> usuarioService.autenticarUsuario(loginDto))
                    .isInstanceOf(CredenciaisInvalidasException.class);

            verify(jwtEncoder, never()).encode(any());
        }

        @Test
        @DisplayName("Deveria lançar CredenciaisInvalidasException quando senha está incorreta")
        void deveriaLancarExcecaoQuandoSenhaIncorreta() {
            // Arrange
            var loginDto = new UsuarioLoginDTO("joao123", "senha_errada");

            var usuario = new Usuario();
            usuario.setId(1);
            usuario.setNome("João");
            usuario.setEmail("joao@email.com");
            usuario.setUsername("joao123");
            usuario.setSenhaHash("hash_encoded");

            doReturn(Optional.of(usuario)).when(usuarioRepository).findByUsername(loginDto.username());
            doReturn(false).when(passwordEncoder).matches(loginDto.senha(), usuario.getSenhaHash());

            assertThatThrownBy(() -> usuarioService.autenticarUsuario(loginDto))
                    .isInstanceOf(CredenciaisInvalidasException.class);

            verify(jwtEncoder, never()).encode(any());
        }
    }
}