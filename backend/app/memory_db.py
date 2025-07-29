from typing import List, Optional
from .models import Event, Case, Task, Asset

# In-memory storage using dictionaries
_events: dict[str, Event] = {}
_cases: dict[str, Case] = {}
_tasks: dict[str, Task] = {}
_assets: dict[str, Asset] = {}

# Utility helpers


def clear_db() -> None:
    """Remove all records from every table."""
    _events.clear()
    _cases.clear()
    _tasks.clear()
    _assets.clear()


# Event operations


def add_event(event: Event) -> Event:
    _events[event.id] = event
    return event


def list_events() -> List[Event]:
    return list(_events.values())


def get_event(event_id: str) -> Optional[Event]:
    return _events.get(event_id)


def update_event(event_id: str, event: Event) -> Optional[Event]:
    if event_id not in _events:
        return None
    _events[event_id] = event
    return event


def delete_event(event_id: str) -> bool:
    return _events.pop(event_id, None) is not None


# Case operations


def add_case(case: Case) -> Case:
    _cases[case.id] = case
    return case


def list_cases() -> List[Case]:
    return list(_cases.values())


def get_case(case_id: str) -> Optional[Case]:
    return _cases.get(case_id)


def update_case(case_id: str, case: Case) -> Optional[Case]:
    if case_id not in _cases:
        return None
    _cases[case_id] = case
    return case


def delete_case(case_id: str) -> bool:
    return _cases.pop(case_id, None) is not None


# Task operations


def add_task(task: Task) -> Task:
    _tasks[task.id] = task
    return task


def list_tasks() -> List[Task]:
    return list(_tasks.values())


def get_task(task_id: str) -> Optional[Task]:
    return _tasks.get(task_id)


def update_task(task_id: str, task: Task) -> Optional[Task]:
    if task_id not in _tasks:
        return None
    _tasks[task_id] = task
    return task


def delete_task(task_id: str) -> bool:
    return _tasks.pop(task_id, None) is not None


# Asset operations


def add_asset(asset: Asset) -> Asset:
    _assets[asset.id] = asset
    return asset


def list_assets() -> List[Asset]:
    return list(_assets.values())


def get_asset(asset_id: str) -> Optional[Asset]:
    return _assets.get(asset_id)


def update_asset(asset_id: str, asset: Asset) -> Optional[Asset]:
    if asset_id not in _assets:
        return None
    _assets[asset_id] = asset
    return asset


def delete_asset(asset_id: str) -> bool:
    return _assets.pop(asset_id, None) is not None
