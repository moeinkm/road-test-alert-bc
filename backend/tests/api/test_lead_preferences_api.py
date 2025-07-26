from calendar import Day
from urllib.parse import urljoin
import json
from datetime import datetime, timedelta

import pytest
from pytest_snapshot.plugin import Snapshot
from fastapi.testclient import TestClient
from pydantic import ValidationError
from sqlalchemy.orm import Session

from app.main import app
from app.core.config import settings
from app.schemas import UserPreferenceCreate


class TestUserPreferencesAPI:
    """Test suite for lead preferences endpoints."""

    def test_submit_form_success(self, client: TestClient, db: Session, centers, get_url):
        from app.models import Lead

        payload = {
            "lead": {
                "email": "test@example.com"
            },
            "preferences": {
                "start_date": datetime(year=1997, month=2, day=17).date().isoformat(),
                "end_date": (datetime(year=1997, month=2, day=17).date() + timedelta(days=7)).isoformat(),
                "preferred_centers_ids": [centers[0].id, centers[1].id],
                "preferred_days": [Day.MONDAY.value, Day.WEDNESDAY.value]
            }
        }
        response = client.post(get_url("lead:create"), json=payload)
        assert response.status_code == 201
        data = response.json()
        assert data["lead"]["email"] == "test@example.com"
        assert "id" in data
        assert data["preferred_days"] == [Day.MONDAY.value, Day.WEDNESDAY.value]

        created_lead = db.query(Lead).filter(Lead.email == "test@example.com").first()
        assert created_lead is not None

    def test_submit_form_duplicate_email(self, client: TestClient, db: Session, existing_lead, snapshot: Snapshot, get_url):
        payload = {
            "lead": {
                "email": "existing@example.com"
            },
            "preferences": {
                "start_date": datetime(year=1997, month=2, day=17).date().isoformat(),
                "end_date": (datetime(year=1997, month=2, day=17).date() + timedelta(days=7)).isoformat(),
                "preferred_centers_ids": [],
                "preferred_days": [Day.MONDAY.value, Day.WEDNESDAY.value]
            }
        }
        url = settings.API_V1_STR + get_url("lead:create")
        response = client.post(get_url("lead:create"), json=payload)
        snapshot.assert_match(json.dumps(response.json()), "test_submit_form_duplicate_email_response")
        assert response.status_code == 409

    def test_submit_form_invalid_center_ids(self, client: TestClient, db: Session, snapshot: Snapshot, get_url):
        payload = {
            "lead": {
                "email": "test@example.com"
            },
            "preferences": {
                "start_date": datetime(year=1997, month=2, day=17).date().isoformat(),
                "end_date": (datetime(year=1997, month=2, day=17).date() + timedelta(days=7)).isoformat(),
                "preferred_centers_ids": [999],  # Non-existent center ID
                "preferred_days": [Day.MONDAY.value, Day.WEDNESDAY.value]
            }
        }
        response = client.post(get_url("lead:create"), json=payload)
        snapshot.assert_match(json.dumps(response.json()), "test_submit_form_invalid_center_ids_response")
        assert response.status_code == 400

    def test_submit_form_invalid_dates(self, client: TestClient, snapshot: Snapshot, get_url):
        payload = {
            "lead": {
                "email": "test@example.com"
            },
            "preferences": {
                "start_date": (datetime(year=1997, month=2, day=17).date() + timedelta(days=7)).isoformat(),
                "end_date": datetime(year=1997, month=2, day=17).date().isoformat(),
                "preferred_centers_ids": [],
                "preferred_days": [Day.MONDAY.value, Day.WEDNESDAY.value]
            }
        }
        response = client.post(get_url("lead:create"), json=payload)
        snapshot.assert_match(json.dumps(response.json()), "test_submit_form_invalid_dates_response")
        assert response.status_code == 422

    def test_invalid_day_of_week_in_preferences(db: Session, centers):
        """
        Test for providing an invalid day of the week in user preferences.
        Ensure the system raises an error or handles it gracefully.
        """
        with pytest.raises(ValidationError):
            UserPreferenceCreate(
                start_date=datetime(year=1997, month=2, day=17).date(),
                end_date=datetime(year=1997, month=2, day=17).date() + timedelta(days=7),
                preferred_centers_ids=[centers[0].id],
                preferred_days=[Day.MONDAY, 7]  # 7 is invalid day of the week
            )

