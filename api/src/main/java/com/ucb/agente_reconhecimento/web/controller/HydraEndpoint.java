package com.ucb.agente_reconhecimento.web.controller;

import com.ucb.agente_reconhecimento.domain.entities.hydra.HydraAtaque;
import com.ucb.agente_reconhecimento.service.HydraService;
import com.ucb.agente_reconhecimento.web.dto.hydra.HydraCriadoResponse;
import com.ucb.agente_reconhecimento.web.dto.hydra.HydraDetalheResponse;
import com.ucb.agente_reconhecimento.web.dto.hydra.HydraResultadoRequest;
import com.ucb.agente_reconhecimento.web.dto.hydra.HydraResumoResponse;
import jakarta.validation.Valid;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.oauth2.server.resource.authentication.JwtAuthenticationToken;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RequestMapping("/hydra")
@RestController
public class HydraEndpoint {

    private final HydraService hydraService;

    public HydraEndpoint(HydraService hydraService) {
        this.hydraService = hydraService;
    }

    @PostMapping
    public ResponseEntity<HydraCriadoResponse> criarAtaque(
            @RequestBody @Valid HydraResultadoRequest request,
            JwtAuthenticationToken authentication) {

        Integer usuarioId = Integer.parseInt(authentication.getToken().getSubject());
        HydraAtaque ataque = hydraService.persistirAtaque(request, usuarioId);

        return ResponseEntity.status(HttpStatus.CREATED)
                .body(new HydraCriadoResponse(ataque.getId()));
    }

    @GetMapping
    public ResponseEntity<List<HydraResumoResponse>> listarAtaques(
            JwtAuthenticationToken authentication) {

        Integer usuarioId = Integer.parseInt(authentication.getToken().getSubject());
        List<HydraResumoResponse> ataques = hydraService.listarAtaques(usuarioId);
        return ResponseEntity.ok(ataques);
    }

    @GetMapping("/{id}")
    public ResponseEntity<HydraDetalheResponse> buscarAtaque(
            @PathVariable Integer id,
            JwtAuthenticationToken authentication) {

        Integer usuarioId = Integer.parseInt(authentication.getToken().getSubject());
        HydraDetalheResponse response = hydraService.buscarAtaquePorId(id, usuarioId);
        return ResponseEntity.ok(response);
    }
}
