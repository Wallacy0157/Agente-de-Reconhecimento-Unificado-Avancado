package com.ucb.agente_reconhecimento.web.controller;

import com.ucb.agente_reconhecimento.domain.entities.stress.TesteStress;
import com.ucb.agente_reconhecimento.service.StressService;
import com.ucb.agente_reconhecimento.web.dto.stress.StressTestCriadoResponse;
import com.ucb.agente_reconhecimento.web.dto.stress.StressTestDetalheResponse;
import com.ucb.agente_reconhecimento.web.dto.stress.StressTestResumoResponse;
import com.ucb.agente_reconhecimento.web.dto.stress.StressTestResultadoRequest;
import jakarta.validation.Valid;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.oauth2.server.resource.authentication.JwtAuthenticationToken;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RequestMapping("/stress-tests")
@RestController
public class StressEndpoint {

    private final StressService stressService;

    public StressEndpoint(StressService stressService) {
        this.stressService = stressService;
    }

    @PostMapping
    public ResponseEntity<StressTestCriadoResponse> criarStressTest(
            @RequestBody @Valid StressTestResultadoRequest request,
            JwtAuthenticationToken authentication) {

        Integer usuarioId = Integer.parseInt(authentication.getToken().getSubject());
        TesteStress testeStress = stressService.persistirStressTest(request, usuarioId);

        return ResponseEntity.status(HttpStatus.CREATED)
                .body(new StressTestCriadoResponse(testeStress.getId()));
    }

    @GetMapping
    public ResponseEntity<List<StressTestResumoResponse>> listarStressTests(
            JwtAuthenticationToken authentication) {

        Integer usuarioId = Integer.parseInt(authentication.getToken().getSubject());
        List<StressTestResumoResponse> testes = stressService.listarStressTests(usuarioId);
        return ResponseEntity.ok(testes);
    }

    @GetMapping("/{id}")
    public ResponseEntity<StressTestDetalheResponse> buscarStressTest(
            @PathVariable Integer id,
            JwtAuthenticationToken authentication) {

        Integer usuarioId = Integer.parseInt(authentication.getToken().getSubject());
        StressTestDetalheResponse response = stressService.buscarStressTestPorId(id, usuarioId);
        return ResponseEntity.ok(response);
    }
}
