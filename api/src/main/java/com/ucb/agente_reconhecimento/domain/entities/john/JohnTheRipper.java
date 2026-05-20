package com.ucb.agente_reconhecimento.domain.entities.john;

import com.ucb.agente_reconhecimento.domain.entities.Execucao;
import jakarta.persistence.*;
import lombok.*;

@Builder
@NoArgsConstructor
@AllArgsConstructor
@Getter
@Setter
@Entity
public class JohnTheRipper {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer id;

    @ManyToOne(cascade = CascadeType.ALL)
    @JoinColumn(name = "id_execucao")
    private Execucao execucao;

    @Column(name = "status")
    private String status;

    @Column(name = "hash_alvo")
    private String hashAlvo;

    @Column(name = "algoritmo")
    private String algoritmo;

    @Column(name = "salt")
    private String salt;

    @Column(name = "senha_encontrada")
    private String senhaEncontrada;

    @Column(name = "modo_ataque")
    private String modoAtaque;

    @Column(name = "hashes_testados")
    private Integer hashesTestados;

}
