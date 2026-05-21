#!/bin/bash
set -e

echo "[2/2] Iniciando API Spring Boot..."
cd api && ./mvnw spring-boot:run
