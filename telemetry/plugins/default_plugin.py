"""
default_plugin
---------------

Fallback parser for telemetry sensors.  When no specific plugin exists for
a given sensor, this module simply returns the raw key/value pairs from
the data dictionary.
"""

from __future__ import annotations

from typing import Dict, Any, Iterable, Tuple


def parse(sensor: str, data: Dict[str, Any]) -> Iterable[Tuple[str, Any]]:
    """Return key/value pairs unchanged."""
    return data.items()