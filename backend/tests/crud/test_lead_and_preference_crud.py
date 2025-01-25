from datetime import datetime, timedelta

import pytest
from sqlalchemy.orm import Session

from app.crud.crud_lead import create_lead_with_preference
from app.schemas import LeadCreate, UserPreferenceCreate

def test_create_lead_with_preference_logic(db_session: Session, test_centers):
    lead_data = LeadCreate(email="test@example.com")
    preferences_data = UserPreferenceCreate(
        start_date=datetime.now().date(),
        end_date=datetime.now().date() + timedelta(days=7),
        preferred_centers_ids=[test_centers[0].id, test_centers[1].id]
    )

    result = create_lead_with_preference(db_session, lead_data, preferences_data)

    assert result.lead.email == "test@example.com"
    assert len(result.preferred_centers) == 2
    assert test_centers[0] in result.preferred_centers
    assert test_centers[1] in result.preferred_centers