package com.ucb.agente_reconhecimento.service;

import com.ucb.agente_reconhecimento.domain.entities.*;
import com.ucb.agente_reconhecimento.domain.entities.scan.*;
import com.ucb.agente_reconhecimento.domain.enums.Disponibilidade;
import com.ucb.agente_reconhecimento.domain.enums.Gravidade;
import com.ucb.agente_reconhecimento.repository.*;
import com.ucb.agente_reconhecimento.web.dto.scan.*;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.web.server.ResponseStatusException;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

@RequiredArgsConstructor
@Service
public class ScanService {

    private final ExecucaoRepository execucaoRepository;
    private final ScanRedeRepository scanRedeRepository;
    private final HostDescobertoRepository hostDescobertoRepository;
    private final PortaAbertaRepository portaAbertaRepository;
    private final VulnerabilidadeRepository vulnerabilidadeRepository;
    private final SugestaoTesteRepository sugestaoTesteRepository;
    private final ProjetoRepository projetoRepository;
    private final FerramentaRepository ferramentaRepository;
    private final UsuarioRepository usuarioRepository;

    @Transactional
    public ScanRede persistirScan(ScanResultadoRequest request, Integer usuarioId) {
        Projeto projeto = obterOuCriarProjeto(usuarioId);
        Ferramenta ferramenta = obterOuCriarFerramenta();

        ScanMetadataDTO metadata = request.metadata();
        String inicio = metadata.scanDate() + " " + metadata.scanTime();

        Execucao execucao = Execucao.builder()
                .projeto(projeto)
                .ferramenta(ferramenta)
                .tipo("SCAN_REDE")
                .status("CONCLUIDO")
                .inicio(inicio)
                .fim(inicio)
                .gravidade("BAIXA")
                .resumo("Varredura de rede executada em " + metadata.scanDate())
                .build();
        execucao = execucaoRepository.save(execucao);

        ScanRede scanRede = ScanRede.builder()
                .execucao(execucao)
                .build();
        scanRede = scanRedeRepository.save(scanRede);

        for (HostResultDTO hostDTO : request.results()) {
            HostDescoberto host = criarHost(hostDTO, scanRede);

            Map<Integer, PortaAberta> portasPorNumero = new HashMap<>();
            if (hostDTO.openPorts() != null) {
                for (PortaDTO portaDTO : hostDTO.openPorts()) {
                    PortaAberta porta = criarPorta(portaDTO, host);
                    portasPorNumero.put(portaDTO.port(), porta);
                }
            }

            if (hostDTO.vulnerabilities() != null) {
                for (VulnerabilidadeDTO vulnDTO : hostDTO.vulnerabilities()) {
                    criarVulnerabilidade(vulnDTO, portasPorNumero);
                }
            }

            if (hostDTO.suggestedTests() != null) {
                for (String suggestedTest : hostDTO.suggestedTests()) {
                    criarSugestaoTeste(suggestedTest, host);
                }
            }
        }

        return scanRede;
    }

    public List<ScanResumoResponse> listarScans(Integer usuarioId) {
        List<ScanRede> scans = scanRedeRepository.findByExecucao_Projeto_Usuario_IdOrderByExecucao_InicioDesc(usuarioId);

        return scans.stream().map(scan -> {
            Execucao execucao = scan.getExecucao();

            String scanDate = "";
            String scanTime = "";
            if (execucao.getInicio() != null) {
                String[] parts = execucao.getInicio().split(" ", 2);
                scanDate = parts[0];
                scanTime = parts.length > 1 ? parts[1] : "";
            }

            int totalHosts = hostDescobertoRepository.findByScanRede_Id(scan.getId()).size();
            int totalVulnerabilities = vulnerabilidadeRepository.countByPortaAberta_HostDescoberto_ScanRede_Id(scan.getId());

            return new ScanResumoResponse(
                    scan.getId(),
                    scanDate,
                    scanTime,
                    totalHosts,
                    totalVulnerabilities,
                    execucao.getStatus()
            );
        }).toList();
    }

    public ScanDetalheResponse buscarScanPorId(Integer scanId, Integer usuarioId) {
        ScanRede scanRede = scanRedeRepository.findById(scanId)
                .orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND, "Scan não encontrado"));

        Integer donoId = scanRede.getExecucao().getProjeto().getUsuario().getId();
        if (!donoId.equals(usuarioId)) {
            throw new ResponseStatusException(HttpStatus.FORBIDDEN, "Acesso negado: scan pertence a outro usuário");
        }

        Execucao execucao = scanRede.getExecucao();
        String scanDate = "";
        String scanTime = "";
        if (execucao.getInicio() != null) {
            String[] parts = execucao.getInicio().split(" ", 2);
            scanDate = parts[0];
            scanTime = parts.length > 1 ? parts[1] : "";
        }
        ScanMetadataDTO metadata = new ScanMetadataDTO(scanDate, scanTime, null);

        List<HostDescoberto> hosts = hostDescobertoRepository.findByScanRede_Id(scanId);
        List<HostDetalheDTO> hostDTOs = hosts.stream().map(host -> {
            List<PortaAberta> portas = portaAbertaRepository.findByHostDescoberto_Id(host.getId());
            List<PortaDTO> portaDTOs = portas.stream()
                    .map(p -> new PortaDTO(p.getPorta(), p.getProtocolo(), p.getServico()))
                    .toList();

            List<VulnerabilidadeDTO> vulnDTOs = portas.stream()
                    .flatMap(p -> vulnerabilidadeRepository.findByPortaAberta_Id(p.getId()).stream())
                    .map(v -> new VulnerabilidadeDTO(
                            v.getPortaAberta() != null ? String.valueOf(v.getPortaAberta().getPorta()) : null,
                            v.getObservacao(),
                            v.getDetalhes()
                    ))
                    .toList();

            List<String> suggestedTests = sugestaoTesteRepository.findByHostDescoberto_Id(host.getId()).stream()
                    .map(SugestaoTeste::getMotivo)
                    .toList();

            return new HostDetalheDTO(
                    host.getId(),
                    host.getIp(),
                    host.getOsDetectado(),
                    host.getErro(),
                    host.isTemWeb(),
                    host.isTemDatabase(),
                    host.isTemAcessoRemoto(),
                    host.isTemServicoAuth(),
                    portaDTOs,
                    vulnDTOs,
                    suggestedTests
            );
        }).toList();

        return new ScanDetalheResponse(scanRede.getId(), metadata, hostDTOs);
    }

    private Projeto obterOuCriarProjeto(Integer usuarioId) {
        return projetoRepository.findByUsuario_Id(usuarioId)
                .orElseGet(() -> {
                    Usuario usuario = usuarioRepository.findById(usuarioId)
                            .orElseThrow(() -> new RuntimeException("Usuário não encontrado: " + usuarioId));
                    Projeto novoProjeto = Projeto.builder()
                            .usuario(usuario)
                            .nome("Projeto Padrão")
                            .descricao("Projeto criado automaticamente para varreduras de rede")
                            .build();
                    return projetoRepository.save(novoProjeto);
                });
    }

    private Ferramenta obterOuCriarFerramenta() {
        return ferramentaRepository.findByNome("Nmap")
                .orElseGet(() -> {
                    Ferramenta nmap = Ferramenta.builder()
                            .nome("Nmap")
                            .descricao("Scanner de rede e detecção de vulnerabilidades")
                            .disponibilidade(Disponibilidade.DISPONIVEL)
                            .build();
                    return ferramentaRepository.save(nmap);
                });
    }

    private HostDescoberto criarHost(HostResultDTO hostDTO, ScanRede scanRede) {
        boolean temWeb = false;
        boolean temDatabase = false;
        boolean temAcessoRemoto = false;
        boolean temServicoAuth = false;

        if (hostDTO.serviceProfile() != null) {
            temWeb = hostDTO.serviceProfile().web();
            temDatabase = hostDTO.serviceProfile().database();
            temAcessoRemoto = hostDTO.serviceProfile().remoteAccess();
            temServicoAuth = hostDTO.serviceProfile().authService();
        }

        HostDescoberto host = HostDescoberto.builder()
                .scanRede(scanRede)
                .ip(hostDTO.ip())
                .osDetectado(hostDTO.os())
                .erro(hostDTO.error())
                .temWeb(temWeb)
                .temDatabase(temDatabase)
                .temAcessoRemoto(temAcessoRemoto)
                .temServicoAuth(temServicoAuth)
                .build();
        return hostDescobertoRepository.save(host);
    }

    private PortaAberta criarPorta(PortaDTO portaDTO, HostDescoberto host) {
        PortaAberta porta = PortaAberta.builder()
                .hostDescoberto(host)
                .porta(portaDTO.port())
                .protocolo(portaDTO.protocol())
                .servico(portaDTO.service())
                .build();
        return portaAbertaRepository.save(porta);
    }

    private void criarVulnerabilidade(VulnerabilidadeDTO vulnDTO, Map<Integer, PortaAberta> portasPorNumero) {
        PortaAberta portaAberta = null;
        if (vulnDTO.port() != null) {
            try {
                Integer portNumber = Integer.parseInt(vulnDTO.port());
                portaAberta = portasPorNumero.get(portNumber);
            } catch (NumberFormatException ignored) {
            }
        }

        Vulnerabilidade vulnerabilidade = Vulnerabilidade.builder()
                .portaAberta(portaAberta)
                .detalhes(vulnDTO.details())
                .observacao(vulnDTO.script())
                .gravidade(Gravidade.MEDIA)
                .build();
        vulnerabilidadeRepository.save(vulnerabilidade);
    }

    private void criarSugestaoTeste(String suggestedTest, HostDescoberto host) {
        Ferramenta ferramentaSugerida = ferramentaRepository.findByNome(suggestedTest).orElse(null);

        SugestaoTeste sugestao = SugestaoTeste.builder()
                .hostDescoberto(host)
                .ferramentaSugerida(ferramentaSugerida)
                .motivo(suggestedTest)
                .build();
        sugestaoTesteRepository.save(sugestao);
    }
}
