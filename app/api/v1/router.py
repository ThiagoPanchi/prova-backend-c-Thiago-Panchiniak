from fastapi import APIRouter

from app.api.v1.routes import ai_processing, auth, health, missions

api_router = APIRouter()
api_router.include_router(auth.router)
api_router.include_router(health.router, tags=["health"])
api_router.include_router(missions.router)
api_router.include_router(ai_processing.router)
