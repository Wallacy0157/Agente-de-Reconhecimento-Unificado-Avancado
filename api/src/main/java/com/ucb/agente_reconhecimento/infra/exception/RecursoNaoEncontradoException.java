package com.ucb.agente_reconhecimento.infra.exception;

import org.springframework.http.HttpStatus;
import org.springframework.http.ProblemDetail;

public class RecursoNaoEncontradoException extends ReconhecimentoException {

    private final String entidade;
    private final Object id;

    public RecursoNaoEncontradoException(String entidade, Object id) {
        this.entidade = entidade;
        this.id = id;
    }

    @Override
    public ProblemDetail toProblemDetail() {
        var problemDetail = ProblemDetail.forStatus(HttpStatus.NOT_FOUND);
        problemDetail.setTitle("Recurso não encontrado");
        problemDetail.setDetail("%s com id %s não encontrado.".formatted(entidade, id));
        return problemDetail;
    }
}
