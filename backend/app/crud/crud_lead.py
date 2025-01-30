from typing import Type, List

from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func

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

def get_lead_preferences(db: Session) -> List[dict]:
    query = db.query(
        Lead.email,
        func.array_agg(TestCenter.id).label('preferred_centers'),
        UserPreference.start_date,
        UserPreference.end_date
    ).join(UserPreference, Lead.id == UserPreference.lead_id)\
     .join(UserPreference.preferred_centers)\
     .group_by(Lead.email, UserPreference.start_date, UserPreference.end_date)

    return query.all()


def get_lead_preference_to_filter_for_email(db: Session) -> List[dict]:
    lead_preferences = get_lead_preferences(db)
    return _transform_preferences(lead_preferences)


def _transform_preferences(raw_preferences: List[dict]) -> List[dict]:
    """
    Transforms raw query results into a structured dictionary format.
    """
    return [
        {
            'email': email,
            'preferred_locations': preferred_centers,
            'start_date': start_date.isoformat(),
            'end_date': end_date.isoformat()
        }
        for email, preferred_centers, start_date, end_date in raw_preferences
    ]