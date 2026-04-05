from pydantic import BaseModel, Field
from typing import Optional, Literal, List
from datetime import datetime

class StatusHistory(BaseModel):
    status: str
    timestamp: datetime
    updated_by: str

class ProofOfDelivery(BaseModel):
    image_url: str
    uploaded_at: datetime

class ParcelCreate(BaseModel):
    sender_name: str
    sender_phone: str
    receiver_name: str
    receiver_phone: str
    receiver_address: str
    weight: float
    dimensions: Optional[str] = None
    parcel_type: str
    description: Optional[str] = None
    price: float
    payment_status: Literal["Paid", "Unpaid"] = "Unpaid"
    assigned_agent_id: Optional[str] = None
    route_id: Optional[str] = None
    hub_id: Optional[str] = None

class ParcelUpdate(BaseModel):
    sender_name: Optional[str] = None
    sender_phone: Optional[str] = None
    receiver_name: Optional[str] = None
    receiver_phone: Optional[str] = None
    receiver_address: Optional[str] = None
    weight: Optional[float] = None
    dimensions: Optional[str] = None
    parcel_type: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    payment_status: Optional[Literal["Paid", "Unpaid"]] = None
    assigned_agent_id: Optional[str] = None
    route_id: Optional[str] = None
    hub_id: Optional[str] = None

class ParcelStatusUpdate(BaseModel):
    status: Literal["Created", "Picked Up", "In Transit", "At Hub", "Out for Delivery", "Delivered"]

class ParcelAssign(BaseModel):
    agent_id: str

class ParcelResponse(BaseModel):
    id: str
    tracking_id: str
    sender_name: str
    sender_phone: str
    receiver_name: str
    receiver_phone: str
    receiver_address: str
    weight: float
    dimensions: Optional[str] = None
    parcel_type: str
    description: Optional[str] = None
    price: float
    payment_status: str
    status: str
    assigned_agent_id: Optional[str] = None
    route_id: Optional[str] = None
    hub_id: Optional[str] = None
    proof_of_delivery: Optional[dict] = None
    status_history: Optional[List[dict]] = []
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
