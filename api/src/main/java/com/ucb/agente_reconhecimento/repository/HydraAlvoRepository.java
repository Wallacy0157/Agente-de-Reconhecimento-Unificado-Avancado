package com.ucb.agente_reconhecimento.repository;

import com.ucb.agente_reconhecimento.domain.entities.hydra.HydraAlvo;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;

public interface HydraAlvoRepository extends JpaRepository<HydraAlvo, Integer> {

    List<HydraAlvo> findByHydraAtaque_Id(Integer hydraAtaqueId);
}
