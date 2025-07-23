#!/usr/bin/env python3
"""
orchestrator.py
---------------

This module acts as a simple scheduler and router for the Æther Wraith ISR
Fleet.  It loads a YAML schedule (see `tasks/schedule.yaml`) and, on
invocation, checks which tasks should run at the current time.  For the
purposes of this skeleton it executes all configured actions immediately
when run.

The orchestrator writes an `orchestration_log.json` file to record when
actions were invoked.  This log can be used for auditing and replay.
"""
import yaml
from datetime import datetime
import json
import os
from typing import Callable, Dict

try:
    from croniter import croniter  # type: ignore
except ImportError:
    croniter = None  # type: ignore

SCHEDULE_PATH = os.path.join(os.path.dirname(__file__), 'tasks', 'schedule.yaml')
LOG_PATH = os.path.join(os.path.dirname(__file__), 'orchestration_log.json')


def load_schedule() -> list[dict]:
    with open(SCHEDULE_PATH, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    return config.get('tasks', [])

def push_telemetry():
    print("[Orchestrator] Pushing telemetry to central repository (placeholder)...")

def replan_isr_sweep():
    print("[Orchestrator] Replanning ISR sweep (placeholder)...")

ACTION_MAP: Dict[str, Callable[[], None]] = {
    'push_telemetry': push_telemetry,
    'replan_isr_sweep': replan_isr_sweep,
}

def run_actions(tasks: list[dict]) -> list[dict]:
    events = []
    now = datetime.utcnow()
    for task in tasks:
        action_name = task.get('action')
        cron_expr = task.get('cron')
        if not action_name:
            continue
        # In this skeleton we trigger all tasks unconditionally.  To support real
        # scheduling you would compare `now` against the next run time computed
        # by croniter(cron_expr).get_next(datetime).
        handler = ACTION_MAP.get(action_name)
        if handler:
            handler()
            events.append({
                'task': task.get('name'),
                'action': action_name,
                'timestamp': now.isoformat() + 'Z',
            })
    return events

def append_log(events: list[dict]) -> None:
    if not events:
        return
    log_entries = []
    if os.path.exists(LOG_PATH):
        with open(LOG_PATH, 'r', encoding='utf-8') as f:
            try:
                log_entries = json.load(f)
            except json.JSONDecodeError:
                log_entries = []
    log_entries.extend(events)
    with open(LOG_PATH, 'w', encoding='utf-8') as f:
        json.dump(log_entries, f, indent=2)

def main() -> None:
    tasks = load_schedule()
    events = run_actions(tasks)
    append_log(events)
    if events:
        print(f"Recorded {len(events)} orchestration events.")
    else:
        print("No tasks were triggered.")

if __name__ == '__main__':
    main()