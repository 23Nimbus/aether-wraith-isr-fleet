#!/usr/bin/env python3
"""
add_task.py
-----------

CLI utility for adding a new scheduled task to ``tasks/schedule.yaml`` at
runtime.  This script enables dynamic modification of the scheduler
configuration without manually editing YAML files.  It accepts the task
name, cron expression and action name and appends a new entry to the
existing list of tasks.

Example:

    python tasks/add_task.py --name nightly_upload --cron "0 2 * * *" --action push_telemetry
"""

from __future__ import annotations

import argparse
import yaml  # type: ignore
import os
from utils.logging_utils import setup_logging, get_logger

setup_logging()
logger = get_logger(__name__)

HERE = os.path.dirname(os.path.dirname(__file__))
SCHEDULE_PATH = os.path.join(HERE, 'tasks', 'schedule.yaml')


def load_schedule() -> dict:
    if not os.path.exists(SCHEDULE_PATH):
        return {'tasks': []}
    with open(SCHEDULE_PATH, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f) or {'tasks': []}


def save_schedule(data: dict) -> None:
    os.makedirs(os.path.dirname(SCHEDULE_PATH), exist_ok=True)
    with open(SCHEDULE_PATH, 'w', encoding='utf-8') as f:
        yaml.safe_dump(data, f, sort_keys=False)


def main() -> None:
    parser = argparse.ArgumentParser(description='Add a scheduled task to the orchestrator.')
    parser.add_argument('--name', required=True, help='Unique name for the task')
    parser.add_argument('--cron', required=True, help='Cron expression (e.g. "0 0 * * *")')
    parser.add_argument('--action', required=True, help='Action name defined in the orchestrator')
    args = parser.parse_args()

    sched = load_schedule()
    # Prevent duplicate task names
    for t in sched.get('tasks', []):
        if t.get('name') == args.name:
            logger.error('A task named %s already exists.', args.name)
            return
    sched.setdefault('tasks', []).append({
        'name': args.name,
        'cron': args.cron,
        'action': args.action,
    })
    save_schedule(sched)
    logger.info('Added task %s with cron "%s" and action %s', args.name, args.cron, args.action)


if __name__ == '__main__':
    main()