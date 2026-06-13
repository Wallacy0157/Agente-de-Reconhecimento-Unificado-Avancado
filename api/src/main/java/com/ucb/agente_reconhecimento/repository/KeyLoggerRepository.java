package com.ucb.agente_reconhecimento.repository;

import com.ucb.agente_reconhecimento.domain.entities.keylogger.KeyLogger;
import org.springframework.data.jpa.repository.JpaRepository;

public interface KeyLoggerRepository extends JpaRepository<KeyLogger, Integer> {
}