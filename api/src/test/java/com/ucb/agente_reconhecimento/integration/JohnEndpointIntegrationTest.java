package com.ucb.agente_reconhecimento.integration;

import com.ucb.agente_reconhecimento.domain.entities.Usuario;
import com.ucb.agente_reconhecimento.domain.entities.john.JohnTheRipper;
import com.ucb.agente_reconhecimento.repository.UsuarioRepository;
import com.ucb.agente_reconhecimento.service.JohnService;
import com.ucb.agente_reconhecimento.web.dto.john.JohnResultadoRequest;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.bean.override.mockito.MockitoBean;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.setup.MockMvcBuilders;
import org.springframework.web.context.WebApplicationContext;

import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.when;
import static org.springframework.security.test.web.servlet.request.SecurityMockMvcRequestPostProcessors.jwt;
import static org.springframework.security.test.web.servlet.setup.SecurityMockMvcConfigurers.springSecurity;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.MOCK)
class JohnEndpointIntegrationTest {

    MockMvc mockMvc;

    @Autowired WebApplicationContext webApplicationContext;
    @Autowired UsuarioRepository usuarioRepository;
    @Autowired tools.jackson.databind.ObjectMapper objectMapper;

    @MockitoBean JohnService johnService;

    Usuario usuarioAtivo;

    @BeforeEach
    void setup() {
        mockMvc = MockMvcBuilders.webAppContextSetup(webApplicationContext).apply(springSecurity()).build();
        Usuario u = new Usuario();
        u.setNome("John Tester"); u.setEmail("john@tester.com"); u.setUsername("john");
        u.setSenhaHash("$2a$10$hash_teste"); u.setAtivo(true);
        usuarioAtivo = usuarioRepository.save(u);

        JohnTheRipper entity = new JohnTheRipper();
        entity.setId(1);
        when(johnService.salvar(any(), any())).thenReturn(entity);
    }

    @Test
    @DisplayName("Deveria aceitar o DTO válido do John The Ripper e retornar 201 Created")
    void deveriaAceitarRelatorioJohn() throws Exception {
        var payload = new JohnResultadoRequest(
                "5d41402abc4b2a76b9719d911017c592", "MD5", null, "hello",
                "wordlist", 10500, "Concluído"
        );

        mockMvc.perform(post("/john")
                        .with(jwt().jwt(jwt -> jwt.subject(usuarioAtivo.getId().toString())))
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(payload)))
                .andExpect(status().isCreated())
                .andExpect(jsonPath("$.id").value(1));
    }
}