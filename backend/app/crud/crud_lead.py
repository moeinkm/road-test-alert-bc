from typing import Type

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.crud.crud_user import get_test_centers
from app.schemas import LeadCreate, UserPreferenceCreate
from app.models import TestCenter, Lead, UserPreference


def get_lead_by_email(db: Session, email: str) -> Type[Lead] | None:
    return db.query(Lead).filter(Lead.email == email).first()



def create_lead(db: Session, lead_in: LeadCreate) -> Lead:
    new_lead = Lead(email=lead_in.email)
    db.add(new_lead)

    return new_lead


def create_preference(db: Session, lead_id: int, preferences: UserPreferenceCreate,
                      test_centers: list[Type[TestCenter]]) -> UserPreference:
    new_preferences = UserPreference(
        lead_id=lead_id,
        start_date=preferences.start_date,
        end_date=preferences.end_date,
        preferred_centers=test_centers
    )
    db.add(new_preferences)

    return new_preferences



def create_lead_with_preference(db: Session, lead_in: LeadCreate, preferences: UserPreferenceCreate) -> Lead:
    existing_lead = get_lead_by_email(db, str(lead_in.email))
    if existing_lead:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Lead with this email already exists"
        )

    new_lead = create_lead(db, lead_in)
    db.flush()

    test_centers = get_test_centers(db, preferences.preferred_centers_ids)
    if len(test_centers) != len(preferences.preferred_centers_ids):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="One or more invalid test center IDs provided"
        )

    new_preference = create_preference(db, new_lead.id, preferences, test_centers)
    db.commit()
    db.refresh(new_preference, ['lead', 'preferred_centers'])

    return new_preference
