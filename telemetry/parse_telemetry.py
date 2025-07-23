#!/usr/bin/env python3
"""
parse_telemetry.py
-------------------

This script normalises raw telemetry JSON into a flat CSV suitable for
downstream analysis or ingestion by ML models.  It reads a stream of
telemetry events from `telemetry/sample_stream.json` (or a user‑specified
file) and writes a CSV file called `telemetry/event_log.csv` with the
following columns:

- `timestamp`: ISO 8601 timestamp of the event
- `node_id`: identifier of the emitting node
- `sensor`: name of the sensor module
- `key`: data field name
- `value`: data field value

Usage:

```bash
python telemetry/parse_telemetry.py --input telemetry/sample_stream.json
```
"""
import argparse
import json
import csv
import os

DEFAULT_INPUT = os.path.join(os.path.dirname(__file__), 'sample_stream.json')
DEFAULT_OUTPUT = os.path.join(os.path.dirname(__file__), 'event_log.csv')

def parse_stream(input_path: str, output_path: str) -> None:
    with open(input_path, 'r', encoding='utf-8') as f:
        events = json.load(f)
    with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['timestamp', 'node_id', 'sensor', 'key', 'value'])
        for event in events:
            ts = event.get('timestamp')
            node_id = event.get('node_id')
            sensor = event.get('sensor')
            data = event.get('data', {})
            for key, value in data.items():
                writer.writerow([ts, node_id, sensor, key, value])

def main() -> None:
    parser = argparse.ArgumentParser(description='Normalise telemetry JSON into CSV.')
    parser.add_argument('--input', default=DEFAULT_INPUT, help='Path to the input JSON file')
    parser.add_argument('--output', default=DEFAULT_OUTPUT, help='Path to the output CSV file')
    args = parser.parse_args()
    parse_stream(args.input, args.output)
    print(f"Event log written to {args.output}")

if __name__ == '__main__':
    main()