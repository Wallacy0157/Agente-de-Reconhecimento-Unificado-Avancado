package com.ucb.agente_reconhecimento.integration;

import com.ucb.agente_reconhecimento.domain.entities.Usuario;
import com.ucb.agente_reconhecimento.repository.ScanRedeRepository;
import com.ucb.agente_reconhecimento.repository.UsuarioRepository;
import com.ucb.agente_reconhecimento.web.dto.scan.*;
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
import com.jayway.jsonpath.JsonPath;

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
class ScanEndpointIntegrationTest {

    MockMvc mockMvc;

    @Autowired
    WebApplicationContext webApplicationContext;

    @Autowired
    UsuarioRepository usuarioRepository;

    @Autowired
    ScanRedeRepository scanRedeRepository;

    @Autowired
    tools.jackson.databind.ObjectMapper objectMapper;

    Usuario usuarioAtivo;

    @BeforeEach
    void setup() {
        mockMvc = MockMvcBuilders
                .webAppContextSetup(webApplicationContext)
                .apply(springSecurity())
                .build();

       
        Usuario u = new Usuario();
        u.setNome("Master Chief");
        u.setEmail("chief@halo.com");
        u.setUsername("john117");
        u.setSenhaHash("$2a$10$hash_falso_apenas_para_teste");
        u.setAtivo(true);
        usuarioAtivo = usuarioRepository.save(u);
    }

    private String toJson(Object obj) throws Exception {
        return objectMapper.writeValueAsString(obj);
    }

    private ScanResultadoRequest criarPayloadValido() {
        var metadata = new ScanMetadataDTO("2026-06-12", "15:30:00", "America/Sao_Paulo");
        var porta = new PortaDTO(80, "tcp", "http");
        var vuln = new VulnerabilidadeDTO("80", "vulners", "VULNERABLE: CVE-2021-1234");
        var host = new HostResultDTO(
                "192.168.1.100",
                "Linux 5.x",
                "Nenhum erro",
                List.of(porta),
                new ServiceProfileDTO(true, false, false, false),
                List.of("Nikto"),
                List.of(vuln)
        );
        return new ScanResultadoRequest(metadata, List.of(host));
    }

    @Nested
    @DisplayName("Filtro de Segurança (JWT)")
    class Seguranca {

        @Test
        @DisplayName("Deveria bloquear acesso (401 Unauthorized) se não for enviado token JWT")
        void deveriaBloquearAcessoSemToken() throws Exception {
            mockMvc.perform(post("/scans")
                            .contentType(MediaType.APPLICATION_JSON)
                            .content(toJson(criarPayloadValido())))
                    .andExpect(status().isUnauthorized());
        }
    }

    @Nested
    @DisplayName("POST /scans - Inserção de Relatório")
    class CriarScan {

        @Test
        @DisplayName("Deveria realizar o Insert completo no banco e retornar 201 Created")
        void deveriaSalvarScanRetornar201() throws Exception {
            mockMvc.perform(post("/scans")
                            .with(jwt().jwt(jwt -> jwt.subject(usuarioAtivo.getId().toString())))
                            .contentType(MediaType.APPLICATION_JSON)
                            .content(toJson(criarPayloadValido())))
                    .andExpect(status().isCreated())
                    .andExpect(jsonPath("$.id").exists());


            var scansNoBanco = scanRedeRepository.findAll();
            assertThat(scansNoBanco).hasSize(1);
        }
    }

    @Nested
    @DisplayName("GET /scans - Consultas")
    class ConsultarScans {

        @Test
        @DisplayName("Deveria listar todos os scans pertencentes ao usuário logado (200 OK)")
        void deveriaListarScansDoUsuario() throws Exception {
            mockMvc.perform(post("/scans")
                    .with(jwt().jwt(jwt -> jwt.subject(usuarioAtivo.getId().toString())))
                    .contentType(MediaType.APPLICATION_JSON)
                    .content(toJson(criarPayloadValido())));


            mockMvc.perform(get("/scans")
                            .with(jwt().jwt(jwt -> jwt.subject(usuarioAtivo.getId().toString()))))
                    .andExpect(status().isOk())
                    .andExpect(jsonPath("$").isArray())
                    .andExpect(jsonPath("$[0].id").exists())
                    .andExpect(jsonPath("$[0].dataScan").value("2026-06-12"));
        }

        @Test
        @DisplayName("Deveria buscar os detalhes completos de um scan específico (200 OK)")
        void deveriaBuscarDetalhesDoScan() throws Exception {
            String responseBody = mockMvc.perform(post("/scans")
                            .with(jwt().jwt(jwt -> jwt.subject(usuarioAtivo.getId().toString())))
                            .contentType(MediaType.APPLICATION_JSON)
                            .content(toJson(criarPayloadValido())))
                    .andReturn().getResponse().getContentAsString();

            Integer scanIdGerado = JsonPath.read(responseBody, "$.id");


            mockMvc.perform(get("/scans/{id}", scanIdGerado)
                            .with(jwt().jwt(jwt -> jwt.subject(usuarioAtivo.getId().toString()))))
                    .andExpect(status().isOk())
                    .andExpect(jsonPath("$.id").value(scanIdGerado))
                    .andExpect(jsonPath("$.hosts").isArray())
                    .andExpect(jsonPath("$.hosts[0].ip").value("192.168.1.100"))
                    .andExpect(jsonPath("$.hosts[0].vulnerabilidades[0].script").value("vulners"));
        }
    }
}