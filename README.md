# AURA - Agente de Reconhecimento Unificado Avançado

AURA é uma interface de auditoria e aprendizado em segurança que reúne ferramentas de reconhecimento, OSINT, teste de credenciais, auditoria local e relatórios em um único painel.

> Use somente em sistemas próprios, laboratórios ou ambientes onde você tem autorização explícita.

## Recursos

- Varredura de rede com relatórios e envio de alvos vulneráveis para o Hydra.
- Sherlock para investigação OSINT por nickname ou nome completo.
- Hydra para testes autorizados de credenciais.
- John the Ripper para análise de hashes em laboratório.
- Auditor de teclado para estudos controlados de captura local.
- Teste de carga, auditoria de segurança local, histórico e central de logs.
- Tema claro/escuro e cor neon configurável.

## Requisitos

- Python 3.12 ou superior.
- Nmap instalado para a varredura de rede.
- Ferramentas externas opcionais conforme o módulo usado, como Hydra e John the Ripper.
- Docker, caso queira executar o backend com banco de dados.

## Instalar a interface

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python security_toolkit.py
```

No Windows, ative o ambiente com:

```powershell
.venv\Scripts\activate
python security_toolkit.py
```

## Backend opcional

O projeto inclui uma API Java/Spring e um banco PostgreSQL para persistir alguns resultados.

```bash
docker compose up --build
```

A API fica em `http://localhost:8080` e o Adminer em `http://localhost:8081`.

## Estrutura principal

- `security_toolkit.py`: interface principal do AURA.
- `core/`: motores das ferramentas, estilos e componentes compartilhados.
- `services/`: clientes para comunicação com a API.
- `languages/`: traduções e textos informativos.
- `logs/`: relatórios e registros gerados localmente.
- `api/`: backend Spring Boot.

## Uso responsável

O AURA foi criado para estudo, auditoria autorizada e defesa. Não use para invadir, monitorar terceiros, testar redes sem permissão ou causar indisponibilidade em sistemas.
