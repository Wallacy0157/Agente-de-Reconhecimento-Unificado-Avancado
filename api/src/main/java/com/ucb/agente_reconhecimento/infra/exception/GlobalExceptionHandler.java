package com.ucb.agente_reconhecimento.infra.exception;

import org.springframework.http.HttpStatus;
import org.springframework.http.ProblemDetail;
import org.springframework.validation.FieldError;
import org.springframework.web.bind.MethodArgumentNotValidException;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;

import java.util.Map;

@RestControllerAdvice
public class GlobalExceptionHandler {

    @ExceptionHandler(MethodArgumentNotValidException.class)
    public ProblemDetail parametrosInvalidos(MethodArgumentNotValidException e) {
        var problemDetail = ProblemDetail.forStatus(HttpStatus.BAD_REQUEST);
        var erros = e.getFieldErrors().stream().map(ParametroInvalido::new).toList();
        problemDetail.setTitle("Parâmetros da requisição inválidos");
        problemDetail.setProperties(Map.of("parametros-invalidos", erros));
        return problemDetail;
    }

    @ExceptionHandler(ReconhecimentoException.class)
    public ProblemDetail erroPolimorfismo(ReconhecimentoException e) {
        return e.toProblemDetail();
    }

    private record ParametroInvalido(String campo, String motivo) {
        public ParametroInvalido(FieldError error) {
            this(error.getField(), error.getDefaultMessage());
        }
    }
}
