package com.ucb.agente_reconhecimento.web.controller;

import com.ucb.agente_reconhecimento.domain.entities.osint.Osint;
import com.ucb.agente_reconhecimento.service.OsintService;
import com.ucb.agente_reconhecimento.web.dto.osint.OsintCriadoResponse;
import com.ucb.agente_reconhecimento.web.dto.osint.OsintDetalheResponse;
import com.ucb.agente_reconhecimento.web.dto.osint.OsintResultadoRequest;
import com.ucb.agente_reconhecimento.web.dto.osint.OsintResumoResponse;
import jakarta.validation.Valid;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.oauth2.server.resource.authentication.JwtAuthenticationToken;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RequestMapping("/osint")
@RestController
public class OsintEndpoint {

    private final OsintService osintService;

    public OsintEndpoint(OsintService osintService) {
        this.osintService = osintService;
    }

    @PostMapping
    public ResponseEntity<OsintCriadoResponse> criarInvestigacao(
            @RequestBody @Valid OsintResultadoRequest request,
            JwtAuthenticationToken authentication) {

        Integer usuarioId = Integer.parseInt(authentication.getToken().getSubject());
        Osint osint = osintService.persistirOsint(request, usuarioId);

        return ResponseEntity.status(HttpStatus.CREATED)
                .body(new OsintCriadoResponse(osint.getId()));
    }

    @GetMapping
    public ResponseEntity<List<OsintResumoResponse>> listarInvestigacoes(
            JwtAuthenticationToken authentication) {

        Integer usuarioId = Integer.parseInt(authentication.getToken().getSubject());
        List<OsintResumoResponse> investigacoes = osintService.listarInvestigacoes(usuarioId);
        return ResponseEntity.ok(investigacoes);
    }

    @GetMapping("/{id}")
    public ResponseEntity<OsintDetalheResponse> buscarInvestigacao(
            @PathVariable Integer id,
            JwtAuthenticationToken authentication) {

        Integer usuarioId = Integer.parseInt(authentication.getToken().getSubject());
        OsintDetalheResponse response = osintService.buscarInvestigacaoPorId(id, usuarioId);
        return ResponseEntity.ok(response);
    }
}
