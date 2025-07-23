#!/usr/bin/env python3
"""
generate_mission.py
--------------------

This script reads the mission template defined in
``missions/mission_template.yaml`` and produces a concrete mission file
based on user‑supplied overrides.  It supports command‑line arguments for
the mission objective, target zone and priority tier.  Additional node
overrides may be specified via a JSON or YAML file.  The resulting
mission file is written to the ``missions/`` directory with a timestamped
name.

Example:

```bash
python generate_mission.py --objective "survey target" --zone "GEO-23" \
--priority 2
```
"""

import argparse
import yaml
from datetime import datetime
import json
import os
from utils.logging_utils import setup_logging, get_logger

# Path to the YAML mission template.  This is resolved relative to
# the location of this script so that it works whether executed from
# the project root or the ``aether-wraith-isr-fleet`` directory.
TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), "missions",
"mission_template.yaml")

# Initialise logging for the mission generator.  Using shared logging
setup_logging()
logger = get_logger(__name__)


def load_template() -> dict:
    """Load and return the mission template as a Python dictionary."""
    with open(TEMPLATE_PATH, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def merge_config(
    template: dict,
    objective: str | None,
    zone: str | None,
    priority: int | None,
    overrides: dict | None,
) -> dict:
    """Merge user‑specified parameters into the mission template.

    Parameters
    ----------
    template: dict
        The loaded mission template.
    objective: str | None
        New objective string to replace the template value.
    zone: str | None
        New geographic zone identifier.
    priority: int | None
        Priority tier (lower numbers indicate higher priority).
    overrides: dict | None
        Optional per‑node configuration overrides loaded from a file.

    Returns
    -------
    dict
        A new mission dictionary containing the merged values.
    """
    mission = template.get('mission', {}).copy()
    if objective:
        mission['objective'] = objective
    if zone:
        mission['target_zone'] = zone
    if priority is not None:
        mission['priority_tier'] = priority
    if overrides:
        node_override = mission.get('node_config_override', {})
        # shallow merge of overrides into default config
        node_override.update(overrides)
        mission['node_config_override'] = node_override
    return {'mission': mission}


def parse_overrides(path: str | None) -> dict | None:
    """Parse a YAML or JSON overrides file if provided."""
    if not path:
        return None
    with open(path, 'r', encoding='utf-8') as f:
        if path.endswith('.json'):
            return json.load(f)
        return yaml.safe_load(f)


def save_mission(mission: dict) -> str:
    """Write the mission definition to a timestamped YAML file and return its path."""
    timestamp = datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')
    outfile = os.path.join(
        os.path.dirname(__file__),
        'missions',
        f'compiled_mission_{timestamp}.yaml',
    )
    with open(outfile, 'w', encoding='utf-8') as f:
        yaml.safe_dump(mission, f, sort_keys=False)
    return outfile


def main() -> None:
    """Entry point for CLI invocation."""
    parser = argparse.ArgumentParser(description='Compile a mission from the template.')
    parser.add_argument('--objective', help='Mission objective')
    parser.add_argument('--zone', help='Target zone identifier')
    parser.add_argument('--priority', type=int, help='Priority tier (1-5)')
    parser.add_argument('--overrides', help='Path to YAML/JSON file with node overrides')
    args = parser.parse_args()
    template = load_template()
    overrides = parse_overrides(args.overrides)
    mission = merge_config(template, args.objective, args.zone, args.priority, overrides)
    outfile = save_mission(mission)
    logger.info("Mission saved to %s", outfile)


if __name__ == '__main__':
    main()