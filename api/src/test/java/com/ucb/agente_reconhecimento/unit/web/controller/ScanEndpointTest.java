package com.ucb.agente_reconhecimento.unit.web.controller;

import com.ucb.agente_reconhecimento.domain.entities.scan.ScanRede;
import com.ucb.agente_reconhecimento.service.ScanService;
import com.ucb.agente_reconhecimento.web.controller.ScanEndpoint;
import com.ucb.agente_reconhecimento.web.dto.scan.*;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Nested;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.http.HttpStatus;
import org.springframework.security.oauth2.jwt.Jwt;
import org.springframework.security.oauth2.server.resource.authentication.JwtAuthenticationToken;

import java.util.List;

import static org.assertj.core.api.Assertions.*;
import static org.mockito.Mockito.*;

@ExtendWith(MockitoExtension.class)
class ScanEndpointTest {

    @Mock
    ScanService scanService;

    @InjectMocks
    ScanEndpoint scanEndpoint;

    private JwtAuthenticationToken criarAuthToken(Integer usuarioId) {
        var jwt = mock(Jwt.class);
        doReturn(String.valueOf(usuarioId)).when(jwt).getSubject();
        return new JwtAuthenticationToken(jwt);
    }

    @Nested
    class criarScan {

        @Test
        @DisplayName("Deveria delegar a persistência para ScanService e retornar HTTP 201")
        void deveriaDelegarParaServiceERetornar201() {
            // Arrange
            var auth = criarAuthToken(1);
            var metadata = new ScanMetadataDTO("2025-01-15", "14:30:00", null);
            var host = new HostResultDTO("192.168.1.1", "Linux", null, List.of(), null, List.of(), List.of());
            var request = new ScanResultadoRequest(metadata, List.of(host));

            var scanRede = new ScanRede();
            scanRede.setId(10);

            doReturn(scanRede).when(scanService).persistirScan(request, 1);

            // Act
            var response = scanEndpoint.criarScan(request, auth);

            // Assert
            assertThat(response.getStatusCode()).isEqualTo(HttpStatus.CREATED);
            assertThat(response.getBody()).isNotNull();
            assertThat(response.getBody().id()).isEqualTo(10);

            verify(scanService, times(1)).persistirScan(request, 1);
            verifyNoMoreInteractions(scanService);
        }
    }

    @Nested
    class listarScans {

        @Test
        @DisplayName("Deveria delegar a listagem para ScanService e retornar HTTP 200")
        void deveriaDelegarParaServiceERetornar200() {
            // Arrange
            var auth = criarAuthToken(1);
            var resumos = List.of(
                    new ScanResumoResponse(10, "2025-01-15", "14:30", 5, 3, "CONCLUIDO"),
                    new ScanResumoResponse(11, "2025-01-16", "09:00", 2, 0, "CONCLUIDO")
            );

            doReturn(resumos).when(scanService).listarScans(1);

            // Act
            var response = scanEndpoint.listarScans(auth);

            // Assert
            assertThat(response.getStatusCode()).isEqualTo(HttpStatus.OK);
            assertThat(response.getBody()).hasSize(2);
            assertThat(response.getBody().get(0).id()).isEqualTo(10);

            verify(scanService, times(1)).listarScans(1);
            verifyNoMoreInteractions(scanService);
        }

        @Test
        @DisplayName("Deveria retornar lista vazia quando não há scans")
        void deveriaRetornarListaVazia() {
            // Arrange
            var auth = criarAuthToken(5);

            doReturn(List.of()).when(scanService).listarScans(5);

            // Act
            var response = scanEndpoint.listarScans(auth);

            // Assert
            assertThat(response.getStatusCode()).isEqualTo(HttpStatus.OK);
            assertThat(response.getBody()).isEmpty();
        }
    }

    @Nested
    class buscarScan {

        @Test
        @DisplayName("Deveria delegar a busca para ScanService e retornar HTTP 200 com detalhes")
        void deveriaDelegarParaServiceERetornarDetalhes() {
            // Arrange
            var auth = criarAuthToken(1);
            var metadata = new ScanMetadataDTO("2025-01-15", "14:30", null);
            var hostDetalhe = new HostDetalheDTO(
                    100, "192.168.1.1", "Linux 5.x", null,
                    true, false, false, false,
                    List.of(new PortaDTO(80, "tcp", "http")),
                    List.of(),
                    List.of("Nikto")
            );
            var detalheResponse = new ScanDetalheResponse(10, metadata, List.of(hostDetalhe));

            doReturn(detalheResponse).when(scanService).buscarScanPorId(10, 1);

            // Act
            var response = scanEndpoint.buscarScan(10, auth);

            // Assert
            assertThat(response.getStatusCode()).isEqualTo(HttpStatus.OK);
            assertThat(response.getBody()).isNotNull();
            assertThat(response.getBody().id()).isEqualTo(10);
            assertThat(response.getBody().hosts()).hasSize(1);
            assertThat(response.getBody().hosts().get(0).ip()).isEqualTo("192.168.1.1");

            verify(scanService, times(1)).buscarScanPorId(10, 1);
            verifyNoMoreInteractions(scanService);
        }
    }
}
