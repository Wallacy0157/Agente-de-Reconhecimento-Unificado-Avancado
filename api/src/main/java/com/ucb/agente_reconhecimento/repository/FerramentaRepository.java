package com.ucb.agente_reconhecimento.repository;

import com.ucb.agente_reconhecimento.domain.entities.Ferramenta;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.Optional;

public interface FerramentaRepository extends JpaRepository<Ferramenta, Integer> {

    Optional<Ferramenta> findByNome(String nome);

}
