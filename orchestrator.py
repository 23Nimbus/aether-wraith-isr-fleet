#!/usr/bin/env python3
"""
orchestrator.py
---------------

This module acts as a simple scheduler and router for the Æther Wraith ISR
Fleet.  It loads a YAML schedule (see ``tasks/schedule.yaml``) and, on
invocation, determines which tasks should run at the current time.  The
resulting actions are logged to ``orchestration_log.json`` for auditing and
replay.  After executing scheduled actions the orchestrator optionally runs
the anomaly detector defined in ``agents/aether_ai.py`` to analyse the
latest telemetry.

The scheduler uses the ``croniter`` library if available to interpret cron
expressions.  If ``croniter`` is not installed, all tasks are executed
unconditionally.
"""

from __future__ import annotations

import yaml
from datetime import datetime
import json
import os
from utils.logging_utils import get_logger, setup_logging
import asyncio
from typing import Callable, Dict, List, Awaitable

try:
    # croniter is used to evaluate cron expressions.  It is optional; if not
    # present the orchestrator simply runs all configured tasks.
    from croniter import croniter  # type: ignore
except ImportError:
    croniter = None  # type: ignore


# Configure logging for the orchestrator.  Using the shared logging
# utilities ensures consistent formatting across the system and honours
# environment overrides (e.g. AE_LOG_JSON).
setup_logging()
logger = get_logger(__name__)

# Paths relative to this script.  These are computed lazily to allow the
# orchestrator to be run from any working directory.
HERE = os.path.dirname(__file__)
SCHEDULE_PATH = os.path.join(HERE, 'tasks', 'schedule.yaml')
LOG_PATH = os.path.join(HERE, 'orchestration_log.json')
EVENT_LOG_PATH = os.path.join(HERE, 'telemetry', 'event_log.csv')


def load_schedule() -> List[dict]:
    """Load the task schedule from YAML.

    Returns an array of tasks, each of which contains at minimum the keys
    ``name``, ``cron`` and ``action``.
    """
    with open(SCHEDULE_PATH, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f) or {}
    return config.get('tasks', [])


def should_run(cron_expr: str | None, ref_time: datetime) -> bool:
    """Determine whether a cron expression is due at the reference time.

    This helper uses croniter, if available, to decide whether the task
    described by ``cron_expr`` should be invoked at ``ref_time``.  The
    function returns ``True`` if the cron expression is invalid or if
    croniter is not installed, resulting in the task being executed
    unconditionally.
    """
    if croniter is None or not cron_expr:
        return True
    try:
        itr = croniter(cron_expr, ref_time)
    except Exception:
        # Invalid cron expression – run the task anyway and let the user fix it.
        return True
    # A task is considered due if the current time is within the window
    # [prev_time, next_time).  This is a simplistic interpretation but
    # sufficient for a lightweight orchestrator.  Subtracting a small
    # epsilon accounts for tasks scheduled exactly on ``ref_time``.
    prev_time = itr.get_prev(datetime)
    next_time = itr.get_next(datetime)
    return prev_time <= ref_time < next_time


async def push_telemetry() -> None:
    """Placeholder asynchronous function for pushing telemetry."""
    # Simulate an asynchronous network call with asyncio.sleep.
    await asyncio.sleep(0)
    logger.info("Pushing telemetry to central repository (placeholder)...")


async def replan_isr_sweep() -> None:
    """Placeholder asynchronous function for replanning an ISR sweep."""
    await asyncio.sleep(0)
    logger.info("Replanning ISR sweep (placeholder)...")


# Mapping from action names in the schedule to callables.  Extend this map
# with additional handlers as new tasks are added to ``tasks/schedule.yaml``.
ACTION_MAP: Dict[str, Callable[[], Awaitable[None]]] = {
    'push_telemetry': push_telemetry,
    'replan_isr_sweep': replan_isr_sweep,
}


async def run_actions(tasks: List[dict]) -> List[dict]:
    """Execute scheduled actions concurrently and return a list of event records.

    This asynchronous variant schedules handlers concurrently using
    ``asyncio``.  Each handler in ``ACTION_MAP`` is an ``async`` function.
    
    Parameters
    ----------
    tasks : list of dict
        The loaded schedule entries.

    Returns
    -------
    list of dict
        A list of event records with the keys ``task``, ``action`` and
        ``timestamp``.  This list is empty if no actions were triggered.
    """
    events: List[dict] = []
    now = datetime.utcnow()

    async def wrap_and_record(task_def: dict) -> None:
        action_name = task_def.get('action')
        cron_expr = task_def.get('cron')
        if not action_name:
            return
        handler = ACTION_MAP.get(action_name)
        if handler is None:
            logger.warning("Unknown action '%s' in schedule", action_name)
            return
        if should_run(cron_expr, now):
            await handler()
            events.append({
                'task': task_def.get('name'),
                'action': action_name,
                'timestamp': now.isoformat() + 'Z',
            })
    # Execute all tasks concurrently
    await asyncio.gather(*(wrap_and_record(t) for t in tasks))
    return events


def append_log(events: List[dict]) -> None:
    """Append orchestration events to the persistent log file."""
    if not events:
        return
    log_entries: List[dict] = []
    if os.path.exists(LOG_PATH):
        with open(LOG_PATH, 'r', encoding='utf-8') as f:
            try:
                log_entries = json.load(f)
            except json.JSONDecodeError:
                log_entries = []
    log_entries.extend(events)
    with open(LOG_PATH, 'w', encoding='utf-8') as f:
        json.dump(log_entries, f, indent=2)


def run_anomaly_detection() -> None:
    """Invoke the AI agent over the most recent event log if present."""
    # Only run the detector if the event log exists – it's optional in CI.
    if not os.path.exists(EVENT_LOG_PATH):
        return
    try:
        # Import lazily to avoid mandatory dependency on the AI code.
        from agents import aether_ai  # type: ignore
    except ImportError:
        logger.warning("AI agent not available; skipping anomaly detection")
        return
    logger.info("Running anomaly detection on event log...")
    aether_ai.process_event_log(EVENT_LOG_PATH)


async def main_async() -> None:
    """Entry point for CLI invocation of the orchestrator using asyncio."""
    tasks = load_schedule()
    events = await run_actions(tasks)
    append_log(events)
    if events:
        logger.info("Recorded %d orchestration events.", len(events))
    else:
        logger.info("No tasks were triggered.")
    # After executing scheduled actions we run the anomaly detector to flag any
    # new events in the telemetry log.
    run_anomaly_detection()


if __name__ == '__main__':
    # Run the asynchronous orchestrator via asyncio.  This ensures that the
    # event loop is properly created and closed.
    asyncio.run(main_async())