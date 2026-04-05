from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Literal
from datetime import datetime

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: Literal["admin", "agent", "customer"] = "customer"
    phone: Optional[str] = None

class UserUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None

class PasswordChange(BaseModel):
    current_password: str
    new_password: str
    confirm_password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: str
    name: str
    email: str
    role: str
    phone: Optional[str] = None
    profile_pic: Optional[str] = None
    created_at: Optional[datetime] = None
    settings: Optional[dict] = None

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse
