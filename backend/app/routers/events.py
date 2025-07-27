from fastapi import APIRouter, HTTPException
from ..models import Event

router = APIRouter(prefix="/v1/events", tags=["events"])

events_db = []

@router.post("", response_model=Event)
def create_event(event: Event):
    events_db.append(event)
    return event

@router.get("", response_model=list[Event])
def list_events():
    return events_db

@router.get("/{event_id}", response_model=Event)
def read_event(event_id: str):
    event = get_event(event_id)
    if not event:
        raise HTTPException(status_code=404, detail="event not found")
    return event

@router.put("/{event_id}", response_model=Event)
def update_event(event_id: str, event_update: Event):
    event = get_event(event_id)
    if not event:
        raise HTTPException(status_code=404, detail="event not found")
    event_update.id = event_id
    idx = events_db.index(event)
    events_db[idx] = event_update
    return event_update

@router.delete("/{event_id}")
def delete_event(event_id: str):
    event = get_event(event_id)
    if not event:
        raise HTTPException(status_code=404, detail="event not found")
    events_db.remove(event)
    return {"detail": "deleted"}

def get_event(event_id: str) -> Event:
    for e in events_db:
        if e.id == event_id:
            return e
    return None
