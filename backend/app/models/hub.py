from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class HubCreate(BaseModel):
    hub_name: str
    hub_code: str
    city: str
    address: str
    contact_person: str
    phone: str
    capacity: int

class HubUpdate(BaseModel):
    hub_name: Optional[str] = None
    hub_code: Optional[str] = None
    city: Optional[str] = None
    address: Optional[str] = None
    contact_person: Optional[str] = None
    phone: Optional[str] = None
    capacity: Optional[int] = None

class HubResponse(BaseModel):
    id: str
    hub_name: str
    hub_code: str
    city: str
    address: str
    contact_person: str
    phone: str
    capacity: int
    created_at: Optional[datetime] = None
