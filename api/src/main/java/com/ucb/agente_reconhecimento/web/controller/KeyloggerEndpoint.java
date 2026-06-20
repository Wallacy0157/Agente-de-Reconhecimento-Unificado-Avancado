package com.ucb.agente_reconhecimento.web.controller;

import com.ucb.agente_reconhecimento.domain.entities.keylogger.KeyLogger;
import com.ucb.agente_reconhecimento.service.KeyloggerService;
import com.ucb.agente_reconhecimento.web.dto.keylogger.KeyloggerCriadoResponse;
import com.ucb.agente_reconhecimento.web.dto.keylogger.KeyloggerResultadoRequest;
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
    public ResponseEntity<KeyloggerCriadoResponse> salvarCaptura(
            @RequestBody KeyloggerResultadoRequest request,
            JwtAuthenticationToken authentication) {

        Integer usuarioId = Integer.parseInt(authentication.getToken().getSubject());
        KeyLogger entity = keyloggerService.salvar(request, usuarioId);

        return ResponseEntity.status(HttpStatus.CREATED)
                .body(new KeyloggerCriadoResponse(entity.getId()));
    }
}