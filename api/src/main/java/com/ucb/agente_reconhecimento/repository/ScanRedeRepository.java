package com.ucb.agente_reconhecimento.repository;

import com.ucb.agente_reconhecimento.domain.entities.scan.ScanRede;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;

public interface ScanRedeRepository extends JpaRepository<ScanRede, Integer> {

    List<ScanRede> findByExecucao_Projeto_Usuario_IdOrderByExecucao_InicioDesc(Integer usuarioId);

}
