from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class DispatchCreate(BaseModel):
    parcel_id: str
    agent_id: str
    hub_id: str
    route_id: str
    dispatch_date: datetime
    expected_delivery: datetime
    notes: Optional[str] = None

class DispatchUpdate(BaseModel):
    agent_id: Optional[str] = None
    hub_id: Optional[str] = None
    route_id: Optional[str] = None
    dispatch_date: Optional[datetime] = None
    expected_delivery: Optional[datetime] = None
    status: Optional[str] = None
    notes: Optional[str] = None

class DispatchResponse(BaseModel):
    id: str
    parcel_id: str
    agent_id: str
    hub_id: str
    route_id: str
    dispatch_date: Optional[datetime] = None
    expected_delivery: Optional[datetime] = None
    status: Optional[str] = None
    notes: Optional[str] = None
    created_at: Optional[datetime] = None
