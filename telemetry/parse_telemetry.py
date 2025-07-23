#!/usr/bin/env python3
"""
parse_telemetry.py
-------------------

This script normalises raw telemetry JSON into a flat CSV suitable for
downstream analysis or ingestion by ML models.  It reads a stream of
telemetry events from ``telemetry/sample_stream.json`` (or a user‑specified
file) and writes a CSV file called ``telemetry/event_log.csv`` with the
following columns:

``timestamp``
    ISO 8601 timestamp of the event.
``node_id``
    Identifier of the emitting node.
``sensor``
    Name of the sensor module.
``key``
    Data field name.
``value``
    Data field value.

Usage:

```bash
python telemetry/parse_telemetry.py --input telemetry/sample_stream.json
```
"""

import argparse
import json
import csv
import os
from utils.logging_utils import get_logger, setup_logging
# Import the plugin loader using an absolute import so that both package
# imports and direct script execution work correctly.  When run as a
# script __package__ is None and relative imports fail, so we avoid
# leading dots here.
from telemetry.plugins import load_plugins  # type: ignore
from telemetry.plugins.default_plugin import parse as default_parse  # type: ignore

# Default input and output paths.  These are resolved relative to this
# script so that it works whether executed from the project root or within
# the ``aether-wraith-isr-fleet`` directory.
DEFAULT_INPUT = os.path.join(os.path.dirname(__file__), 'sample_stream.json')
DEFAULT_OUTPUT = os.path.join(os.path.dirname(__file__), 'event_log.csv')

# Configure a basic logger for the telemetry parser.  The shared logging
# utilities centralise configuration and support JSON output via the
# AE_LOG_JSON environment variable.
setup_logging()
logger = get_logger(__name__)


def parse_stream(input_path: str, output_path: str) -> None:
    """Read events from ``input_path`` and write a normalised CSV to ``output_path``."""
    with open(input_path, 'r', encoding='utf-8') as f:
        events = json.load(f)
    # Load sensor plugins once per invocation.  The returned mapping
    # associates sensor names with parsing functions.
    plugins = load_plugins()
    # Write normalised events to CSV.  Create the directory if missing.
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['timestamp', 'node_id', 'sensor', 'key', 'value'])
        for event in events:
            ts = event.get('timestamp')
            node_id = event.get('node_id')
            sensor = event.get('sensor')
            data = event.get('data', {})
            # Select appropriate parser based on sensor name; fall back to default
            parser = plugins.get(sensor, default_parse)
            for key, value in parser(sensor, data):
                writer.writerow([ts, node_id, sensor, key, value])


def main() -> None:
    """Parse command‑line arguments and normalise a telemetry stream."""
    parser = argparse.ArgumentParser(description='Normalise telemetry JSON into CSV.')
    parser.add_argument('--input', default=DEFAULT_INPUT, help='Path to the input JSON file')
    parser.add_argument('--output', default=DEFAULT_OUTPUT, help='Path to the output CSV file')
    args = parser.parse_args()
    parse_stream(args.input, args.output)
    logger.info("Event log written to %s", args.output)


if __name__ == '__main__':
    main()