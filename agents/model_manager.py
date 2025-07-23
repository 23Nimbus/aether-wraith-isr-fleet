"""
model_manager.py
----------------

Utility functions for loading and managing anomaly detection models.  The
model manager supports per‑profile models stored in the ``models/``
directory.  Models are loaded lazily and cached in memory.  To update
models at runtime, call ``reload_models()`` to clear the cache; the next
invocation of ``get_model()`` will reload the model from disk.

This abstraction allows the AI agent to support multiple missions with
different anomaly classifiers and provides a hook for future streaming
model updates.
"""

from __future__ import annotations

import os
import joblib  # type: ignore
from typing import Dict, Any
from utils.logging_utils import get_logger

logger = get_logger(__name__)

_model_cache: Dict[str, Any] = {}


def _model_path(profile: str) -> str:
    """Construct the expected filename for a profile's model."""
    here = os.path.dirname(os.path.dirname(__file__))
    return os.path.join(here, 'models', f'{profile}_anomaly_classifier.joblib')


def get_model(profile: str = 'default') -> Any:
    """Load and return the anomaly model for a given profile.

    If the model has been loaded previously it will be returned from the
    cache.  If no model exists for the profile the default model is used
    if available, otherwise ``None`` is returned.
    """
    if profile in _model_cache:
        return _model_cache[profile]
    path = _model_path(profile)
    if not os.path.exists(path):
        # Fallback to default model
        if profile != 'default':
            logger.warning('Model for profile %s not found, falling back to default', profile)
            return get_model('default')
        else:
            logger.error('Default anomaly model not found at %s', path)
            return None
    try:
        model = joblib.load(path)
        _model_cache[profile] = model
        logger.info('Loaded anomaly model for profile %s', profile)
        return model
    except Exception as exc:
        logger.error('Failed to load model %s: %s', path, exc)
        return None


def reload_models() -> None:
    """Clear the model cache forcing models to be reloaded on next access."""
    _model_cache.clear()
    logger.info('Cleared anomaly model cache')


__all__ = ['get_model', 'reload_models']