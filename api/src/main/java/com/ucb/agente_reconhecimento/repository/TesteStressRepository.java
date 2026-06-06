package com.ucb.agente_reconhecimento.repository;

import com.ucb.agente_reconhecimento.domain.entities.stress.TesteStress;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;

public interface TesteStressRepository extends JpaRepository<TesteStress, Integer> {

    List<TesteStress> findTop100ByExecucao_Projeto_Usuario_IdOrderByCriadoEmDesc(Integer usuarioId);

}
