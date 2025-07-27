from fastapi import APIRouter
from ..models import Event

router = APIRouter(prefix="/v1/events", tags=["events"])

events_db = []

@router.post("", response_model=Event)
def create_event(event: Event):
    events_db.append(event)
    return event

def get_event(event_id: str) -> Event:
    for e in events_db:
        if e.id == event_id:
            return e
    return None
