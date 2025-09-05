from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import api
from app.core.config import settings

app = FastAPI(title=settings.PROJECT_NAME)


# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # In production, replace with your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(api.api_router, prefix=settings.API_V1_STR)