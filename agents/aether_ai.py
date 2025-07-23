#!/usr/bin/env python3
"""
aether_ai.py
-------------

This module defines a simple AI overlay for the Æther Wraith ISR Fleet.
It reads normalised telemetry from ``telemetry/event_log.csv``, classifies
potential anomalies, and triggers mission adjustments via the message bus.

In this stub implementation the classifier is random and always returns
"normal" except for a small probability of flagging an event as anomalous.
Replace the :func:`classify` function with a call to a trained model
(``models/anomaly_classifier.joblib``) to implement real anomaly detection.
"""

import csv
import os
import random
from utils.logging_utils import get_logger, setup_logging
from .model_manager import get_model


def classify(event: dict, model: object | None = None) -> str:
    """Classify an event as 'normal' or 'anomaly'.

    If a trained model is supplied, this function will attempt to call
    its ``predict`` method with the event features.  Otherwise a dummy
    classifier is used that returns 'anomaly' with a small probability.

    Parameters
    ----------
    event : dict
        Event with keys ``timestamp``, ``node_id``, ``sensor``, ``key`` and ``value``.
    model : object or None, optional
        A scikit‑learn style model with a ``predict`` method.  If None,
        random classification is performed.

    Returns
    -------
    str
        Classification label: ``'normal'`` or ``'anomaly'``.
    """
    if model is not None and hasattr(model, 'predict'):
        # Convert the event into a feature vector.  For now we use the
        # sensor value as a numeric feature when possible.
        try:
            value = float(event['value'])
        except Exception:
            value = 0.0
        prediction = model.predict([[value]])
        return 'anomaly' if prediction[0] == 1 else 'normal'
    # Dummy fallback classifier
    return 'anomaly' if random.random() < 0.05 else 'normal'


def process_event_log(path: str, profile: str = 'default') -> None:
    """Iterate over events and emit anomaly notifications using a profile.

    Parameters
    ----------
    path : str
        Path to the CSV file containing normalised telemetry.
    profile : str, optional
        Name of the model profile to use.  Defaults to ``'default'``.
    """
    # Configure a logger for the AI module.  Use the shared logging
    # utilities so that environment‑wide settings (e.g. JSON output) are
    # honoured without duplicating configuration.
    setup_logging()
    logger = get_logger(__name__)
    model = get_model(profile)
    with open(path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            label = classify(row, model)
            if label == 'anomaly':
                logger.warning(
                    "Anomaly detected at %s on node %s sensor %s -> %s=%s",
                    row['timestamp'],
                    row['node_id'],
                    row['sensor'],
                    row['key'],
                    row['value'],
                )


def main() -> None:
    """Entry point for command‑line execution of the AI agent."""
    import argparse
    parser = argparse.ArgumentParser(description='Run the anomaly detection agent.')
    parser.add_argument('--profile', default='default', help='Model profile to use')
    parser.add_argument('--log', default=None, help='Path to event log CSV (defaults to telemetry/event_log.csv)')
    args = parser.parse_args()
    event_log_path = args.log or os.path.join(
        os.path.dirname(__file__), '..', 'telemetry', 'event_log.csv'
    )
    process_event_log(event_log_path, profile=args.profile)


if __name__ == '__main__':
    main()