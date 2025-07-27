from fastapi import APIRouter, HTTPException
from ..models import Case
from .events import get_event

router = APIRouter(prefix="/v1/cases", tags=["cases"])

cases_db = []

@router.post("", response_model=Case)
def create_case(case: Case):
    if not get_event(case.initial_event_id):
        raise HTTPException(status_code=404, detail="initial_event_id not found")
    cases_db.append(case)
    return case

@router.get("", response_model=list[Case])
def list_cases():
    return cases_db

def get_case(case_id: str) -> Case:
    for c in cases_db:
        if c.id == case_id:
            return c
    return None
