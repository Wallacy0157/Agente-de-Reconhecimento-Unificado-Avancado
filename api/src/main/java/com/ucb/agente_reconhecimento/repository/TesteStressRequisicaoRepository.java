package com.ucb.agente_reconhecimento.repository;

import com.ucb.agente_reconhecimento.domain.entities.stress.TesteStressRequisicao;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;

public interface TesteStressRequisicaoRepository extends JpaRepository<TesteStressRequisicao, Integer> {

    List<TesteStressRequisicao> findByTesteStress_Id(Integer testeStressId);

}
