package com.ucb.agente_reconhecimento;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

import java.util.Objects;

@SpringBootApplication
public class AgenteReconhecimentoApplication {

	public static void main(String[] args) {
		SpringApplication springApplication = new SpringApplication(AgenteReconhecimentoApplication.class);

		String profileActive = System.getenv("SPRING_PROFILE_ACTIVE");
		springApplication.setAdditionalProfiles(Objects.requireNonNullElse(profileActive, "local"));

		springApplication.run(args);
	}

}
