from pydantic import BaseModel
from typing import Optional, Literal
from datetime import datetime

class NotificationCreate(BaseModel):
    user_id: str
    message: str
    type: Literal["parcel", "ticket", "billing", "dispatch", "system"] = "system"

class NotificationResponse(BaseModel):
    id: str
    user_id: str
    message: str
    type: str
    is_read: bool = False
    created_at: Optional[datetime] = None
