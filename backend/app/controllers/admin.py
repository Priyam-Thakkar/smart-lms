from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.responses import StreamingResponse
from bson import ObjectId
from datetime import datetime
import io

from app.dependencies import require_admin
from app.models.parcel import ParcelCreate, ParcelUpdate, ParcelStatusUpdate, ParcelAssign
from app.models.hub import HubCreate, HubUpdate
from app.models.route import RouteCreate, RouteUpdate
from app.models.dispatch import DispatchCreate, DispatchUpdate
from app.models.billing import PaymentUpdate
from app.services import parcel_service, hub_service, billing_service, notification_service, pdf_service
from app.database import (
    parcels_collection, hubs_collection, routes_collection,
    dispatches_collection, billing_collection, tickets_collection, users_collection
)

router = APIRouter()

# ─── USERS / AGENTS ───
@router.get("/users")
async def get_users_by_role(role: str = None, admin=Depends(require_admin)):
    query = {}
    if role:
        query["role"] = role
    users = []
    async for u in users_collection.find(query):
        u["id"] = str(u["_id"])
        del u["_id"]
        u.pop("password", None)
        users.append(u)
    return users

# ─── PARCELS ───
@router.get("/parcels")
async def get_parcels(admin=Depends(require_admin)):
    return await parcel_service.get_all_parcels()

@router.post("/parcels", status_code=201)
async def create_parcel(data: ParcelCreate, admin=Depends(require_admin)):
    parcel_data = data.dict()
    parcel = await parcel_service.create_parcel(parcel_data, admin["name"])
    # Auto-create billing
    billing = await billing_service.create_billing(
        parcel["id"], parcel["sender_name"], "", parcel["price"]
    )
    # Notify if agent assigned
    if parcel.get("assigned_agent_id"):
        await notification_service.create_notification(
            parcel["assigned_agent_id"], f"New parcel assigned: {parcel['tracking_id']}", "dispatch"
        )
    return {"parcel": parcel, "billing": billing}

@router.get("/parcels/{parcel_id}")
async def get_parcel(parcel_id: str, admin=Depends(require_admin)):
    parcel = await parcel_service.get_parcel_by_id(parcel_id)
    if not parcel:
        raise HTTPException(404, "Parcel not found")
    return parcel

@router.put("/parcels/{parcel_id}")
async def update_parcel(parcel_id: str, data: ParcelUpdate, admin=Depends(require_admin)):
    update_data = {k: v for k, v in data.dict().items() if v is not None}
    return await parcel_service.update_parcel(parcel_id, update_data)

@router.delete("/parcels/{parcel_id}")
async def delete_parcel(parcel_id: str, admin=Depends(require_admin)):
    deleted = await parcel_service.delete_parcel(parcel_id)
    if not deleted:
        raise HTTPException(404, "Parcel not found")
    return {"message": "Parcel deleted"}

@router.put("/parcels/{parcel_id}/status")
async def update_parcel_status(parcel_id: str, data: ParcelStatusUpdate, admin=Depends(require_admin)):
    parcel = await parcel_service.update_parcel_status(parcel_id, data.status, admin["name"])
    # Notify customer - find by parcel
    return parcel

@router.put("/parcels/{parcel_id}/assign")
async def assign_agent(parcel_id: str, data: ParcelAssign, admin=Depends(require_admin)):
    parcel = await parcel_service.assign_agent(parcel_id, data.agent_id)
    await notification_service.create_notification(
        data.agent_id, f"Parcel {parcel['tracking_id']} assigned to you", "dispatch"
    )
    return parcel

@router.get("/parcels/{parcel_id}/proof")
async def get_proof(parcel_id: str, admin=Depends(require_admin)):
    parcel = await parcel_service.get_parcel_by_id(parcel_id)
    if not parcel:
        raise HTTPException(404, "Parcel not found")
    return {"proof": parcel.get("proof_of_delivery")}

# ─── HUBS ───
@router.get("/hubs")
async def get_hubs(admin=Depends(require_admin)):
    return await hub_service.get_all_hubs()

@router.post("/hubs", status_code=201)
async def create_hub(data: HubCreate, admin=Depends(require_admin)):
    return await hub_service.create_hub(data.dict())

@router.get("/hubs/{hub_id}")
async def get_hub(hub_id: str, admin=Depends(require_admin)):
    hub = await hub_service.get_hub_by_id(hub_id)
    if not hub:
        raise HTTPException(404, "Hub not found")
    return hub

@router.put("/hubs/{hub_id}")
async def update_hub(hub_id: str, data: HubUpdate, admin=Depends(require_admin)):
    update_data = {k: v for k, v in data.dict().items() if v is not None}
    return await hub_service.update_hub(hub_id, update_data)

@router.delete("/hubs/{hub_id}")
async def delete_hub(hub_id: str, admin=Depends(require_admin)):
    deleted = await hub_service.delete_hub(hub_id)
    if not deleted:
        raise HTTPException(404, "Hub not found")
    return {"message": "Hub deleted"}

# ─── ROUTES ───
def serialize_route(r):
    r["id"] = str(r["_id"]); del r["_id"]; return r

@router.get("/routes")
async def get_routes(admin=Depends(require_admin)):
    routes = []
    async for r in routes_collection.find():
        routes.append(serialize_route(r))
    return routes

@router.post("/routes", status_code=201)
async def create_route(data: RouteCreate, admin=Depends(require_admin)):
    doc = data.dict()
    doc["created_at"] = datetime.utcnow()
    result = await routes_collection.insert_one(doc)
    route = await routes_collection.find_one({"_id": result.inserted_id})
    return serialize_route(route)

@router.put("/routes/{route_id}")
async def update_route(route_id: str, data: RouteUpdate, admin=Depends(require_admin)):
    update_data = {k: v for k, v in data.dict().items() if v is not None}
    await routes_collection.update_one({"_id": ObjectId(route_id)}, {"$set": update_data})
    route = await routes_collection.find_one({"_id": ObjectId(route_id)})
    return serialize_route(route) if route else HTTPException(404, "Route not found")

@router.delete("/routes/{route_id}")
async def delete_route(route_id: str, admin=Depends(require_admin)):
    result = await routes_collection.delete_one({"_id": ObjectId(route_id)})
    if result.deleted_count == 0:
        raise HTTPException(404, "Route not found")
    return {"message": "Route deleted"}

# ─── DISPATCH ───
def serialize_dispatch(d):
    d["id"] = str(d["_id"]); del d["_id"]; return d

@router.get("/dispatch")
async def get_dispatches(admin=Depends(require_admin)):
    dispatches = []
    async for d in dispatches_collection.find():
        dispatches.append(serialize_dispatch(d))
    return dispatches

@router.post("/dispatch", status_code=201)
async def create_dispatch(data: DispatchCreate, admin=Depends(require_admin)):
    try:
        parcel = await parcels_collection.find_one({"_id": ObjectId(data.parcel_id)})
        if not parcel:
            raise HTTPException(status_code=404, detail="Parcel not found")
            
        agent = await users_collection.find_one({"_id": ObjectId(data.agent_id), "role": "agent"})
        if not agent:
            raise HTTPException(status_code=404, detail="Agent not found")
            
        hub = await hubs_collection.find_one({"_id": ObjectId(data.hub_id)})
        if not hub:
            raise HTTPException(status_code=404, detail="Hub not found")
            
        route = await routes_collection.find_one({"_id": ObjectId(data.route_id)})
        if not route:
            raise HTTPException(status_code=404, detail="Route not found")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid ID format or error: {str(e)}")

    doc = data.dict()
    doc["status"] = "Dispatched"
    doc["created_at"] = datetime.utcnow()
    result = await dispatches_collection.insert_one(doc)
    dispatch = await dispatches_collection.find_one({"_id": result.inserted_id})
    
    # Update parcel: assign agent and change status
    await parcel_service.assign_agent(data.parcel_id, data.agent_id)
    await parcel_service.update_parcel_status(data.parcel_id, "In Transit", admin["name"])
    
    await notification_service.create_notification(
        data.agent_id, f"New dispatch assigned to you", "dispatch"
    )
    return serialize_dispatch(dispatch)

@router.put("/dispatch/{dispatch_id}")
async def update_dispatch(dispatch_id: str, data: DispatchUpdate, admin=Depends(require_admin)):
    update_data = {k: v for k, v in data.dict().items() if v is not None}
    
    # Optional validations if IDs are being updated
    try:
        if "agent_id" in update_data:
            agent = await users_collection.find_one({"_id": ObjectId(update_data["agent_id"]), "role": "agent"})
            if not agent: raise HTTPException(status_code=404, detail="Agent not found")
        if "hub_id" in update_data:
            hub = await hubs_collection.find_one({"_id": ObjectId(update_data["hub_id"])})
            if not hub: raise HTTPException(status_code=404, detail="Hub not found")
        if "route_id" in update_data:
            route = await routes_collection.find_one({"_id": ObjectId(update_data["route_id"])})
            if not route: raise HTTPException(status_code=404, detail="Route not found")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid ID format: {str(e)}")

    await dispatches_collection.update_one({"_id": ObjectId(dispatch_id)}, {"$set": update_data})
    d = await dispatches_collection.find_one({"_id": ObjectId(dispatch_id)})
    
    if d and "agent_id" in update_data:
        # Sync the tied parcel
        await parcel_service.assign_agent(d["parcel_id"], update_data["agent_id"])
        
    return serialize_dispatch(d) if d else HTTPException(404, "Not found")

@router.delete("/dispatch/{dispatch_id}")
async def delete_dispatch(dispatch_id: str, admin=Depends(require_admin)):
    result = await dispatches_collection.delete_one({"_id": ObjectId(dispatch_id)})
    if result.deleted_count == 0:
        raise HTTPException(404, "Dispatch not found")
    return {"message": "Dispatch deleted"}

# ─── BILLING ───
@router.get("/billing")
async def get_all_billing(admin=Depends(require_admin)):
    return await billing_service.get_all_billing()

@router.get("/billing/{billing_id}")
async def get_billing(billing_id: str, admin=Depends(require_admin)):
    b = await billing_service.get_billing_by_id(billing_id)
    if not b:
        raise HTTPException(404, "Billing record not found")
    return b

@router.put("/billing/{billing_id}/pay")
async def mark_paid(billing_id: str, admin=Depends(require_admin)):
    return await billing_service.mark_paid(billing_id)

@router.post("/billing/generate", status_code=201)
async def generate_billing(admin=Depends(require_admin), parcel_id: str = "", customer_name: str = "", amount: float = 0.0):
    return await billing_service.create_billing(parcel_id, customer_name, "", amount)

@router.get("/billing/{billing_id}/download")
async def download_invoice(billing_id: str, admin=Depends(require_admin)):
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

# ─── REPORTS ───
@router.get("/reports/deliveries")
async def report_deliveries(admin=Depends(require_admin)):
    pipeline = [{"$group": {"_id": "$status", "count": {"$sum": 1}}}]
    result = []
    async for doc in parcels_collection.aggregate(pipeline):
        result.append({"status": doc["_id"], "count": doc["count"]})
    return result

@router.get("/reports/revenue")
async def report_revenue(admin=Depends(require_admin)):
    pipeline = [{"$group": {"_id": "$payment_status", "total": {"$sum": "$amount"}}}]
    result = []
    async for doc in billing_collection.aggregate(pipeline):
        result.append({"payment_status": doc["_id"], "total": doc["total"]})
    return result

@router.get("/reports/agents")
async def report_agents(admin=Depends(require_admin)):
    pipeline = [{"$group": {"_id": "$assigned_agent_id", "count": {"$sum": 1}}}]
    result = []
    async for doc in parcels_collection.aggregate(pipeline):
        result.append({"agent_id": doc["_id"], "parcel_count": doc["count"]})
    return result

@router.get("/reports/parcels")
async def report_parcels(admin=Depends(require_admin)):
    total = await parcels_collection.count_documents({})
    delivered = await parcels_collection.count_documents({"status": "Delivered"})
    pending = total - delivered
    return {"total": total, "delivered": delivered, "pending": pending}

# ─── TICKETS ───
def serialize_ticket(t):
    t["id"] = str(t["_id"]); del t["_id"]; return t

@router.get("/tickets")
async def get_tickets(admin=Depends(require_admin)):
    tickets = []
    async for t in tickets_collection.find().sort("created_at", -1):
        tickets.append(serialize_ticket(t))
    return tickets

@router.put("/tickets/{ticket_id}")
async def update_ticket(ticket_id: str, data: dict, admin=Depends(require_admin)):
    data["updated_at"] = datetime.utcnow()
    await tickets_collection.update_one({"_id": ObjectId(ticket_id)}, {"$set": data})
    t = await tickets_collection.find_one({"_id": ObjectId(ticket_id)})
    if t:
        # Notify customer
        await notification_service.create_notification(
            t.get("customer_id", ""), f"Your ticket #{t.get('ticket_id', '')} has been updated", "ticket"
        )
    return serialize_ticket(t) if t else HTTPException(404, "Ticket not found")

# ─── DASHBOARD STATS ───
@router.get("/dashboard")
async def dashboard(admin=Depends(require_admin)):
    total_parcels = await parcels_collection.count_documents({})
    total_agents = await users_collection.count_documents({"role": "agent"})
    total_customers = await users_collection.count_documents({"role": "customer"})
    open_tickets = await tickets_collection.count_documents({"status": "Open"})
    pending_dispatches = await dispatches_collection.count_documents({"status": "Dispatched"})
    
    # Status distribution
    status_pipeline = [{"$group": {"_id": "$status", "count": {"$sum": 1}}}]
    status_dist = []
    async for doc in parcels_collection.aggregate(status_pipeline):
        status_dist.append({"status": doc["_id"], "count": doc["count"]})
    
    # Recent parcels
    recent_parcels = []
    async for p in parcels_collection.find().sort("created_at", -1).limit(5):
        p["id"] = str(p["_id"]); del p["_id"]
        recent_parcels.append(p)

    return {
        "total_parcels": total_parcels,
        "total_agents": total_agents,
        "total_customers": total_customers,
        "open_tickets": open_tickets,
        "pending_dispatches": pending_dispatches,
        "status_distribution": status_dist,
        "recent_parcels": recent_parcels
    }
