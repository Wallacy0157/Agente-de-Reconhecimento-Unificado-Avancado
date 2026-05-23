package com.ucb.agente_reconhecimento.infra.exception;

import org.springframework.http.HttpStatus;
import org.springframework.http.ProblemDetail;

public class SenhasNaoCoincidemException extends ReconhecimentoException {

    @Override
    public ProblemDetail toProblemDetail() {
        var problemDetail = ProblemDetail.forStatus(HttpStatus.BAD_REQUEST);
        problemDetail.setTitle("Validação de senha");
        problemDetail.setDetail("As senhas informadas não coincidem.");
        return problemDetail;
    }
}
