"""
camera
------

Example plugin for a ``camera`` sensor.  This parser demonstrates how
sensor‑specific logic can be encapsulated within a plugin.  Here we
standardise a ``resolution`` field into a pixel count and preserve
other fields unchanged.
"""

from __future__ import annotations

from typing import Dict, Any, Iterable, Tuple


def parse(sensor: str, data: Dict[str, Any]) -> Iterable[Tuple[str, Any]]:
    for key, value in data.items():
        if key == 'resolution' and isinstance(value, str):
            # Convert resolution like "1920x1080" into pixel count
            try:
                width, height = (int(x) for x in value.lower().split('x'))
                yield ('resolution_px', width * height)
            except Exception:
                # Fallback to raw resolution string
                yield ('resolution', value)
        else:
            yield (key, value)