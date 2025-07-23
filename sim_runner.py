#!/usr/bin/env python3
"""
sim_runner.py
-------------

This script simulates execution of a mission in a controlled environment.  It
leverages other components of the Æther Wraith ISR fleet – namely the
orchestrator, telemetry parser and AI agent – to produce a rudimentary run
score.  The simulator is not a physics‑based model; rather, it wires
together the existing tooling to demonstrate end‑to‑end integration.

The simulator performs the following high‑level steps:

1.  Optionally compile a mission from a template if the user supplies a
    high‑level description (see ``generate_mission.py`` for details).
2.  Normalise a telemetry sample into a CSV event log using
    ``telemetry/parse_telemetry.py``.
3.  Invoke the orchestrator to execute any scheduled tasks.
4.  Run the anomaly classifier over the resulting event log.
5.  Evaluate run performance against thresholds defined in
    ``mission_success_criteria.json``.

Use this tool during development to validate that all subcomponents are
correctly wired together.  It is not intended to replace full system tests
or hardware‑in‑the‑loop simulations.
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import subprocess
import sys
from typing import Tuple

import yaml  # type: ignore
from utils.logging_utils import setup_logging, get_logger
from utils.config_loader import load_config


HERE = os.path.dirname(__file__)
CRITERIA_PATH = os.path.join(HERE, 'mission_success_criteria.json')
EVENT_LOG_PATH = os.path.join(HERE, 'telemetry', 'event_log.csv')

# Initialise logging once for the simulator.  Using the shared logging
# configuration ensures consistency with other modules.
setup_logging()
logger = get_logger(__name__)


def run_telemetry_parser() -> None:
    """Run the telemetry parser to generate a fresh event log."""
    parser_script = os.path.join(HERE, 'telemetry', 'parse_telemetry.py')
    sample_stream = os.path.join(HERE, 'telemetry', 'sample_stream.json')
    subprocess.check_call([
        sys.executable,
        parser_script,
        '--input', sample_stream,
        '--output', EVENT_LOG_PATH,
    ])


def run_orchestrator() -> None:
    """Execute the orchestrator to process scheduled tasks."""
    orchestrator_script = os.path.join(HERE, 'orchestrator.py')
    subprocess.check_call([sys.executable, orchestrator_script])


def evaluate_run(criteria_data: dict) -> Tuple[float, bool]:
    """Evaluate the simulation outcome against mission success criteria.

    This function computes the anomaly rate for the current event log and
    compares it against the provided threshold dictionary.  The expected keys
    in ``criteria_data`` are ``max_anomaly_rate`` and ``min_events``.

    Parameters
    ----------
    criteria_data : dict
        A dictionary of thresholds defining pass criteria.

    Returns
    -------
    tuple of (anomaly_rate, pass)
        The computed anomaly rate and a boolean indicating whether the run
        satisfies the provided criteria.
    """
    try:
        from agents import aether_ai  # type: ignore
    except ImportError:
        print("[SimRunner] Error: AI agent not available.")
        return (0.0, False)
    total = 0
    anomalies = 0
    # Process the event log and use the same classifier as the AI agent
    with open(EVENT_LOG_PATH, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            total += 1
            if aether_ai.classify(row) == 'anomaly':
                anomalies += 1
    anomaly_rate = anomalies / total if total else 0.0
    max_rate = criteria_data.get('max_anomaly_rate', 1.0)
    min_events = criteria_data.get('min_events', 0)
    passed = anomaly_rate <= max_rate and total >= min_events
    return (anomaly_rate, passed)


def load_mission(path: str) -> dict:
    """Load a mission file for informational purposes.

    The simulator currently does not use the mission contents beyond
    demonstrating that the file can be parsed.
    """
    with open(path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def main() -> None:
    parser = argparse.ArgumentParser(description='Run an end‑to‑end simulation of the ISR fleet.')
    parser.add_argument(
        '--mission',
        help='Path to a compiled mission YAML file.  If omitted, the default template is used.',
        default=os.path.join(HERE, 'missions', 'mission_template.yaml'),
    )
    parser.add_argument(
        '--criteria',
        help='Path to mission success criteria JSON.',
        default=CRITERIA_PATH,
    )
    parser.add_argument(
        '--profile',
        help='Named profile within the criteria file to use (default or high_priority)',
        default='default',
    )
    args = parser.parse_args()

    # Load mission for completeness; not used further in this simple simulation.
    mission = load_mission(args.mission)
    logger.info(
        "Loaded mission: %s",
        mission.get('mission', {}).get('objective', 'unspecified objective'),
    )

    # Step 1: normalise telemetry
    logger.info("Generating event log from sample telemetry...")
    run_telemetry_parser()

    # Step 2: run orchestrator to invoke tasks and AI detection
    logger.info("Running orchestrator...")
    run_orchestrator()

    # Step 3: evaluate outcome
    # Load criteria from file and select the requested profile if available
    # Load criteria from file using the generic configuration loader
    criteria_doc = load_config(args.criteria)
    profile_data = criteria_doc.get('profiles', {}).get(args.profile, {})
    anomaly_rate, passed = evaluate_run(profile_data)
    logger.info("Anomaly rate: %.2f%%", anomaly_rate * 100)
    logger.info("Success criteria met: %s", passed)


if __name__ == '__main__':
    main()