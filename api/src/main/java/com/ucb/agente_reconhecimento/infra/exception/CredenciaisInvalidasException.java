package com.ucb.agente_reconhecimento.infra.exception;

import org.springframework.http.HttpStatus;
import org.springframework.http.ProblemDetail;

public class CredenciaisInvalidasException extends ReconhecimentoException {

    @Override
    public ProblemDetail toProblemDetail() {
        var problemDetail = ProblemDetail.forStatus(HttpStatus.UNAUTHORIZED);
        problemDetail.setTitle("Falha na autenticação");
        problemDetail.setDetail("Email ou senha incorretos.");
        return problemDetail;
    }
}
