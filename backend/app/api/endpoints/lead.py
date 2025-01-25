from fastapi import Depends, status, APIRouter
from sqlalchemy.orm import Session

from app.crud.crud_lead import create_lead_with_preference
from app.db.session import get_db
from app.schemas import LeadCreate, UserPreferenceCreate, UserPreferenceResponse


router = APIRouter()

@router.post("/create", response_model=UserPreferenceResponse, status_code=status.HTTP_201_CREATED)
def submit_form(lead: LeadCreate, preferences: UserPreferenceCreate, db: Session = Depends(get_db)):
    return create_lead_with_preference(db, lead, preferences)