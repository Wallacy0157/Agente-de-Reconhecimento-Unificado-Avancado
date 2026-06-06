package com.ucb.agente_reconhecimento.repository;

import com.ucb.agente_reconhecimento.domain.entities.osint.Osint;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;

public interface OsintRepository extends JpaRepository<Osint, Integer> {

    List<Osint> findTop100ByExecucao_Projeto_Usuario_IdOrderByCriadoEmDesc(Integer usuarioId);
}
