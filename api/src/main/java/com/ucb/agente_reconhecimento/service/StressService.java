package com.ucb.agente_reconhecimento.service;

import com.ucb.agente_reconhecimento.domain.entities.Execucao;
import com.ucb.agente_reconhecimento.domain.entities.Ferramenta;
import com.ucb.agente_reconhecimento.domain.entities.Projeto;
import com.ucb.agente_reconhecimento.domain.entities.Usuario;
import com.ucb.agente_reconhecimento.domain.entities.stress.TesteStress;
import com.ucb.agente_reconhecimento.domain.entities.stress.TesteStressRequisicao;
import com.ucb.agente_reconhecimento.domain.enums.Disponibilidade;
import com.ucb.agente_reconhecimento.infra.exception.RecursoNaoEncontradoException;
import com.ucb.agente_reconhecimento.repository.*;
import com.ucb.agente_reconhecimento.web.dto.stress.*;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.ZoneOffset;
import java.util.List;

@RequiredArgsConstructor
@Service
public class StressService {

    private final ExecucaoRepository execucaoRepository;
    private final TesteStressRepository testeStressRepository;
    private final TesteStressRequisicaoRepository testeStressRequisicaoRepository;
    private final ProjetoRepository projetoRepository;
    private final FerramentaRepository ferramentaRepository;
    private final UsuarioRepository usuarioRepository;

    @Transactional
    public TesteStress persistirStressTest(StressTestResultadoRequest request, Integer usuarioId) {
        Projeto projeto = obterOuCriarProjeto(usuarioId);
        Ferramenta ferramenta = obterOuCriarFerramenta();
        String gravidade = calcularGravidade(request.totalEnviado(), request.quantidadeErros());

        Execucao execucao = Execucao.builder()
                .projeto(projeto)
                .ferramenta(ferramenta)
                .tipo("STRESS_TEST")
                .status("CONCLUIDO")
                .inicio(request.inicio().atZone(ZoneOffset.UTC).toLocalDateTime())
                .fim(request.fim().atZone(ZoneOffset.UTC).toLocalDateTime())
                .gravidade(gravidade)
                .resumo("Teste de stress em " + request.ipAlvo() + ":" + request.portaAlvo())
                .build();
        execucao = execucaoRepository.save(execucao);

        TesteStress testeStress = TesteStress.builder()
                .execucao(execucao)
                .ipAlvo(request.ipAlvo())
                .portaAlvo(request.portaAlvo())
                .rpsLimite(request.rpsLimite())
                .duracaoConfiguracao(request.duracaoConfiguracao())
                .totalEnviado(request.totalEnviado())
                .quantidadeSucesso(request.quantidadeSucesso())
                .quantidadeErros(request.quantidadeErros())
                .build();
        testeStress = testeStressRepository.save(testeStress);

        for (StressTestCenarioRequest cenario : request.cenarios()) {
            TesteStressRequisicao requisicao = TesteStressRequisicao.builder()
                    .testeStress(testeStress)
                    .porta(cenario.porta())
                    .status(cenario.status())
                    .latenciaMs(cenario.latenciaP95Ms())
                    .build();
            testeStressRequisicaoRepository.save(requisicao);
        }

        return testeStress;
    }

    public List<StressTestResumoResponse> listarStressTests(Integer usuarioId) {
        List<TesteStress> testes = testeStressRepository.findTop100ByExecucao_Projeto_Usuario_IdOrderByCriadoEmDesc(usuarioId);

        return testes.stream().map(teste -> new StressTestResumoResponse(
                teste.getId(),
                teste.getIpAlvo(),
                teste.getPortaAlvo(),
                teste.getRpsLimite(),
                teste.getDuracaoConfiguracao(),
                teste.getTotalEnviado(),
                teste.getQuantidadeSucesso(),
                teste.getQuantidadeErros(),
                teste.getCriadoEm()
        )).toList();
    }

    public StressTestDetalheResponse buscarStressTestPorId(Integer id, Integer usuarioId) {
        TesteStress testeStress = testeStressRepository.findById(id)
                .orElseThrow(() -> new RecursoNaoEncontradoException("TesteStress", id));

        Integer donoId = testeStress.getExecucao().getProjeto().getUsuario().getId();
        if (!donoId.equals(usuarioId)) {
            throw new RecursoNaoEncontradoException("TesteStress", id);
        }

        List<TesteStressRequisicao> requisicoes = testeStressRequisicaoRepository.findByTesteStress_Id(id);

        List<StressTestCenarioDetalheDTO> cenarios = requisicoes.stream().map(req -> new StressTestCenarioDetalheDTO(
                req.getPorta(),
                req.getStatus(),
                req.getLatenciaMs()
        )).toList();

        return new StressTestDetalheResponse(
                testeStress.getId(),
                testeStress.getIpAlvo(),
                testeStress.getPortaAlvo(),
                testeStress.getRpsLimite(),
                testeStress.getDuracaoConfiguracao(),
                testeStress.getTotalEnviado(),
                testeStress.getQuantidadeSucesso(),
                testeStress.getQuantidadeErros(),
                testeStress.getCriadoEm(),
                cenarios
        );
    }

    String calcularGravidade(Integer totalEnviado, Integer quantidadeErros) {
        if (totalEnviado == 0) return "BAIXA";
        double taxaErros = (double) quantidadeErros / totalEnviado;
        if (taxaErros <= 0.10) return "BAIXA";
        if (taxaErros <= 0.50) return "MEDIA";
        return "ALTA";
    }

    private Projeto obterOuCriarProjeto(Integer usuarioId) {
        return projetoRepository.findByUsuario_Id(usuarioId)
                .orElseGet(() -> {
                    Usuario usuario = usuarioRepository.findById(usuarioId)
                            .orElseThrow(() -> new RuntimeException("Usuário não encontrado: " + usuarioId));
                    Projeto novoProjeto = Projeto.builder()
                            .usuario(usuario)
                            .nome("Projeto Padrão")
                            .descricao("Projeto criado automaticamente para testes de stress")
                            .build();
                    return projetoRepository.save(novoProjeto);
                });
    }

    private Ferramenta obterOuCriarFerramenta() {
        return ferramentaRepository.findByNome("StressTest")
                .orElseGet(() -> {
                    Ferramenta stressTest = Ferramenta.builder()
                            .nome("StressTest")
                            .descricao("Ferramenta de teste de carga e resiliência")
                            .disponibilidade(Disponibilidade.DISPONIVEL)
                            .build();
                    return ferramentaRepository.save(stressTest);
                });
    }
}
