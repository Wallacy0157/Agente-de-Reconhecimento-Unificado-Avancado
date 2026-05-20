package com.ucb.agente_reconhecimento.domain.enums;

import lombok.Getter;

@Getter
public enum Disponibilidade {

    INDISPONIVEL("Indisponível"),
    EM_DESENVOLVIMENTO("Em desenvolvimento"),
    EM_TESTES("Em testes"),
    DISPONIVEL("Disponível");

    private final String descricao;

    Disponibilidade(String descricao) {
        this.descricao = descricao;
    }
}
