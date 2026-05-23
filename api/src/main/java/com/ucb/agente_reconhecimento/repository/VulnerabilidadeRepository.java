package com.ucb.agente_reconhecimento.repository;

import com.ucb.agente_reconhecimento.domain.entities.scan.Vulnerabilidade;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;

public interface VulnerabilidadeRepository extends JpaRepository<Vulnerabilidade, Integer> {

    int countByPortaAberta_HostDescoberto_ScanRede_Id(Integer scanRedeId);

    List<Vulnerabilidade> findByPortaAberta_Id(Integer portaAbertaId);
}
