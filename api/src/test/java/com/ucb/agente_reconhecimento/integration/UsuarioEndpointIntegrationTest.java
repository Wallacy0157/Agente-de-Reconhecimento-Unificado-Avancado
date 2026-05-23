package com.ucb.agente_reconhecimento.integration;

import com.ucb.agente_reconhecimento.repository.UsuarioRepository;
import com.ucb.agente_reconhecimento.web.dto.UsuarioCadastroDTO;
import com.ucb.agente_reconhecimento.web.dto.UsuarioLoginDTO;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Nested;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.http.MediaType;
import org.springframework.test.annotation.DirtiesContext;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.setup.MockMvcBuilders;
import org.springframework.web.context.WebApplicationContext;

import static org.assertj.core.api.Assertions.*;
import static org.springframework.security.test.web.servlet.setup.SecurityMockMvcConfigurers.springSecurity;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.MOCK)
@DirtiesContext(classMode = DirtiesContext.ClassMode.AFTER_EACH_TEST_METHOD)
class UsuarioEndpointIntegrationTest {

    MockMvc mockMvc;

    @Autowired
    WebApplicationContext webApplicationContext;

    @Autowired
    UsuarioRepository usuarioRepository;

    @Autowired
    tools.jackson.databind.ObjectMapper objectMapper;

    @BeforeEach
    void setup() {
        mockMvc = MockMvcBuilders
                .webAppContextSetup(webApplicationContext)
                .apply(springSecurity())
                .build();
    }

    private String toJson(Object obj) throws Exception {
        return objectMapper.writeValueAsString(obj);
    }

    private UsuarioCadastroDTO criarCadastroValido() {
        return new UsuarioCadastroDTO(
                "João Silva",
                "joao@email.com",
                "joao123",
                "senha123",
                "senha123"
        );
    }

    private void cadastrarUsuarioPadrao() throws Exception {
        mockMvc.perform(post("/usuarios")
                .contentType(MediaType.APPLICATION_JSON)
                .content(toJson(criarCadastroValido())))
                .andExpect(status().isOk());
    }

    @Nested
    @DisplayName("POST /usuarios - Cadastro")
    class cadastro {

        @Test
        @DisplayName("Deveria cadastrar usuário com sucesso e retornar HTTP 200")
        void deveriaCadastrarComSucesso() throws Exception {
            mockMvc.perform(post("/usuarios")
                            .contentType(MediaType.APPLICATION_JSON)
                            .content(toJson(criarCadastroValido())))
                    .andExpect(status().isOk());

            assertThat(usuarioRepository.existsByEmail("joao@email.com")).isTrue();
            assertThat(usuarioRepository.existsByUsername("joao123")).isTrue();
        }

        @Test
        @DisplayName("Deveria persistir a senha codificada com BCrypt")
        void deveriaPersistirSenhaCodificada() throws Exception {
            cadastrarUsuarioPadrao();

            var usuario = usuarioRepository.findByEmail("joao@email.com").orElseThrow();
            assertThat(usuario.getSenhaHash()).isNotEqualTo("senha123");
            assertThat(usuario.getSenhaHash()).startsWith("$2a$");
        }

        @Test
        @DisplayName("Deveria retornar HTTP 409 ao cadastrar email duplicado")
        void deveriaRetornar409ParaEmailDuplicado() throws Exception {
            cadastrarUsuarioPadrao();

            var duplicado = new UsuarioCadastroDTO(
                    "Outro Nome", "joao@email.com", "outro_user", "abc123", "abc123");

            mockMvc.perform(post("/usuarios")
                            .contentType(MediaType.APPLICATION_JSON)
                            .content(toJson(duplicado)))
                    .andExpect(status().isConflict())
                    .andExpect(jsonPath("$.title").value("Conflito no cadastro"))
                    .andExpect(jsonPath("$.detail").value("Email 'joao@email.com' já está em uso."));
        }

        @Test
        @DisplayName("Deveria retornar HTTP 409 ao cadastrar username duplicado")
        void deveriaRetornar409ParaUsernameDuplicado() throws Exception {
            cadastrarUsuarioPadrao();

            var duplicado = new UsuarioCadastroDTO(
                    "Outro Nome", "outro@email.com", "joao123", "abc123", "abc123");

            mockMvc.perform(post("/usuarios")
                            .contentType(MediaType.APPLICATION_JSON)
                            .content(toJson(duplicado)))
                    .andExpect(status().isConflict())
                    .andExpect(jsonPath("$.title").value("Conflito no cadastro"))
                    .andExpect(jsonPath("$.detail").value("Username 'joao123' já está em uso."));
        }

        @Test
        @DisplayName("Deveria retornar HTTP 400 quando senhas não coincidem")
        void deveriaRetornar400QuandoSenhasNaoCoincidem() throws Exception {
            var dto = new UsuarioCadastroDTO(
                    "João", "joao@email.com", "joao123", "senha123", "outra456");

            mockMvc.perform(post("/usuarios")
                            .contentType(MediaType.APPLICATION_JSON)
                            .content(toJson(dto)))
                    .andExpect(status().isBadRequest())
                    .andExpect(jsonPath("$.title").value("Validação de senha"))
                    .andExpect(jsonPath("$.detail").value("As senhas informadas não coincidem."));
        }

        @Test
        @DisplayName("Deveria retornar HTTP 400 com parametros-invalidos quando campos obrigatórios estão vazios")
        void deveriaRetornar400ParaCamposVazios() throws Exception {
            var dto = new UsuarioCadastroDTO("", "", "", "", "");

            mockMvc.perform(post("/usuarios")
                            .contentType(MediaType.APPLICATION_JSON)
                            .content(toJson(dto)))
                    .andExpect(status().isBadRequest())
                    .andExpect(jsonPath("$.title").value("Parâmetros da requisição inválidos"))
                    .andExpect(jsonPath("$.parametros-invalidos").isArray())
                    .andExpect(jsonPath("$.parametros-invalidos").isNotEmpty());
        }
    }

    @Nested
    @DisplayName("POST /usuarios/login - Autenticação")
    class login {

        @Test
        @DisplayName("Deveria autenticar com sucesso e retornar token JWT")
        void deveriaAutenticarComSucesso() throws Exception {
            cadastrarUsuarioPadrao();

            var loginDto = new UsuarioLoginDTO("joao@email.com", "senha123");

            mockMvc.perform(post("/usuarios/login")
                            .contentType(MediaType.APPLICATION_JSON)
                            .content(toJson(loginDto)))
                    .andExpect(status().isOk())
                    .andExpect(jsonPath("$.token").isNotEmpty())
                    .andExpect(jsonPath("$.expiraEm").isNotEmpty());
        }

        @Test
        @DisplayName("Deveria retornar HTTP 401 quando email não existe")
        void deveriaRetornar401ParaEmailInexistente() throws Exception {
            var loginDto = new UsuarioLoginDTO("inexistente@email.com", "senha123");

            mockMvc.perform(post("/usuarios/login")
                            .contentType(MediaType.APPLICATION_JSON)
                            .content(toJson(loginDto)))
                    .andExpect(status().isUnauthorized())
                    .andExpect(jsonPath("$.title").value("Falha na autenticação"))
                    .andExpect(jsonPath("$.detail").value("Email ou senha incorretos."));
        }

        @Test
        @DisplayName("Deveria retornar HTTP 401 quando senha está incorreta")
        void deveriaRetornar401ParaSenhaIncorreta() throws Exception {
            cadastrarUsuarioPadrao();

            var loginDto = new UsuarioLoginDTO("joao@email.com", "senha_errada");

            mockMvc.perform(post("/usuarios/login")
                            .contentType(MediaType.APPLICATION_JSON)
                            .content(toJson(loginDto)))
                    .andExpect(status().isUnauthorized())
                    .andExpect(jsonPath("$.title").value("Falha na autenticação"))
                    .andExpect(jsonPath("$.detail").value("Email ou senha incorretos."));
        }
    }
}
