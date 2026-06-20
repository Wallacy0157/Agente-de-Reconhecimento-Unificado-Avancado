package com.ucb.agente_reconhecimento.web.controller;

import com.ucb.agente_reconhecimento.domain.entities.john.JohnTheRipper;
import com.ucb.agente_reconhecimento.service.JohnService;
import com.ucb.agente_reconhecimento.web.dto.john.JohnCriadoResponse;
import com.ucb.agente_reconhecimento.web.dto.john.JohnResultadoRequest;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.oauth2.server.resource.authentication.JwtAuthenticationToken;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/john")
public class JohnEndpoint {

    private final JohnService johnService;

    public JohnEndpoint(JohnService johnService) {
        this.johnService = johnService;
    }

    @PostMapping
    public ResponseEntity<JohnCriadoResponse> salvarRelatorio(
            @RequestBody JohnResultadoRequest request,
            JwtAuthenticationToken authentication) {

        Integer usuarioId = Integer.parseInt(authentication.getToken().getSubject());
        JohnTheRipper entity = johnService.salvar(request, usuarioId);

        return ResponseEntity.status(HttpStatus.CREATED)
                .body(new JohnCriadoResponse(entity.getId()));
    }
}