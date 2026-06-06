package com.ucb.agente_reconhecimento.repository;

import com.ucb.agente_reconhecimento.domain.entities.hydra.HydraCredencialEncontrada;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;

public interface HydraCredencialEncontradaRepository extends JpaRepository<HydraCredencialEncontrada, Integer> {

    List<HydraCredencialEncontrada> findByHydraAtaque_Id(Integer hydraAtaqueId);
}
