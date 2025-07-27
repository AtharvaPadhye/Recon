from fastapi import APIRouter, HTTPException
from ..models import Event

router = APIRouter(prefix="/v1/events", tags=["events"])

# Use a simple in-memory dict for storage keyed by event ID
events_db: dict[str, Event] = {}

@router.post("", response_model=Event)
def create_event(event: Event):
    events_db[event.id] = event
    return event

@router.get("", response_model=list[Event])
def list_events():
    return list(events_db.values())

@router.get("/{event_id}", response_model=Event)
def read_event(event_id: str):
    event = get_event(event_id)
    if not event:
        raise HTTPException(status_code=404, detail="event not found")
    return event

@router.put("/{event_id}", response_model=Event)
def update_event(event_id: str, event_update: Event):
    if event_id not in events_db:
        raise HTTPException(status_code=404, detail="event not found")
    event_update.id = event_id
    events_db[event_id] = event_update
    return event_update

@router.delete("/{event_id}")
def delete_event(event_id: str):
    event = events_db.pop(event_id, None)
    if not event:
        raise HTTPException(status_code=404, detail="event not found")
    return {"detail": "deleted"}

def get_event(event_id: str) -> Event | None:
    return events_db.get(event_id)
