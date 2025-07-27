from pydantic import BaseModel, Field
from typing import List, Optional
from uuid import uuid4

class Location(BaseModel):
    lat: float
    lon: float

class Event(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    source_type: str
    source_id: str
    timestamp: str
    location: Location
    summary: str
    media_url: Optional[str] = None

class Case(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    title: str
    location: Location
    initial_event_id: str

class TaskRequest(BaseModel):
    case_id: str
    sensor_types: List[str]
    urgency: str
    preferred_assets: List[str] = []

class Task(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    case_id: str
    sensor_types: List[str]
    urgency: str
    preferred_assets: List[str] = []
