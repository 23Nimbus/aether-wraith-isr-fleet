# Æther Wraith ISR Fleet

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