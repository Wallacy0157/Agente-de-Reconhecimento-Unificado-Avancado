package com.ucb.agente_reconhecimento.service;

import com.ucb.agente_reconhecimento.domain.entities.Execucao;
import com.ucb.agente_reconhecimento.domain.entities.Ferramenta;
import com.ucb.agente_reconhecimento.domain.entities.Projeto;
import com.ucb.agente_reconhecimento.domain.entities.Usuario;
import com.ucb.agente_reconhecimento.domain.entities.hydra.HydraAlvo;
import com.ucb.agente_reconhecimento.domain.entities.hydra.HydraAtaque;
import com.ucb.agente_reconhecimento.domain.entities.hydra.HydraCredencialEncontrada;
import com.ucb.agente_reconhecimento.domain.enums.Disponibilidade;
import com.ucb.agente_reconhecimento.infra.exception.RecursoNaoEncontradoException;
import com.ucb.agente_reconhecimento.repository.*;
import com.ucb.agente_reconhecimento.web.dto.hydra.*;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.ZoneOffset;
import java.util.List;

@RequiredArgsConstructor
@Service
public class HydraService {

    private final ExecucaoRepository execucaoRepository;
    private final HydraAtaqueRepository hydraAtaqueRepository;
    private final HydraAlvoRepository hydraAlvoRepository;
    private final HydraCredencialEncontradaRepository hydraCredencialRepository;
    private final ProjetoRepository projetoRepository;
    private final FerramentaRepository ferramentaRepository;
    private final UsuarioRepository usuarioRepository;

    @Transactional
    public HydraAtaque persistirAtaque(HydraResultadoRequest request, Integer usuarioId) {
        Projeto projeto = obterOuCriarProjeto(usuarioId);
        Ferramenta ferramenta = obterOuCriarFerramenta();
        String gravidade = Boolean.TRUE.equals(request.sucesso()) ? "ALTA" : "BAIXA";

        Execucao execucao = Execucao.builder()
                .projeto(projeto)
                .ferramenta(ferramenta)
                .tipo("HYDRA")
                .status("CONCLUIDO")
                .inicio(request.inicio().atZone(ZoneOffset.UTC).toLocalDateTime())
                .fim(request.fim().atZone(ZoneOffset.UTC).toLocalDateTime())
                .gravidade(gravidade)
                .resumo("Hydra " + request.servico() + " em " + request.alvos().get(0) + ":" + request.porta())
                .build();
        execucao = execucaoRepository.save(execucao);

        HydraAtaque ataque = HydraAtaque.builder()
                .execucao(execucao)
                .servico(request.servico())
                .porta(request.porta())
                .tipoAtaque(request.tipoAtaque())
                .sucesso(request.sucesso())
                .build();
        ataque = hydraAtaqueRepository.save(ataque);

        for (String alvoIp : request.alvos()) {
            HydraAlvo alvo = HydraAlvo.builder()
                    .hydraAtaque(ataque)
                    .ip(alvoIp)
                    .build();
            hydraAlvoRepository.save(alvo);
        }

        if (request.credenciaisEncontradas() != null) {
            for (HydraCredencialRequest cred : request.credenciaisEncontradas()) {
                HydraCredencialEncontrada credencial = HydraCredencialEncontrada.builder()
                        .hydraAtaque(ataque)
                        .username(cred.username())
                        .password(cred.password())
                        .build();
                hydraCredencialRepository.save(credencial);
            }
        }

        return ataque;
    }

    public List<HydraResumoResponse> listarAtaques(Integer usuarioId) {
        List<HydraAtaque> ataques = hydraAtaqueRepository.findTop100ByExecucao_Projeto_Usuario_IdOrderByCriadoEmDesc(usuarioId);

        return ataques.stream().map(ataque -> {
            int totalAlvos = hydraAlvoRepository.findByHydraAtaque_Id(ataque.getId()).size();
            int totalCreds = hydraCredencialRepository.findByHydraAtaque_Id(ataque.getId()).size();

            return new HydraResumoResponse(
                    ataque.getId(),
                    ataque.getServico(),
                    ataque.getPorta(),
                    ataque.getTipoAtaque(),
                    ataque.getSucesso(),
                    totalAlvos,
                    totalCreds,
                    ataque.getCriadoEm()
            );
        }).toList();
    }

    public HydraDetalheResponse buscarAtaquePorId(Integer id, Integer usuarioId) {
        HydraAtaque ataque = hydraAtaqueRepository.findById(id)
                .orElseThrow(() -> new RecursoNaoEncontradoException("HydraAtaque", id));

        Integer donoId = ataque.getExecucao().getProjeto().getUsuario().getId();
        if (!donoId.equals(usuarioId)) {
            throw new RecursoNaoEncontradoException("HydraAtaque", id);
        }

        List<String> alvos = hydraAlvoRepository.findByHydraAtaque_Id(id).stream()
                .map(HydraAlvo::getIp)
                .toList();

        List<HydraCredencialDTO> credenciais = hydraCredencialRepository.findByHydraAtaque_Id(id).stream()
                .map(c -> new HydraCredencialDTO(c.getUsername(), c.getPassword()))
                .toList();

        return new HydraDetalheResponse(
                ataque.getId(),
                ataque.getServico(),
                ataque.getPorta(),
                ataque.getTipoAtaque(),
                ataque.getSucesso(),
                ataque.getCriadoEm(),
                alvos,
                credenciais
        );
    }

    private Projeto obterOuCriarProjeto(Integer usuarioId) {
        return projetoRepository.findByUsuario_Id(usuarioId)
                .orElseGet(() -> {
                    Usuario usuario = usuarioRepository.findById(usuarioId)
                            .orElseThrow(() -> new RuntimeException("Usuário não encontrado: " + usuarioId));
                    Projeto novoProjeto = Projeto.builder()
                            .usuario(usuario)
                            .nome("Projeto Padrão")
                            .descricao("Projeto criado automaticamente para ataques Hydra")
                            .build();
                    return projetoRepository.save(novoProjeto);
                });
    }

    private Ferramenta obterOuCriarFerramenta() {
        return ferramentaRepository.findByNome("Hydra")
                .orElseGet(() -> {
                    Ferramenta hydra = Ferramenta.builder()
                            .nome("Hydra")
                            .descricao("Ferramenta de força bruta para teste de credenciais")
                            .disponibilidade(Disponibilidade.DISPONIVEL)
                            .build();
                    return ferramentaRepository.save(hydra);
                });
    }
}
