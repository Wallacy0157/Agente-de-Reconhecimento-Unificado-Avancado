package com.ucb.agente_reconhecimento.service;

import com.ucb.agente_reconhecimento.domain.entities.keylogger.KeyLogger;
import com.ucb.agente_reconhecimento.repository.KeyLoggerRepository;
import com.ucb.agente_reconhecimento.web.dto.keylogger.KeyloggerResultadoRequest;
import org.springframework.stereotype.Service;

@Service
public class KeyloggerService {

    private final KeyLoggerRepository repository;

    public KeyloggerService(KeyLoggerRepository repository) {
        this.repository = repository;
    }

    public void salvar(KeyloggerResultadoRequest request, Integer usuarioId) {
        KeyLogger entity = new KeyLogger();
        entity.setInicio(request.inicio());
        entity.setTermino(request.termino());
        entity.setUrlArquivo(request.urlArquivo());

        repository.save(entity);
    }
}