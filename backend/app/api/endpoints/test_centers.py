from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models import TestCenter
from app.schemas import TestCenterResponse

router = APIRouter()

@router.get("/", response_model=List[TestCenterResponse])
def read_test_centers(db: Session = Depends(get_db)):
    test_centers = db.query(TestCenter).all()

    return test_centers