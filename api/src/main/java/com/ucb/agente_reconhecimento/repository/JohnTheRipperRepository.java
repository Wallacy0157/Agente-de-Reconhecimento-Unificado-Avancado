package com.ucb.agente_reconhecimento.repository;

import com.ucb.agente_reconhecimento.domain.entities.john.JohnTheRipper;
import org.springframework.data.jpa.repository.JpaRepository;

public interface JohnTheRipperRepository extends JpaRepository<JohnTheRipper, Integer> {
}