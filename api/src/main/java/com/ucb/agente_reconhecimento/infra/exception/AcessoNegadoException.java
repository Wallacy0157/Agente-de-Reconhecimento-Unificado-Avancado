package com.ucb.agente_reconhecimento.infra.exception;

import org.springframework.http.HttpStatus;
import org.springframework.http.ProblemDetail;

public class AcessoNegadoException extends ReconhecimentoException {

    private final String motivo;

    public AcessoNegadoException(String motivo) {
        this.motivo = motivo;
    }

    @Override
    public ProblemDetail toProblemDetail() {
        var problemDetail = ProblemDetail.forStatus(HttpStatus.FORBIDDEN);
        problemDetail.setTitle("Acesso negado");
        problemDetail.setDetail(motivo);
        return problemDetail;
    }
}
