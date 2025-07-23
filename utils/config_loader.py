"""
config_loader.py
-----------------

Common configuration loader for the Æther system.  This module
abstracts away the differences between YAML and JSON formats and
provides a unified interface for retrieving structured configuration
data.  The loader gracefully handles missing files by returning an
empty dictionary and can be extended in the future to merge
environment variable overrides.

Usage:

    from utils.config_loader import load_config
    cfg = load_config('config/mission_profiles.yaml')

The returned object is a Python dict regardless of the input format.
"""

from __future__ import annotations

import json
import yaml  # type: ignore
from typing import Any, Dict
import os


def load_config(path: str) -> Dict[str, Any]:
    """Load a YAML or JSON configuration file.

    Parameters
    ----------
    path : str
        Path to the configuration file.  The file extension must be
        `.yaml`, `.yml` or `.json`.

    Returns
    -------
    dict
        Parsed configuration contents.  Returns an empty dict if the
        file does not exist.

    Raises
    ------
    ValueError
        If the file extension is not supported.
    """
    if not os.path.exists(path):
        return {}
    _, ext = os.path.splitext(path)
    ext = ext.lower()
    with open(path, 'r', encoding='utf-8') as f:
        if ext in {'.yaml', '.yml'}:
            return yaml.safe_load(f) or {}
        if ext == '.json':
            return json.load(f)
        raise ValueError(f"Unsupported config extension: {ext}")


__all__ = ['load_config']