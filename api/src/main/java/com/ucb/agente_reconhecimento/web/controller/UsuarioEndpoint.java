package com.ucb.agente_reconhecimento.web.controller;

import com.ucb.agente_reconhecimento.service.UsuarioService;
import com.ucb.agente_reconhecimento.web.dto.TokenResponse;
import com.ucb.agente_reconhecimento.web.dto.UsuarioCadastroDTO;
import com.ucb.agente_reconhecimento.web.dto.UsuarioLoginDTO;
import jakarta.validation.Valid;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RequestMapping("/usuarios")
@RestController
public class UsuarioEndpoint {

    private final UsuarioService usuarioService;

    public UsuarioEndpoint(UsuarioService usuarioService) {
        this.usuarioService = usuarioService;
    }

    @PostMapping
    public ResponseEntity<?> cadastrarUsuario(@RequestBody @Valid UsuarioCadastroDTO usuarioCadastroDTO) {
        usuarioService.salvarUsuario(usuarioCadastroDTO);
        return ResponseEntity.ok().build();
    }

    @PostMapping("/login")
    public ResponseEntity<TokenResponse> autenticarUsuario(@RequestBody UsuarioLoginDTO usuarioLoginDTO) {
        return ResponseEntity.ok(usuarioService.autenticarUsuario(usuarioLoginDTO));
    }

}
