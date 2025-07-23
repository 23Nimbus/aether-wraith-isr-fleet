"""
secret_manager.py
-----------------

Simple secret storage for node credentials.  Secrets are stored in a
JSON file on disk to avoid hardcoding sensitive data into version
control.  In a production deployment this mechanism should be replaced
with an external secrets manager or hardware security module.
"""

from __future__ import annotations

import json
import os
from typing import Any, Dict, Optional
from utils.logging_utils import get_logger

logger = get_logger(__name__)


def _get_secrets_path() -> str:
    """Return the path to the secrets file from environment or default."""
    root = os.path.dirname(os.path.dirname(__file__))
    filename = os.getenv('NODE_SECRET_FILE', os.path.join(root, 'node_management', 'secrets.json'))
    return filename


def _load_secrets() -> Dict[str, Any]:
    path = _get_secrets_path()
    if not os.path.exists(path):
        return {}
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f) or {}


def _save_secrets(secrets: Dict[str, Any]) -> None:
    path = _get_secrets_path()
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(secrets, f, indent=2)


def store_secret(node_id: str, token: str) -> None:
    """Store a secret token for a node.

    Parameters
    ----------
    node_id : str
        Node identifier.
    token : str
        Secret token to associate with the node.
    """
    secrets = _load_secrets()
    secrets[node_id] = token
    _save_secrets(secrets)
    logger.info('Stored secret for node %s', node_id)


def get_secret(node_id: str) -> Optional[str]:
    """Retrieve the secret token for a node if available."""
    secrets = _load_secrets()
    return secrets.get(node_id)


__all__ = ['store_secret', 'get_secret']