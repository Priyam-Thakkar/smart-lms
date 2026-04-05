from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
from app.database import create_indexes
from app.config import settings

# Import routers
from app.controllers.auth import router as auth_router
from app.controllers.admin import router as admin_router
from app.controllers.agent import router as agent_router
from app.controllers.customer import router as customer_router
from app.controllers.common import router as common_router

app = FastAPI(
    title="Smart Logistics Management System API",
    description="Backend API for LMS with Admin, Agent, Customer roles",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200", "http://127.0.0.1:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve uploaded files statically
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=settings.UPLOAD_DIR), name="uploads")

# Startup event
@app.on_event("startup")
async def startup_event():
    await create_indexes()
    print("✅ MongoDB connected and indexes created")

# Include routers
app.include_router(auth_router, prefix="/api/auth", tags=["Auth"])
app.include_router(admin_router, prefix="/api/admin", tags=["Admin"])
app.include_router(agent_router, prefix="/api/agent", tags=["Agent"])
app.include_router(customer_router, prefix="/api/customer", tags=["Customer"])
app.include_router(common_router, prefix="/api/common", tags=["Common"])

@app.get("/")
async def root():
    return {"message": "Smart Logistics Management System API", "version": "1.0.0", "docs": "/docs"}
