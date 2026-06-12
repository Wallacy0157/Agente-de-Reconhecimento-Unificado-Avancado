package com.ucb.agente_reconhecimento.integration;

import com.ucb.agente_reconhecimento.domain.entities.Usuario;
import com.ucb.agente_reconhecimento.repository.TesteStressRepository;
import com.ucb.agente_reconhecimento.repository.UsuarioRepository;
import com.ucb.agente_reconhecimento.web.dto.stress.StressTestCenarioRequest;
import com.ucb.agente_reconhecimento.web.dto.stress.StressTestResultadoRequest;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.http.MediaType;
import org.springframework.test.annotation.DirtiesContext;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.setup.MockMvcBuilders;
import org.springframework.web.context.WebApplicationContext;

import java.math.BigDecimal;
import java.time.Instant;
import java.util.List;

import static org.assertj.core.api.Assertions.assertThat;
import static org.springframework.security.test.web.servlet.request.SecurityMockMvcRequestPostProcessors.jwt;
import static org.springframework.security.test.web.servlet.setup.SecurityMockMvcConfigurers.springSecurity;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.MOCK)
@DirtiesContext(classMode = DirtiesContext.ClassMode.AFTER_EACH_TEST_METHOD)
class StressEndpointIntegrationTest {

    MockMvc mockMvc;

    @Autowired WebApplicationContext webApplicationContext;
    @Autowired UsuarioRepository usuarioRepository;
    @Autowired TesteStressRepository testeStressRepository;
    @Autowired tools.jackson.databind.ObjectMapper objectMapper;

    Usuario usuarioAtivo;

    @BeforeEach
    void setup() {
        mockMvc = MockMvcBuilders.webAppContextSetup(webApplicationContext).apply(springSecurity()).build();
        Usuario u = new Usuario();
        u.setNome("Stress Tester"); u.setEmail("stress@tester.com"); u.setUsername("stress");
        u.setSenhaHash("$2a$10$hash_teste"); u.setAtivo(true);
        usuarioAtivo = usuarioRepository.save(u);
    }

    @Test
    @DisplayName("Deveria inserir métricas de Stress Test no banco de dados e retornar 201")
    void deveriaInserirMetricasStress() throws Exception {
        var cenario = new StressTestCenarioRequest("Carga Maxima", 80, "Timeout", new BigDecimal("1050.5"));
        var payload = new StressTestResultadoRequest(
                "10.0.0.1", 80, 500, 60, 30000, 29000, 1000,
                Instant.now(), Instant.now(), List.of(cenario)
        );

        mockMvc.perform(post("/stress-tests")
                        .with(jwt().jwt(jwt -> jwt.subject(usuarioAtivo.getId().toString())))
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(payload)))
                .andExpect(status().isCreated())
                .andExpect(jsonPath("$.id").exists());

        assertThat(testeStressRepository.findAll()).hasSize(1);
    }
}