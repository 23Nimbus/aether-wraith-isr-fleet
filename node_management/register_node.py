#!/usr/bin/env python3
"""
register_node.py
-----------------

Utility for registering a new autonomous node with the Æther system.  The
registered node list is stored in ``nodes/registered_nodes.yaml`` and
can be used by orchestration and deployment tools to discover available
platforms.  Each entry records basic metadata including node ID,
platform type, location and available sensors.

Example:

    python node_management/register_node.py --id NODE-001 \
        --type quadcopter --location "Lat,Long" --sensors camera lidar

Upon execution the script will append the node definition to the YAML
document, creating it if it does not exist.  The log emitted will
indicate success and the number of nodes registered.
"""

from __future__ import annotations

import argparse
import os
import yaml  # type: ignore
from typing import List, Dict, Any

from utils.logging_utils import get_logger
from .secret_manager import store_secret

logger = get_logger(__name__)


def load_nodes(path: str) -> List[Dict[str, Any]]:
    """Load the list of registered nodes from YAML."""
    if not os.path.exists(path):
        return []
    with open(path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f) or []


def save_nodes(path: str, nodes: List[Dict[str, Any]]) -> None:
    """Persist the list of nodes back to YAML."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        yaml.safe_dump(nodes, f, sort_keys=False)


def main() -> None:
    parser = argparse.ArgumentParser(description='Register a new autonomous node.')
    parser.add_argument('--id', required=True, help='Unique identifier for the node')
    parser.add_argument('--type', default='generic', help='Platform type (e.g. quadcopter, rover)')
    parser.add_argument('--location', default='unspecified', help='Location string (lat,long or descriptive)')
    parser.add_argument('--sensors', nargs='+', default=['camera'], help='List of sensors equipped on the node')
    parser.add_argument('--role', default='observer', help='Role or capability tier for the node (e.g. observer, commander)')
    parser.add_argument('--secret', help='Secret token to associate with this node')
    args = parser.parse_args()

    # Determine the path to the registry file relative to this script
    repo_root = os.path.dirname(os.path.dirname(__file__))
    registry_path = os.path.join(repo_root, 'nodes', 'registered_nodes.yaml')

    nodes = load_nodes(registry_path)
    node_entry = {
        'id': args.id,
        'type': args.type,
        'location': args.location,
        'sensors': args.sensors,
        'role': args.role,
    }
    nodes.append(node_entry)
    save_nodes(registry_path, nodes)
    # If a secret is provided, store it separately via the secret manager
    if args.secret:
        store_secret(args.id, args.secret)
    logger.info(
        'Registered node %s (%s) with role %s and sensors %s. Total nodes: %d',
        args.id,
        args.type,
        args.role,
        ','.join(args.sensors),
        len(nodes),
    )


if __name__ == '__main__':
    main()