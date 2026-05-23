package com.ucb.agente_reconhecimento.web.controller;

import com.ucb.agente_reconhecimento.domain.entities.scan.ScanRede;
import com.ucb.agente_reconhecimento.service.ScanService;
import com.ucb.agente_reconhecimento.web.dto.scan.ScanCriadoResponse;
import com.ucb.agente_reconhecimento.web.dto.scan.ScanDetalheResponse;
import com.ucb.agente_reconhecimento.web.dto.scan.ScanResumoResponse;
import com.ucb.agente_reconhecimento.web.dto.scan.ScanResultadoRequest;
import jakarta.validation.Valid;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.oauth2.server.resource.authentication.JwtAuthenticationToken;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RequestMapping("/scans")
@RestController
public class ScanEndpoint {

    private final ScanService scanService;

    public ScanEndpoint(ScanService scanService) {
        this.scanService = scanService;
    }

    @PostMapping
    public ResponseEntity<ScanCriadoResponse> criarScan(
            @RequestBody @Valid ScanResultadoRequest request,
            JwtAuthenticationToken authentication) {

        Integer usuarioId = Integer.parseInt(authentication.getToken().getSubject());
        ScanRede scanRede = scanService.persistirScan(request, usuarioId);

        return ResponseEntity.status(HttpStatus.CREATED)
                .body(new ScanCriadoResponse(scanRede.getId()));
    }

    @GetMapping
    public ResponseEntity<List<ScanResumoResponse>> listarScans(JwtAuthenticationToken authentication) {
        Integer usuarioId = Integer.parseInt(authentication.getToken().getSubject());
        List<ScanResumoResponse> scans = scanService.listarScans(usuarioId);
        return ResponseEntity.ok(scans);
    }

    @GetMapping("/{id}")
    public ResponseEntity<ScanDetalheResponse> buscarScan(
            @PathVariable Integer id,
            JwtAuthenticationToken authentication) {
        Integer usuarioId = Integer.parseInt(authentication.getToken().getSubject());
        ScanDetalheResponse response = scanService.buscarScanPorId(id, usuarioId);
        return ResponseEntity.ok(response);
    }

}
