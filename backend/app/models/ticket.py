from pydantic import BaseModel
from typing import Optional, Literal
from datetime import datetime

class TicketCreate(BaseModel):
    parcel_id: str
    issue_type: str
    description: str
    priority: Literal["Low", "Medium", "High"] = "Medium"

class TicketUpdate(BaseModel):
    status: Optional[Literal["Open", "In Progress", "Resolved"]] = None
    admin_notes: Optional[str] = None
    priority: Optional[Literal["Low", "Medium", "High"]] = None

class TicketResponse(BaseModel):
    id: str
    ticket_id: str
    customer_id: str
    parcel_id: str
    issue_type: str
    description: str
    priority: str
    status: str
    admin_notes: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
