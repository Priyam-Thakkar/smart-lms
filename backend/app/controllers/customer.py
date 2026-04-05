from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import StreamingResponse
from app.dependencies import require_customer
from app.services import parcel_service, billing_service, pdf_service, notification_service
from app.database import tickets_collection
from bson import ObjectId
from datetime import datetime
import random, string, io

router = APIRouter()

def serialize_ticket(t):
    t["id"] = str(t["_id"]); del t["_id"]; return t

@router.get("/track/{tracking_id}")
async def track_parcel(tracking_id: str, customer=Depends(require_customer)):
    parcel = await parcel_service.get_parcel_by_tracking_id(tracking_id)
    if not parcel:
        raise HTTPException(404, "Parcel not found with this tracking ID")
    return parcel

@router.post("/tickets", status_code=201)
async def create_ticket(data: dict, customer=Depends(require_customer)):
    ticket_id = "TKT-" + ''.join(random.choices(string.digits, k=6))
    doc = {
        "ticket_id": ticket_id,
        "customer_id": customer["id"],
        "parcel_id": data.get("parcel_id"),
        "issue_type": data.get("issue_type"),
        "description": data.get("description"),
        "priority": data.get("priority", "Medium"),
        "status": "Open",
        "admin_notes": None,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
    result = await tickets_collection.insert_one(doc)
    # Notify admin
    await notification_service.create_notification(
        "admin", f"New support ticket {ticket_id} from {customer['name']}", "ticket"
    )
    t = await tickets_collection.find_one({"_id": result.inserted_id})
    return serialize_ticket(t)

@router.get("/tickets")
async def get_tickets(customer=Depends(require_customer)):
    tickets = []
    async for t in tickets_collection.find({"customer_id": customer["id"]}).sort("created_at", -1):
        tickets.append(serialize_ticket(t))
    return tickets

@router.get("/billing/{tracking_id}")
async def get_billing_by_tracking(tracking_id: str, customer=Depends(require_customer)):
    parcel = await parcel_service.get_parcel_by_tracking_id(tracking_id)
    if not parcel:
        raise HTTPException(404, "Parcel not found")
    billing = await billing_service.get_billing_by_parcel_id(parcel["id"])
    if not billing:
        raise HTTPException(404, "Billing record not found")
    return billing

@router.get("/billing/{billing_id}/download")
async def download_invoice(billing_id: str, customer=Depends(require_customer)):
    billing = await billing_service.get_billing_by_id(billing_id)
    if not billing:
        raise HTTPException(404, "Billing not found")
    parcel = await parcel_service.get_parcel_by_id(billing["parcel_id"])
    if not parcel:
        raise HTTPException(404, "Parcel not found")
    pdf_bytes = pdf_service.generate_invoice_pdf(billing, parcel)
    return StreamingResponse(
        io.BytesIO(pdf_bytes),
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename={billing['invoice_number']}.pdf"}
    )
