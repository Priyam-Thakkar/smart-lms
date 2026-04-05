from fastapi import APIRouter, HTTPException, Depends, UploadFile, File
from app.dependencies import require_agent
from app.services import parcel_service, notification_service
from app.config import settings
import os, aiofiles
from datetime import datetime

router = APIRouter()

@router.get("/parcels")
async def get_agent_parcels(agent=Depends(require_agent)):
    return await parcel_service.get_all_parcels({"assigned_agent_id": agent["id"]})

@router.get("/parcels/{parcel_id}")
async def get_agent_parcel(parcel_id: str, agent=Depends(require_agent)):
    parcel = await parcel_service.get_parcel_by_id(parcel_id)
    if not parcel or parcel.get("assigned_agent_id") != agent["id"]:
        raise HTTPException(404, "Parcel not found or not assigned to you")
    return parcel

@router.put("/parcels/{parcel_id}/status")
async def update_status(parcel_id: str, data: dict, agent=Depends(require_agent)):
    parcel = await parcel_service.get_parcel_by_id(parcel_id)
    if not parcel or parcel.get("assigned_agent_id") != agent["id"]:
        raise HTTPException(403, "Not authorized to update this parcel")
    new_status = data.get("status")
    updated = await parcel_service.update_parcel_status(parcel_id, new_status, agent["name"])
    # Notify admin
    await notification_service.create_notification(
        "admin", f"Agent {agent['name']} updated parcel {parcel['tracking_id']} to {new_status}", "parcel"
    )
    return updated

@router.post("/parcels/{parcel_id}/proof")
async def upload_proof(parcel_id: str, file: UploadFile = File(...), agent=Depends(require_agent)):
    parcel = await parcel_service.get_parcel_by_id(parcel_id)
    if not parcel:
        raise HTTPException(404, "Parcel not found")
    
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    filename = f"proof_{parcel_id}_{int(datetime.utcnow().timestamp())}{os.path.splitext(file.filename)[1]}"
    filepath = os.path.join(settings.UPLOAD_DIR, filename)
    
    async with aiofiles.open(filepath, "wb") as out_file:
        content = await file.read()
        await out_file.write(content)
    
    image_url = f"/uploads/{filename}"
    updated = await parcel_service.save_proof_of_delivery(parcel_id, image_url)
    await notification_service.create_notification(
        "admin", f"Proof of delivery uploaded for parcel {parcel['tracking_id']}", "parcel"
    )
    return updated

@router.get("/tracking/{parcel_id}")
async def get_tracking(parcel_id: str, agent=Depends(require_agent)):
    parcel = await parcel_service.get_parcel_by_id(parcel_id)
    if not parcel:
        raise HTTPException(404, "Parcel not found")
    return {"tracking_id": parcel["tracking_id"], "status": parcel["status"], "history": parcel.get("status_history", [])}

@router.get("/dashboard")
async def agent_dashboard(agent=Depends(require_agent)):
    from app.database import parcels_collection
    total = await parcels_collection.count_documents({"assigned_agent_id": agent["id"]})
    delivered = await parcels_collection.count_documents({"assigned_agent_id": agent["id"], "status": "Delivered"})
    pending = total - delivered
    return {"total_assigned": total, "delivered": delivered, "pending": pending}
