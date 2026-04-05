from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class BillingResponse(BaseModel):
    id: str
    invoice_number: str
    parcel_id: str
    customer_name: str
    customer_email: Optional[str] = None
    amount: float
    payment_status: str
    generated_at: Optional[datetime] = None
    paid_at: Optional[datetime] = None
    pdf_path: Optional[str] = None

class PaymentUpdate(BaseModel):
    payment_status: str  # "Paid" or "Unpaid"

class BillingGenerate(BaseModel):
    parcel_id: str
    customer_name: str
    customer_email: Optional[str] = None
    amount: float
