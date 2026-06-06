package com.ucb.agente_reconhecimento.service;

import com.ucb.agente_reconhecimento.domain.entities.Execucao;
import com.ucb.agente_reconhecimento.domain.entities.Ferramenta;
import com.ucb.agente_reconhecimento.domain.entities.Projeto;
import com.ucb.agente_reconhecimento.domain.entities.Usuario;
import com.ucb.agente_reconhecimento.domain.entities.osint.Osint;
import com.ucb.agente_reconhecimento.domain.entities.osint.OsintResultado;
import com.ucb.agente_reconhecimento.domain.enums.Disponibilidade;
import com.ucb.agente_reconhecimento.infra.exception.RecursoNaoEncontradoException;
import com.ucb.agente_reconhecimento.repository.*;
import com.ucb.agente_reconhecimento.web.dto.osint.*;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.ZoneOffset;
import java.util.List;

@RequiredArgsConstructor
@Service
public class OsintService {

    private final ExecucaoRepository execucaoRepository;
    private final OsintRepository osintRepository;
    private final OsintResultadoRepository osintResultadoRepository;
    private final ProjetoRepository projetoRepository;
    private final FerramentaRepository ferramentaRepository;
    private final UsuarioRepository usuarioRepository;

    @Transactional
    public Osint persistirOsint(OsintResultadoRequest request, Integer usuarioId) {
        Projeto projeto = obterOuCriarProjeto(usuarioId);
        Ferramenta ferramenta = obterOuCriarFerramenta();
        String gravidade = calcularGravidade(request.totalEncontrado());

        Execucao execucao = Execucao.builder()
                .projeto(projeto)
                .ferramenta(ferramenta)
                .tipo("OSINT")
                .status("CONCLUIDO")
                .inicio(request.inicio().atZone(ZoneOffset.UTC).toLocalDateTime())
                .fim(request.fim().atZone(ZoneOffset.UTC).toLocalDateTime())
                .gravidade(gravidade)
                .resumo("Investigação OSINT: " + request.alvo() + " (" + request.modo() + ")")
                .build();
        execucao = execucaoRepository.save(execucao);

        Osint osint = Osint.builder()
                .execucao(execucao)
                .alvo(request.alvo())
                .modo(request.modo())
                .totalEncontrado(request.totalEncontrado())
                .build();
        osint = osintRepository.save(osint);

        for (OsintItemRequest item : request.resultados()) {
            OsintResultado resultado = OsintResultado.builder()
                    .osint(osint)
                    .site(item.site())
                    .url(item.url())
                    .titulo(item.titulo())
                    .fonte(item.fonte())
                    .build();
            osintResultadoRepository.save(resultado);
        }

        return osint;
    }

    public List<OsintResumoResponse> listarInvestigacoes(Integer usuarioId) {
        List<Osint> investigacoes = osintRepository.findTop100ByExecucao_Projeto_Usuario_IdOrderByCriadoEmDesc(usuarioId);

        return investigacoes.stream().map(osint -> new OsintResumoResponse(
                osint.getId(),
                osint.getAlvo(),
                osint.getModo(),
                osint.getTotalEncontrado(),
                osint.getCriadoEm()
        )).toList();
    }

    public OsintDetalheResponse buscarInvestigacaoPorId(Integer id, Integer usuarioId) {
        Osint osint = osintRepository.findById(id)
                .orElseThrow(() -> new RecursoNaoEncontradoException("Osint", id));

        Integer donoId = osint.getExecucao().getProjeto().getUsuario().getId();
        if (!donoId.equals(usuarioId)) {
            throw new RecursoNaoEncontradoException("Osint", id);
        }

        List<OsintResultado> resultados = osintResultadoRepository.findByOsint_Id(id);

        List<OsintItemDetalheDTO> itens = resultados.stream().map(r -> new OsintItemDetalheDTO(
                r.getSite(),
                r.getUrl(),
                r.getTitulo(),
                r.getFonte()
        )).toList();

        return new OsintDetalheResponse(
                osint.getId(),
                osint.getAlvo(),
                osint.getModo(),
                osint.getTotalEncontrado(),
                osint.getCriadoEm(),
                itens
        );
    }

    String calcularGravidade(Integer totalEncontrado) {
        if (totalEncontrado == null || totalEncontrado <= 5) return "BAIXA";
        if (totalEncontrado <= 20) return "MEDIA";
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
                            .descricao("Projeto criado automaticamente para investigações OSINT")
                            .build();
                    return projetoRepository.save(novoProjeto);
                });
    }

    private Ferramenta obterOuCriarFerramenta() {
        return ferramentaRepository.findByNome("Sherlock")
                .orElseGet(() -> {
                    Ferramenta sherlock = Ferramenta.builder()
                            .nome("Sherlock")
                            .descricao("Ferramenta OSINT para busca de perfis e informações públicas")
                            .disponibilidade(Disponibilidade.DISPONIVEL)
                            .build();
                    return ferramentaRepository.save(sherlock);
                });
    }
}
