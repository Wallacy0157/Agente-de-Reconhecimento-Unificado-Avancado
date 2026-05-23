package com.ucb.agente_reconhecimento.repository;

import com.ucb.agente_reconhecimento.domain.entities.scan.SugestaoTeste;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;

public interface SugestaoTesteRepository extends JpaRepository<SugestaoTeste, Integer> {

    List<SugestaoTeste> findByHostDescoberto_Id(Integer hostDescobertoId);
}
