from fastapi import APIRouter, HTTPException
from datetime import datetime, timezone
from ..models import Case
from .events import get_event

router = APIRouter(prefix="/v1/cases", tags=["cases"])

# In-memory case storage keyed by case ID
cases_db: dict[str, Case] = {}

@router.post("", response_model=Case)
def create_case(case: Case):
    if not get_event(case.initial_event_id):
        raise HTTPException(status_code=404, detail="initial_event_id not found")
    now = datetime.now(timezone.utc)
    case.created_date = now
    case.updated_date = now
    cases_db[case.id] = case
    return case

@router.get("", response_model=list[Case])
def list_cases():
    return list(cases_db.values())

@router.get("/{case_id}", response_model=Case)
def read_case(case_id: str):
    case = get_case(case_id)
    if not case:
        raise HTTPException(status_code=404, detail="case not found")
    return case

@router.put("/{case_id}", response_model=Case)
def update_case(case_id: str, case_update: Case):
    if not get_event(case_update.initial_event_id):
        raise HTTPException(status_code=404, detail="initial_event_id not found")
    case = get_case(case_id)
    if not case:
        raise HTTPException(status_code=404, detail="case not found")
    case_update.id = case_id
    case_update.created_date = case.created_date
    case_update.updated_date = datetime.now(timezone.utc)
    cases_db[case_id] = case_update
    return case_update

@router.delete("/{case_id}")
def delete_case(case_id: str):
    case = cases_db.pop(case_id, None)
    if not case:
        raise HTTPException(status_code=404, detail="case not found")
    return {"detail": "deleted"}

def get_case(case_id: str) -> Case | None:
    return cases_db.get(case_id)
