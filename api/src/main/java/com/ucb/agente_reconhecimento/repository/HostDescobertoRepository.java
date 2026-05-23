package com.ucb.agente_reconhecimento.repository;

import com.ucb.agente_reconhecimento.domain.entities.scan.HostDescoberto;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;

public interface HostDescobertoRepository extends JpaRepository<HostDescoberto, Integer> {

    List<HostDescoberto> findByScanRede_Id(Integer scanRedeId);
}
