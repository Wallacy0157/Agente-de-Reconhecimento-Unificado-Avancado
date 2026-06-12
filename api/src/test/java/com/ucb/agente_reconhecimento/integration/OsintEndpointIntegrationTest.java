package com.ucb.agente_reconhecimento.integration;

import com.ucb.agente_reconhecimento.domain.entities.Usuario;
import com.ucb.agente_reconhecimento.repository.OsintRepository;
import com.ucb.agente_reconhecimento.repository.UsuarioRepository;
import com.ucb.agente_reconhecimento.web.dto.osint.OsintItemRequest;
import com.ucb.agente_reconhecimento.web.dto.osint.OsintResultadoRequest;
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
class OsintEndpointIntegrationTest {

    MockMvc mockMvc;

    @Autowired WebApplicationContext webApplicationContext;
    @Autowired UsuarioRepository usuarioRepository;
    @Autowired OsintRepository osintRepository;
    @Autowired tools.jackson.databind.ObjectMapper objectMapper;

    Usuario usuarioAtivo;

    @BeforeEach
    void setup() {
        mockMvc = MockMvcBuilders.webAppContextSetup(webApplicationContext).apply(springSecurity()).build();
        Usuario u = new Usuario();
        u.setNome("Sherlock Holmes"); u.setEmail("sherlock@osint.com"); u.setUsername("sherlock");
        u.setSenhaHash("$2a$10$hash_teste"); u.setAtivo(true);
        usuarioAtivo = usuarioRepository.save(u);
    }

    @Test
    @DisplayName("Deveria salvar a varredura do OSINT Sherlock com os links descobertos (201)")
    void deveriaSalvarVarreduraOsint() throws Exception {
        var item = new OsintItemRequest("GitHub", "https://github.com/wallacy0157", "Perfil GitHub", "sherlock");
        var payload = new OsintResultadoRequest("wallacy0157", "full", 1, Instant.now(), Instant.now(), List.of(item));

        mockMvc.perform(post("/osint")
                        .with(jwt().jwt(jwt -> jwt.subject(usuarioAtivo.getId().toString())))
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(payload)))
                .andExpect(status().isCreated())
                .andExpect(jsonPath("$.id").exists());

        assertThat(osintRepository.findAll()).hasSize(1);
    }
}