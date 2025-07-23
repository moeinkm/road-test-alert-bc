from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models import Center
from app.schemas import CenterResponse

router = APIRouter()

@router.get("/", response_model=List[CenterResponse])
def read_centers(db: Session = Depends(get_db)):
    centers = db.query(Center).all()

    return centers