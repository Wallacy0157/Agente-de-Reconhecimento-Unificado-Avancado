package com.ucb.agente_reconhecimento.infra.exception;

import org.springframework.http.HttpStatus;
import org.springframework.http.ProblemDetail;

public class ConflitoCadastroException extends ReconhecimentoException {

    private final String campo;
    private final Object valor;

    public ConflitoCadastroException(String campo, Object valor) {
        this.campo = campo;
        this.valor = valor;
    }

    @Override
    public ProblemDetail toProblemDetail() {
        var problemDetail = ProblemDetail.forStatus(HttpStatus.CONFLICT);
        problemDetail.setTitle("Conflito no cadastro");
        problemDetail.setDetail("%s '%s' já está em uso.".formatted(campo, valor));
        return problemDetail;
    }
}
