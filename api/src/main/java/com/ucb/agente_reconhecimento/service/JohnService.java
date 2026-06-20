package com.ucb.agente_reconhecimento.service;

import com.ucb.agente_reconhecimento.domain.entities.john.JohnTheRipper;
import com.ucb.agente_reconhecimento.repository.JohnTheRipperRepository;
import com.ucb.agente_reconhecimento.web.dto.john.JohnResultadoRequest;
import org.springframework.stereotype.Service;

@Service
public class JohnService {

    private final JohnTheRipperRepository repository;

    public JohnService(JohnTheRipperRepository repository) {
        this.repository = repository;
    }

    public JohnTheRipper salvar(JohnResultadoRequest request, Integer usuarioId) {
        JohnTheRipper entity = new JohnTheRipper();
        entity.setHashAlvo(request.hashAlvo());
        entity.setAlgoritmo(request.algoritmo());
        entity.setSalt(request.salt());
        entity.setSenhaEncontrada(request.senhaEncontrada());
        entity.setModoAtaque(request.modoAtaque());
        entity.setHashesTestados(request.hashesTestados());
        entity.setStatus(request.status());

        return repository.save(entity);
    }
}