from fastapi import APIRouter, HTTPException
from .cases import get_case
from ..models import Case
# Use TinyDB-backed database for persistence
from .. import database

router = APIRouter(prefix="/entities", tags=["entities"])

@router.get("/Case", response_model=list[Case])
def list_case_entities():
    return database.list_cases()

@router.get("/Case/{case_id}", response_model=Case)
def read_case_entity(case_id: str):
    case = get_case(case_id)
    if not case:
        raise HTTPException(status_code=404, detail="case not found")
    return case
