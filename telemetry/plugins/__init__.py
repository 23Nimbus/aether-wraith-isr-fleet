# Package initialiser for telemetry plugins.

"""
Telemetry Plugins
-----------------

This package hosts sensor‑specific parsers for telemetry normalisation.  Each
plugin module should define a `parse(sensor: str, data: dict) -> list[tuple[str, any]]`
function that takes the sensor name and its raw data dictionary and
returns an iterable of key/value pairs to emit in the event log.

The default plugin falls back to returning the raw data unchanged.  New
plugins can be added by creating a module named after the sensor (e.g.
``camera.py`` for a ``camera`` sensor) and implementing the ``parse``
function.
"""

from __future__ import annotations

from importlib import import_module
from typing import Callable, Dict, Tuple, Any, Iterable
import os


def load_plugins() -> Dict[str, Callable[[str, Dict[str, Any]], Iterable[Tuple[str, Any]]]]:
    """Dynamically load sensor plugins from this package.

    Returns a mapping from sensor name to a parsing function.  If a
    module matching the sensor name cannot be found the default parser
    is used.
    """
    plugins: Dict[str, Callable[[str, Dict[str, Any]], Iterable[Tuple[str, Any]]]] = {}
    pkg_dir = os.path.dirname(__file__)
    for filename in os.listdir(pkg_dir):
        if filename.startswith('_') or not filename.endswith('.py'):
            continue
        name = filename[:-3]
        module = import_module(f'.{name}', package=__name__)
        if hasattr(module, 'parse'):
            plugins[name] = getattr(module, 'parse')
    return plugins


__all__ = ['load_plugins']