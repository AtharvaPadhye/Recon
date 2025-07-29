from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from uuid import uuid4
from enum import Enum


class Location(BaseModel):
    lat: float
    lon: float


class Event(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    source_type: str
    source_id: str
    timestamp: datetime
    location: Location
    summary: str
    media_url: Optional[str] = None


class Case(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    title: str
    status: str = "New"
    location: Location
    summary: Optional[str] = None
    initial_event_id: str
    created_date: Optional[datetime] = None
    updated_date: Optional[datetime] = None
    created_by_id: Optional[str] = None
    created_by: Optional[str] = None
    is_sample: bool = False


class Urgency(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"


class SensorType(str, Enum):
    optical = "optical"
    infrared = "infrared"
    radar = "radar"


class AssetStatus(str, Enum):
    available = "available"
    assigned = "assigned"
    deployed = "deployed"


class Asset(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    name: str
    sensor_type: SensorType
    location: Optional[Location] = None
    status: AssetStatus = AssetStatus.available


class TaskRequest(BaseModel):
    case_id: str
    sensor_types: List[SensorType]
    urgency: Urgency
    preferred_assets: List[str] = Field(default_factory=list)


class Task(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    case_id: str
    sensor_types: List[SensorType]
    urgency: Urgency
    preferred_assets: List[str] = Field(default_factory=list)
    assigned_asset_id: Optional[str] = None
