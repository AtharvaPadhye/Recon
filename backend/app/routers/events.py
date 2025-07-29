from fastapi import APIRouter, HTTPException
from ..models import Event, Case

# Use TinyDB-backed database for persistence
from .. import database
from .. import nlp

router = APIRouter(prefix="/v1/events", tags=["events"])


@router.post("", response_model=Event)
def create_event(event: Event):
    return database.add_event(event)


@router.get("", response_model=list[Event])
def list_events():
    return database.list_events()


@router.get("/{event_id}", response_model=Event)
def read_event(event_id: str):
    event = get_event(event_id)
    if not event:
        raise HTTPException(status_code=404, detail="event not found")
    return event


@router.post("/{event_id}/process", response_model=Case | dict)
def process_event(event_id: str):
    event = get_event(event_id)
    if not event:
        raise HTTPException(status_code=404, detail="event not found")
    case = nlp.extract_case_from_event(event)
    if not case:
        return {"detail": "no case generated"}
    return database.add_case(case)


@router.put("/{event_id}", response_model=Event)
def update_event(event_id: str, event_update: Event):
    event = get_event(event_id)
    if not event:
        raise HTTPException(status_code=404, detail="event not found")
    event_update.id = event_id
    updated = database.update_event(event_id, event_update)
    return updated


@router.delete("/{event_id}")
def delete_event(event_id: str):
    event = get_event(event_id)
    if not event:
        raise HTTPException(status_code=404, detail="event not found")
    database.delete_event(event_id)
    return {"detail": "deleted"}


def get_event(event_id: str) -> Event:
    return database.get_event(event_id)
