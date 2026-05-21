package com.ucb.agente_reconhecimento.repository;

import com.ucb.agente_reconhecimento.domain.entities.Usuario;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.Optional;

public interface UsuarioRepository extends JpaRepository<Usuario, Integer> {

    boolean existsByEmail(String email);

    boolean existsByUsername(String username);

    Optional<Usuario> findByEmail(String email);

}
