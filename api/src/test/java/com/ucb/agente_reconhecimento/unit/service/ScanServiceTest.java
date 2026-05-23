package com.ucb.agente_reconhecimento.unit.service;

import com.ucb.agente_reconhecimento.domain.entities.Execucao;
import com.ucb.agente_reconhecimento.domain.entities.Projeto;
import com.ucb.agente_reconhecimento.domain.entities.Usuario;
import com.ucb.agente_reconhecimento.domain.entities.scan.HostDescoberto;
import com.ucb.agente_reconhecimento.domain.entities.scan.PortaAberta;
import com.ucb.agente_reconhecimento.domain.entities.scan.ScanRede;
import com.ucb.agente_reconhecimento.domain.entities.scan.Vulnerabilidade;
import com.ucb.agente_reconhecimento.infra.exception.AcessoNegadoException;
import com.ucb.agente_reconhecimento.infra.exception.RecursoNaoEncontradoException;
import com.ucb.agente_reconhecimento.repository.*;
import com.ucb.agente_reconhecimento.service.ScanService;
import com.ucb.agente_reconhecimento.web.dto.scan.ScanDetalheResponse;
import com.ucb.agente_reconhecimento.web.dto.scan.ScanResumoResponse;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Nested;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import java.time.LocalDateTime;
import java.util.Collections;
import java.util.List;
import java.util.Optional;

import static org.assertj.core.api.Assertions.*;
import static org.mockito.Mockito.*;

@ExtendWith(MockitoExtension.class)
class ScanServiceTest {

    @Mock
    ExecucaoRepository execucaoRepository;

    @Mock
    ScanRedeRepository scanRedeRepository;

    @Mock
    HostDescobertoRepository hostDescobertoRepository;

    @Mock
    PortaAbertaRepository portaAbertaRepository;

    @Mock
    VulnerabilidadeRepository vulnerabilidadeRepository;

    @Mock
    SugestaoTesteRepository sugestaoTesteRepository;

    @Mock
    ProjetoRepository projetoRepository;

    @Mock
    FerramentaRepository ferramentaRepository;

    @Mock
    UsuarioRepository usuarioRepository;

    @InjectMocks
    ScanService scanService;

    @Nested
    class listarScans {

        @Test
        @DisplayName("Deveria retornar lista vazia quando usuário não possui scans")
        void deveriaRetornarListaVaziaQuandoNaoHaScans() {
            // Arrange
            Integer usuarioId = 1;
            doReturn(Collections.emptyList())
                    .when(scanRedeRepository)
                    .findByExecucao_Projeto_Usuario_IdOrderByExecucao_InicioDesc(usuarioId);

            // Act
            List<ScanResumoResponse> resultado = scanService.listarScans(usuarioId);

            // Assert
            assertThat(resultado).isEmpty();
            verify(scanRedeRepository, times(1))
                    .findByExecucao_Projeto_Usuario_IdOrderByExecucao_InicioDesc(usuarioId);
        }

        @Test
        @DisplayName("Deveria retornar lista com resumos mapeados corretamente")
        void deveriaRetornarListaComResumosMapeados() {
            // Arrange
            Integer usuarioId = 1;
            LocalDateTime inicio = LocalDateTime.of(2025, 1, 15, 14, 30, 0);

            var execucao = new Execucao();
            execucao.setInicio(inicio);
            execucao.setStatus("CONCLUIDO");

            var scanRede = new ScanRede();
            scanRede.setId(10);
            scanRede.setExecucao(execucao);

            doReturn(List.of(scanRede))
                    .when(scanRedeRepository)
                    .findByExecucao_Projeto_Usuario_IdOrderByExecucao_InicioDesc(usuarioId);

            doReturn(List.of(new HostDescoberto(), new HostDescoberto()))
                    .when(hostDescobertoRepository).findByScanRede_Id(10);

            doReturn(3)
                    .when(vulnerabilidadeRepository).countByPortaAberta_HostDescoberto_ScanRede_Id(10);

            // Act
            List<ScanResumoResponse> resultado = scanService.listarScans(usuarioId);

            // Assert
            assertThat(resultado).hasSize(1);
            var resumo = resultado.get(0);
            assertThat(resumo.id()).isEqualTo(10);
            assertThat(resumo.scanDate()).isEqualTo("2025-01-15");
            assertThat(resumo.scanTime()).isEqualTo("14:30");
            assertThat(resumo.totalHosts()).isEqualTo(2);
            assertThat(resumo.totalVulnerabilities()).isEqualTo(3);
            assertThat(resumo.status()).isEqualTo("CONCLUIDO");
        }
    }

    @Nested
    class buscarScanPorId {

        @Test
        @DisplayName("Deveria lançar RecursoNaoEncontradoException quando scan não existe")
        void deveriaLancarExcecaoQuandoScanNaoExiste() {
            // Arrange
            Integer scanId = 99;
            Integer usuarioId = 1;

            doReturn(Optional.empty()).when(scanRedeRepository).findById(scanId);

            // Act & Assert
            assertThatThrownBy(() -> scanService.buscarScanPorId(scanId, usuarioId))
                    .isInstanceOf(RecursoNaoEncontradoException.class);
        }

        @Test
        @DisplayName("Deveria lançar AcessoNegadoException quando scan pertence a outro usuário")
        void deveriaLancarExcecaoQuandoScanPertenceAOutroUsuario() {
            // Arrange
            Integer scanId = 10;
            Integer usuarioId = 1;
            Integer outroUsuarioId = 99;

            var usuario = new Usuario();
            usuario.setId(outroUsuarioId);

            var projeto = new Projeto();
            projeto.setUsuario(usuario);

            var execucao = new Execucao();
            execucao.setProjeto(projeto);
            execucao.setInicio(LocalDateTime.now());

            var scanRede = new ScanRede();
            scanRede.setId(scanId);
            scanRede.setExecucao(execucao);

            doReturn(Optional.of(scanRede)).when(scanRedeRepository).findById(scanId);

            // Act & Assert
            assertThatThrownBy(() -> scanService.buscarScanPorId(scanId, usuarioId))
                    .isInstanceOf(AcessoNegadoException.class);
        }

        @Test
        @DisplayName("Deveria retornar detalhes completos quando scan pertence ao usuário")
        void deveriaRetornarDetalhesQuandoScanPerteceAoUsuario() {
            // Arrange
            Integer scanId = 10;
            Integer usuarioId = 1;

            var usuario = new Usuario();
            usuario.setId(usuarioId);

            var projeto = new Projeto();
            projeto.setUsuario(usuario);

            var execucao = new Execucao();
            execucao.setProjeto(projeto);
            execucao.setInicio(LocalDateTime.of(2025, 3, 20, 10, 0, 0));

            var scanRede = new ScanRede();
            scanRede.setId(scanId);
            scanRede.setExecucao(execucao);

            var host = new HostDescoberto();
            host.setId(100);
            host.setIp("192.168.1.1");
            host.setOsDetectado("Linux 5.x");

            var porta = new PortaAberta();
            porta.setId(200);
            porta.setPorta(80);
            porta.setProtocolo("tcp");
            porta.setServico("http");

            doReturn(Optional.of(scanRede)).when(scanRedeRepository).findById(scanId);
            doReturn(List.of(host)).when(hostDescobertoRepository).findByScanRede_Id(scanId);
            doReturn(List.of(porta)).when(portaAbertaRepository).findByHostDescoberto_Id(100);
            doReturn(Collections.emptyList()).when(vulnerabilidadeRepository).findByPortaAberta_Id(200);
            doReturn(Collections.emptyList()).when(sugestaoTesteRepository).findByHostDescoberto_Id(100);

            // Act
            ScanDetalheResponse response = scanService.buscarScanPorId(scanId, usuarioId);

            // Assert
            assertThat(response).isNotNull();
            assertThat(response.id()).isEqualTo(scanId);
            assertThat(response.metadata().scanDate()).isEqualTo("2025-03-20");
            assertThat(response.metadata().scanTime()).isEqualTo("10:00");
            assertThat(response.hosts()).hasSize(1);

            var hostDto = response.hosts().get(0);
            assertThat(hostDto.ip()).isEqualTo("192.168.1.1");
            assertThat(hostDto.os()).isEqualTo("Linux 5.x");
            assertThat(hostDto.openPorts()).hasSize(1);
            assertThat(hostDto.openPorts().get(0).port()).isEqualTo(80);
            assertThat(hostDto.openPorts().get(0).protocol()).isEqualTo("tcp");
            assertThat(hostDto.openPorts().get(0).service()).isEqualTo("http");
        }
    }
}
