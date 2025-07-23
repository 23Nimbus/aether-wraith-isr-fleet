# Æther Wraith ISR Fleet

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
