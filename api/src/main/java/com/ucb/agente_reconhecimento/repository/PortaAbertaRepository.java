package com.ucb.agente_reconhecimento.repository;

import com.ucb.agente_reconhecimento.domain.entities.scan.PortaAberta;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;

public interface PortaAbertaRepository extends JpaRepository<PortaAberta, Integer> {

    List<PortaAberta> findByHostDescoberto_Id(Integer hostDescobertoId);
}
