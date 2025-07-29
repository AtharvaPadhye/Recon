from typing import List, Optional
from tinydb import TinyDB, Query
from .models import Event, Case, Task, Asset

db = TinyDB("db.json")
_events = db.table("events")
_cases = db.table("cases")
_tasks = db.table("tasks")
_assets = db.table("assets")

_event_q = Query()
_case_q = Query()
_task_q = Query()
_asset_q = Query()

# Utility helpers


def clear_db() -> None:
    """Remove all records from every table."""
    _events.truncate()
    _cases.truncate()
    _tasks.truncate()
    _assets.truncate()


# Event operations


def add_event(event: Event) -> Event:
    _events.insert(event.model_dump(mode="json"))
    return event


def list_events() -> List[Event]:
    return [Event(**e) for e in _events.all()]


def get_event(event_id: str) -> Optional[Event]:
    data = _events.get(_event_q.id == event_id)
    return Event(**data) if data else None


def update_event(event_id: str, event: Event) -> Optional[Event]:
    if not _events.contains(_event_q.id == event_id):
        return None
    _events.update(event.model_dump(mode="json"), _event_q.id == event_id)
    return event


def delete_event(event_id: str) -> bool:
    removed = _events.remove(_event_q.id == event_id)
    return bool(removed)


# Case operations


def add_case(case: Case) -> Case:
    _cases.insert(case.model_dump(mode="json"))
    return case


def list_cases() -> List[Case]:
    return [Case(**c) for c in _cases.all()]


def get_case(case_id: str) -> Optional[Case]:
    data = _cases.get(_case_q.id == case_id)
    return Case(**data) if data else None


def update_case(case_id: str, case: Case) -> Optional[Case]:
    if not _cases.contains(_case_q.id == case_id):
        return None
    _cases.update(case.model_dump(mode="json"), _case_q.id == case_id)
    return case


def delete_case(case_id: str) -> bool:
    removed = _cases.remove(_case_q.id == case_id)
    return bool(removed)


# Task operations


def add_task(task: Task) -> Task:
    _tasks.insert(task.model_dump(mode="json"))
    return task


def list_tasks() -> List[Task]:
    return [Task(**t) for t in _tasks.all()]


def get_task(task_id: str) -> Optional[Task]:
    data = _tasks.get(_task_q.id == task_id)
    return Task(**data) if data else None


def update_task(task_id: str, task: Task) -> Optional[Task]:
    if not _tasks.contains(_task_q.id == task_id):
        return None
    _tasks.update(task.model_dump(mode="json"), _task_q.id == task_id)
    return task


def delete_task(task_id: str) -> bool:
    removed = _tasks.remove(_task_q.id == task_id)
    return bool(removed)


# Asset operations


def add_asset(asset: Asset) -> Asset:
    _assets.insert(asset.model_dump(mode="json"))
    return asset


def list_assets() -> List[Asset]:
    return [Asset(**a) for a in _assets.all()]


def get_asset(asset_id: str) -> Optional[Asset]:
    data = _assets.get(_asset_q.id == asset_id)
    return Asset(**data) if data else None


def update_asset(asset_id: str, asset: Asset) -> Optional[Asset]:
    if not _assets.contains(_asset_q.id == asset_id):
        return None
    _assets.update(asset.model_dump(mode="json"), _asset_q.id == asset_id)
    return asset


def delete_asset(asset_id: str) -> bool:
    removed = _assets.remove(_asset_q.id == asset_id)
    return bool(removed)
