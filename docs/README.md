# Æther Wraith ISR Fleet Documentation

This directory collects high‑level documentation and operational playbooks
for the Æther Wraith ISR fleet.  The goal of this documentation is to
provide new developers and operators with the context necessary to
understand, build and run the system in a variety of environments.  It
complements the inline docstrings and comments found throughout the
repository.

## System Overview

Æther Wraith is a modular intelligence, surveillance and reconnaissance
(ISR) platform designed for distributed sensing.  Its key components
include:

- **Mission generation** (`generate_mission.py` and `missions/`):
  Templates and tools for assembling mission definitions tailored to
  specific objectives and regions.
- **Telemetry ingestion** (`telemetry/`):
  Scripts and sample data for normalising raw sensor output into a
  machine‑friendly CSV format.
- **Orchestration layer** (`orchestrator.py` and `tasks/`):
  A lightweight scheduler that executes time‑triggered tasks and
  orchestrates interactions between components.
- **AI agent** (`agents/aether_ai.py`):
  A placeholder anomaly classifier that flags unusual events within the
  telemetry stream.  A trained model can be substituted by replacing
  `models/anomaly_classifier.joblib`.
- **Simulation harness** (`sim_runner.py`):
  A glue script that ties together mission generation, telemetry
  normalisation, scheduling and AI detection to provide end‑to‑end
  integration testing.

For a more detailed architectural description see the top‑level
`README.md` in the project root (if available) and the docstrings
embedded in each module.

## Development Workflow

1. **Install dependencies**

   Use `pip` to install the pinned requirements listed in
   `requirements.txt`.  These include the core runtime libraries as
   well as development tools such as `pytest`, `black`, `flake8` and
   `mypy`.

   ```bash
   python -m pip install -r requirements.txt
   ```

2. **Run unit tests**

   A small but growing test suite lives under the `tests/` directory.
   Execute all tests with:

   ```bash
   pytest -q
   ```

3. **Check code quality**

   The project uses Flake8 and Black to enforce style and formatting
   conventions.  Use the following commands to check your changes:

   ```bash
   flake8 .
   black --check .
   mypy aether-wraith-isr-fleet
   ```

4. **Run the simulator**

   To validate that all components operate in concert, run the
   simulation harness:

   ```bash
   python sim_runner.py --profile default
   ```

5. **Launch with Docker Compose**

   For a more realistic local environment, use Docker Compose to start
   the MQTT broker, node simulation container and AI service:

   ```bash
   docker-compose up --build
   ```

   Compose reads configuration from `docker-compose.yml` and will use
   environment variables defined in a `.env` file if present.  See
   `.env.example` for a template.

## Operational Playbooks

1. **Adding a new mission profile**

   - Edit `config/mission_profiles.yaml` to define threshold values for
     `max_anomaly_rate`, `min_events` and `max_duration_seconds` under
     a new profile name.
   - Update `mission_success_criteria.json` accordingly under the
     `profiles` key so that the simulator can access the new profile.
   - Run `sim_runner.py --profile your_profile_name` to test the
     mission with the new criteria.

2. **Training a new anomaly classifier**

   - Use your preferred ML toolkit to train a model on normal and
     anomalous events.
   - Export the model using `joblib.dump()` and replace
     `models/anomaly_classifier.joblib` with the new file.
   - Ensure that `agents/aether_ai.py` properly loads and applies the
     model during classification.

3. **Deploying to production**

   - Provision an MQTT broker and ensure that credentials are stored
     outside of source control (for example in environment variables or
     secret managers).
   - Containerise each component using the provided Dockerfiles or your
     own build system.
   - Use a container orchestrator (Docker Compose, Kubernetes, etc.) to
     wire together services and manage their lifecycle.

For further assistance or to contribute improvements, please refer to
the repository’s issue tracker and contribution guidelines.