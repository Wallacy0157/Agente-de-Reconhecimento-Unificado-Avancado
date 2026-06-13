package com.ucb.agente_reconhecimento.web.controller;

import com.ucb.agente_reconhecimento.service.JohnService;
import com.ucb.agente_reconhecimento.web.dto.john.JohnResultadoRequest;
import jakarta.validation.Valid;
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
    public ResponseEntity<Void> salvarRelatorio(
            @RequestBody @Valid JohnResultadoRequest request,
            JwtAuthenticationToken authentication) {

        Integer usuarioId = Integer.parseInt(authentication.getToken().getSubject());
        johnService.salvar(request, usuarioId);

        return ResponseEntity.status(HttpStatus.CREATED).build();
    }
}