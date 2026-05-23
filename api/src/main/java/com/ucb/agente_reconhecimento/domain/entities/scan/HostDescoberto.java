package com.ucb.agente_reconhecimento.domain.entities.scan;

import com.ucb.agente_reconhecimento.domain.entities.EntidadeAuditavel;
import jakarta.persistence.*;
import lombok.*;

@Builder
@NoArgsConstructor
@AllArgsConstructor
@Getter
@Setter
@Entity
public class HostDescoberto extends EntidadeAuditavel {

    @ManyToOne(cascade = CascadeType.ALL)
    @JoinColumn(name = "id_scan_rede")
    private ScanRede scanRede;

    @Column(name = "ip")
    private String ip;

    @Column(name = "os_detectado")
    private String osDetectado;

    @Column(name = "erro")
    private String erro;

    @Column(name = "tem_web")
    private boolean temWeb;

    @Column(name = "tem_database")
    private boolean temDatabase;

    @Column(name = "tem_acesso_remoto")
    private boolean temAcessoRemoto;

    @Column(name = "tem_servico_auth")
    private boolean temServicoAuth;
}
