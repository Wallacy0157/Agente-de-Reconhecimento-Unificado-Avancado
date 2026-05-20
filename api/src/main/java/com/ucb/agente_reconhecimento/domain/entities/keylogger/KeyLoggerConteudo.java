package com.ucb.agente_reconhecimento.domain.entities.keylogger;

import jakarta.persistence.*;
import lombok.*;

@Builder
@NoArgsConstructor
@AllArgsConstructor
@Getter
@Setter
@Entity
public class KeyLoggerConteudo {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer id;

    @ManyToOne(cascade = CascadeType.ALL)
    @JoinColumn(name = "id_key_logger")
    private KeyLogger keyLogger;

    @Column(name = "texto_bruto")
    private String textoBruto;
}
