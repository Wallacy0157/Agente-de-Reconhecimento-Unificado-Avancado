package com.ucb.agente_reconhecimento.repository;

import com.ucb.agente_reconhecimento.domain.entities.osint.OsintResultado;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;

public interface OsintResultadoRepository extends JpaRepository<OsintResultado, Integer> {

    List<OsintResultado> findByOsint_Id(Integer osintId);
}
