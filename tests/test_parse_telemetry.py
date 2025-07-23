"""Unit tests for the telemetry parsing script."""
import csv
import os
import importlib


def test_parse_telemetry(tmp_path):
    """Ensure telemetry JSON is normalised to CSV with expected rows."""
    parse_mod = importlib.import_module('telemetry.parse_telemetry')
    # Use the built-in sample stream
    sample_json = os.path.join(os.path.dirname(__file__), '..', 'telemetry', 'sample_stream.json')
    out_csv = tmp_path / "event_log.csv"
    parse_mod.parse_stream(sample_json, out_csv)
    assert out_csv.exists(), "CSV output should be created"
    # There are two events each with multiple keys; count rows accordingly
    with open(out_csv, 'r', encoding='utf-8') as f:
        reader = list(csv.DictReader(f))
    assert len(reader) >= 4, "Parsed CSV should contain at least four rows for two events"