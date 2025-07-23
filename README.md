# Æther Wraith ISR Fleet

<<<<<<< HEAD
This repository houses the code and configuration needed to build and operate a scalable Intelligence, Surveillance & Reconnaissance (ISR) drone fleet.  The project is designed to be agent‑driven: every task leaves behind a verifiable artefact so that the system’s state can be audited and reproduced.

## Project structure

The repository is organised into logical domains:

| Directory/File | Purpose |
|---|---|
| `.env` | Placeholder for environment variables – **never** commit secrets. |
| `.gitignore` | Standard ignore patterns for Python, virtual environments, telemetry logs and generated files. |
| `.github/workflows/deploy.yml` | GitHub Actions workflow that performs basic CI and deployment steps. |
| `git_hooks/` | Client‑side Git hooks for linting and commit message enforcement. |
| `missions/mission_template.yaml` | YAML blueprint for ISR missions that can be filled in to produce concrete mission files. |
| `generate_mission.py` | Script to compile missions from a prompt and the mission template. |
| `telemetry/` | Telemetry sample data and parser stubs for normalisation into `event_log.csv`. |
| `docker/node_sim.dockerfile` | Dockerfile used to build a simulated node container that replays telemetry and responds to mission control. |
| `comms/` | Scripts and configuration for starting the message bus and describing network topology. |
| `agents/aether_ai.py` | Skeleton AI agent that analyses telemetry and flags anomalies. |
| `tasks/schedule.yaml` | Cron‑style triggers for orchestrated tasks. |
| `orchestrator.py` | Entrypoint for loading scheduled tasks and routing them to the appropriate agent. |
| `sim_runner.py` | Simple simulation harness that executes a mission and scores the result against success criteria. |
| `aether.system_report.json` | Generated system report describing the local development environment. |
| `aether.checksum.sha256` | Tamper‑evident hash over repository artefacts. |
| `ci.status` | Output summarising the last CI check – created by the CI pipeline. |

## Getting started

1.  Create and activate a Python virtual environment:
    ```bash
    python -m venv .venv
    source .venv/bin/activate
    ```

2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3.  Generate a system report:
    ```bash
    python scripts/generate_system_report.py
    ```

4.  Run the orchestrator:
    ```bash
    python orchestrator.py
    ```

The detailed operational blueprint is documented in `docs/concept.md` and the associated playbooks.  Each script and configuration file contains inline documentation explaining its role in the overall system.
=======
Æther Wraith is a modular intelligence, surveillance and reconnaissance (ISR)
platform designed to coordinate autonomous agents, sensor nodes and
analytics across distributed environments.  Its architecture emphasises
intentional execution, modularity, verifiable outputs and platform
agnosticism.  The repository contains the building blocks for task
orchestration, telemetry normalisation, simulation replay and anomaly
detection.

## Project Structure

- `generate_mission.py` – CLI tool to create mission files from
  templates.
- `missions/` – Mission templates and compiled missions.
- `telemetry/` – Scripts and sample data for parsing raw telemetry
  into a normalised CSV event log.
- `tasks/` – Schedule definitions for the orchestrator.
- `orchestrator.py` – Lightweight scheduler that triggers actions at
  predefined times and invokes the anomaly detector.
- `agents/` – AI components including a stub anomaly classifier.
- `sim_runner.py` – End‑to‑end simulation harness tying together
  mission generation, telemetry parsing, scheduling and anomaly
  detection.
- `utils/` – Shared utilities for configuration loading and logging.
- `node_management/` – Tools for registering autonomous nodes.
- `nodes/` – Registered node registry.
- `docker/`, `docker-compose.yml` – Container definitions for local
  simulation and service orchestration.
- `docs/` – Developer and operator documentation.

## Operating Principles

Æther Wraith adheres to the following principles:

1. **Intentional Execution** – All actions derive from authenticated user
   instruction and inherit context from prior phases.
2. **Modularity First** – Every function, script and schema is isolated,
   portable and interoperable.
3. **Verifiable Output** – No task is complete unless it produces an
   artefact that can be parsed, replayed, hashed or audited.
4. **System Agnosticism** – The platform deploys across cloud, edge and
   hybrid infrastructure without vendor lock‑in or protocol constraint.
5. **Autonomy with Oversight** – Automated routines emit structured logs
   and support both scheduled and operator‑invoked interventions.

For detailed usage instructions and operational playbooks see
`docs/README.md`.
>>>>>>> 8abbd01 (feat: integrate modular async architecture into ÆTHER platform)
