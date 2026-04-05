from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class RouteCreate(BaseModel):
    route_name: str
    origin_hub_id: str
    destination_hub_id: str
    waypoint_hubs: Optional[List[str]] = []
    distance_km: float
    estimated_days: int

class RouteUpdate(BaseModel):
    route_name: Optional[str] = None
    origin_hub_id: Optional[str] = None
    destination_hub_id: Optional[str] = None
    waypoint_hubs: Optional[List[str]] = None
    distance_km: Optional[float] = None
    estimated_days: Optional[int] = None

class RouteResponse(BaseModel):
    id: str
    route_name: str
    origin_hub_id: str
    destination_hub_id: str
    waypoint_hubs: Optional[List[str]] = []
    distance_km: float
    estimated_days: int
    created_at: Optional[datetime] = None
