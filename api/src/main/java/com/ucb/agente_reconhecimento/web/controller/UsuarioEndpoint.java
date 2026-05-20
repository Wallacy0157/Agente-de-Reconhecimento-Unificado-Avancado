package com.ucb.agente_reconhecimento.web.controller;

import com.ucb.agente_reconhecimento.service.UsuarioService;
import com.ucb.agente_reconhecimento.web.dto.UsuarioCadastroDTO;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RequestMapping("/usuarios")
@RestController
public class UsuarioEndpoint {

    private final UsuarioService usuarioService;

    public UsuarioEndpoint(UsuarioService usuarioService) {
        this.usuarioService = usuarioService;
    }

    @PostMapping
    public ResponseEntity<?> cadastrarUsuario(@RequestBody UsuarioCadastroDTO usuarioCadastroDTO) {
        usuarioService.salvarUsuario(usuarioCadastroDTO);
        return ResponseEntity.ok().build();
    }

}
