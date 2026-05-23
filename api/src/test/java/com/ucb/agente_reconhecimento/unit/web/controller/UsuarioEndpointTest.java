package com.ucb.agente_reconhecimento.unit.web.controller;

import com.ucb.agente_reconhecimento.service.UsuarioService;
import com.ucb.agente_reconhecimento.web.controller.UsuarioEndpoint;
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
import org.springframework.http.HttpStatus;

import java.time.Instant;

import static org.assertj.core.api.Assertions.*;
import static org.mockito.Mockito.*;

@ExtendWith(MockitoExtension.class)
class UsuarioEndpointTest {

    @Mock
    UsuarioService usuarioService;

    @InjectMocks
    UsuarioEndpoint usuarioEndpoint;

    @Captor
    ArgumentCaptor<UsuarioCadastroDTO> cadastroCaptor;

    @Captor
    ArgumentCaptor<UsuarioLoginDTO> loginCaptor;

    @Nested
    class cadastrarUsuario {

        @Test
        @DisplayName("Deveria delegar o cadastro para UsuarioService")
        void deveriaDelegarCadastroParaService() {
            // Arrange
            var dto = new UsuarioCadastroDTO("João", "joao@email.com", "joao123", "senha123", "senha123");

            // Act
            usuarioEndpoint.cadastrarUsuario(dto);

            // Assert
            verify(usuarioService).salvarUsuario(cadastroCaptor.capture());
            var argumento = cadastroCaptor.getValue();

            assertThat(argumento).isEqualTo(dto);
            verify(usuarioService, times(1)).salvarUsuario(dto);
            verifyNoMoreInteractions(usuarioService);
        }

        @Test
        @DisplayName("Deveria retornar HTTP 200 ao cadastrar com sucesso")
        void deveriaRetornarHttp200AoCadastrar() {
            // Arrange
            var dto = new UsuarioCadastroDTO("Maria", "maria@email.com", "maria99", "abc123", "abc123");

            // Act
            var response = usuarioEndpoint.cadastrarUsuario(dto);

            // Assert
            assertThat(response.getStatusCode()).isEqualTo(HttpStatus.OK);
        }
    }

    @Nested
    class autenticarUsuario {

        @Test
        @DisplayName("Deveria delegar a autenticação para UsuarioService")
        void deveriaDelegarAutenticacaoParaService() {
            // Arrange
            var loginDto = new UsuarioLoginDTO("joao@email.com", "senha123");
            var tokenResponse = new TokenResponse("token_abc", Instant.now().plusSeconds(7200));

            doReturn(tokenResponse).when(usuarioService).autenticarUsuario(loginDto);

            // Act
            usuarioEndpoint.autenticarUsuario(loginDto);

            // Assert
            verify(usuarioService).autenticarUsuario(loginCaptor.capture());
            var argumento = loginCaptor.getValue();

            assertThat(argumento).isEqualTo(loginDto);
            verify(usuarioService, times(1)).autenticarUsuario(loginDto);
            verifyNoMoreInteractions(usuarioService);
        }

        @Test
        @DisplayName("Deveria retornar HTTP 200 com TokenResponse no body")
        void deveriaRetornarHttp200ComToken() {
            // Arrange
            var loginDto = new UsuarioLoginDTO("joao@email.com", "senha123");
            var tokenResponse = new TokenResponse("token_xyz", Instant.now().plusSeconds(7200));

            doReturn(tokenResponse).when(usuarioService).autenticarUsuario(loginDto);

            // Act
            var response = usuarioEndpoint.autenticarUsuario(loginDto);

            // Assert
            assertThat(response.getStatusCode()).isEqualTo(HttpStatus.OK);
            assertThat(response.getBody()).isNotNull();
            assertThat(response.getBody().token()).isEqualTo("token_xyz");
        }
    }
}
