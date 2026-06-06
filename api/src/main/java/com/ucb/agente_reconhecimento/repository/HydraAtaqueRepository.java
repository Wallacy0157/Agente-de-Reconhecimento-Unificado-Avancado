package com.ucb.agente_reconhecimento.repository;

import com.ucb.agente_reconhecimento.domain.entities.hydra.HydraAtaque;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;

public interface HydraAtaqueRepository extends JpaRepository<HydraAtaque, Integer> {

    List<HydraAtaque> findTop100ByExecucao_Projeto_Usuario_IdOrderByCriadoEmDesc(Integer usuarioId);
}
