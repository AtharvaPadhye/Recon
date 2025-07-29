"""Very simple NLP utilities used to derive structured information."""

from typing import Optional

from .models import Event, Case, Location


KEYWORDS = ["troop", "convoy", "movement", "asset"]


def extract_case_from_event(event: Event) -> Optional[Case]:
    """Create a Case from an Event if its summary contains known keywords."""
    text = event.summary.lower()
    if any(word in text for word in KEYWORDS):
        return Case(
            title=f"Case derived from {event.source_id}",
            location=event.location,
            summary=event.summary,
            initial_event_id=event.id,
        )
    return None
