from typing import Type, List
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.engine import Row
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import Column, func

from app.crud.crud_user import get_centers
from app.schemas import LeadCreate, UserPreferenceCreate
from app.models import Center, Lead, UserPreference


def get_lead_by_email(db: Session, email: str) -> Type[Lead] | None:
    return db.query(Lead).filter(Lead.email == email).first()


def create_lead(db: Session, lead_in: LeadCreate) -> Lead:
    new_lead = Lead(email=lead_in.email)
    db.add(new_lead)

    return new_lead


def create_preference(db: Session, lead_id: Column[UUID], preferences: UserPreferenceCreate,
                      centers: list[Type[Center]]) -> UserPreference:
    new_preferences = UserPreference(
        lead_id=lead_id,
        start_date=preferences.start_date,
        end_date=preferences.end_date,
        preferred_centers=centers,
        preferred_days = preferences.preferred_days
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
    db.refresh(new_lead)

    centers = get_centers(db, preferences.preferred_centers_ids)
    if len(centers) != len(preferences.preferred_centers_ids):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="One or more invalid test center IDs provided"
        )

    new_preference = create_preference(db, new_lead.id, preferences, centers)
    db.commit()
    db.refresh(new_preference, ['lead', 'preferred_centers'])

    return new_preference


def get_lead_preferences(db: Session) -> List[Row]:
    return db.query(Lead).options(
        joinedload(Lead.preference).joinedload(UserPreference.preferred_centers)
    ).all()