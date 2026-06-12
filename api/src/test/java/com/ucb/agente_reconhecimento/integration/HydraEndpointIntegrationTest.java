package com.ucb.agente_reconhecimento.integration;

import com.ucb.agente_reconhecimento.domain.entities.Usuario;
import com.ucb.agente_reconhecimento.repository.HydraAtaqueRepository;
import com.ucb.agente_reconhecimento.repository.UsuarioRepository;
import com.ucb.agente_reconhecimento.web.dto.hydra.HydraCredencialRequest;
import com.ucb.agente_reconhecimento.web.dto.hydra.HydraResultadoRequest;
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

import java.time.Instant;
import java.util.List;

import static org.assertj.core.api.Assertions.assertThat;
import static org.springframework.security.test.web.servlet.request.SecurityMockMvcRequestPostProcessors.jwt;
import static org.springframework.security.test.web.servlet.setup.SecurityMockMvcConfigurers.springSecurity;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.MOCK)
@DirtiesContext(classMode = DirtiesContext.ClassMode.AFTER_EACH_TEST_METHOD)
class HydraEndpointIntegrationTest {

    MockMvc mockMvc;

    @Autowired WebApplicationContext webApplicationContext;
    @Autowired UsuarioRepository usuarioRepository;
    @Autowired HydraAtaqueRepository hydraAtaqueRepository;
    @Autowired tools.jackson.databind.ObjectMapper objectMapper;

    Usuario usuarioAtivo;

    @BeforeEach
    void setup() {
        mockMvc = MockMvcBuilders.webAppContextSetup(webApplicationContext).apply(springSecurity()).build();
        Usuario u = new Usuario();
        u.setNome("Master Chief"); u.setEmail("chief@halo.com"); u.setUsername("john117");
        u.setSenhaHash("$2a$10$hash_teste"); u.setAtivo(true);
        usuarioAtivo = usuarioRepository.save(u);
    }

    private String toJson(Object obj) throws Exception { return objectMapper.writeValueAsString(obj); }

    private HydraResultadoRequest criarPayloadValido() {
        return new HydraResultadoRequest("ssh", 22, "brute-force", true,
                Instant.parse("2026-06-12T10:00:00Z"), Instant.parse("2026-06-12T11:00:00Z"),
                List.of("192.168.1.10"), List.of(new HydraCredencialRequest("root", "123456")));
    }

    @Nested
    @DisplayName("Testes de Erro: GlobalExceptionHandler")
    class TratamentoDeErros {

        @Test
        @DisplayName("Deveria retornar 404 (Not Found) ao buscar um ID que não existe")
        void deveriaRetornar404ParaIdInexistente() throws Exception {
            mockMvc.perform(get("/hydra/9999")
                            .with(jwt().jwt(jwt -> jwt.subject(usuarioAtivo.getId().toString()))))
                    .andExpect(status().isNotFound())
                    .andExpect(jsonPath("$.title").value("Recurso não encontrado"));
        }

        @Test
        @DisplayName("Deveria retornar 400 (Bad Request) com lista de parâmetros inválidos se a porta for nula")
        void deveriaRetornar400ParaPortaNula() throws Exception {
            var payloadInvalido = new HydraResultadoRequest("ssh", null, "brute-force", true,
                    Instant.now(), Instant.now(), List.of("10.0.0.1"), List.of());

            mockMvc.perform(post("/hydra")
                            .with(jwt().jwt(jwt -> jwt.subject(usuarioAtivo.getId().toString())))
                            .contentType(MediaType.APPLICATION_JSON).content(toJson(payloadInvalido)))
                    .andExpect(status().isBadRequest())
                    .andExpect(jsonPath("$.title").value("Parâmetros da requisição inválidos"))
                    .andExpect(jsonPath("$['parametros-invalidos'][0].campo").value("porta"));
        }
    }

    @Nested
    @DisplayName("Caminho Feliz: Integração com BD")
    class IntegracaoSucesso {

        @Test
        @DisplayName("Deveria salvar o relatório do Hydra e mapear as credenciais encontradas")
        void deveriaSalvarRelatorioCompleto() throws Exception {
            mockMvc.perform(post("/hydra")
                            .with(jwt().jwt(jwt -> jwt.subject(usuarioAtivo.getId().toString())))
                            .contentType(MediaType.APPLICATION_JSON)
                            .content(toJson(criarPayloadValido())))
                    .andExpect(status().isCreated())
                    .andExpect(jsonPath("$.id").exists());

            assertThat(hydraAtaqueRepository.findAll()).hasSize(1);
        }
    }
}