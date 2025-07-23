from fastapi import APIRouter
from app.api.endpoints import auth, centers, lead

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(centers.router, prefix="/centers", tags=["centers"])
api_router.include_router(lead.router, prefix="/lead", tags=["lead"])