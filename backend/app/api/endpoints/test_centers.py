from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.crud.crud_test_center import get_test_centers
from app.db.session import get_db
from app.schemas.test_center import TestCenter

router = APIRouter()

@router.get("/", response_model=List[TestCenter])
def read_test_centers(db: Session = Depends(get_db)):
    test_centers = get_test_centers(db)
    return test_centers