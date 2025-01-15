from fastapi import APIRouter
from app.api.endpoints import auth, test_centers

api_router = APIRouter()
api_router.include_router(auth.router, tags=["login"])
api_router.include_router(test_centers.router, prefix="/centers", tags=["centers"])