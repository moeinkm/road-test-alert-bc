from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from app.core.config import settings
from app.models import Lead



class TestUserPreferencesAPI:

    def test_submit_form_success(self, client: TestClient, db: Session, test_centers):
        payload = {
            "lead": {
                "email": "test@example.com"
            },
            "preferences": {
                "start_date": datetime.now().date().isoformat(),
                "end_date": (datetime.now().date() + timedelta(days=7)).isoformat(),
                "preferred_centers_ids": [test_centers[0].id, test_centers[1].id]
            }
        }

        response = client.post(f"{settings.API_V1_STR}/lead/create", json=payload)
        assert response.status_code == 201
        data = response.json()
        assert data["lead"]["email"] == "test@example.com"
        assert "id" in data

        # Verify that the lead was actually created in the database
        created_lead = db.query(Lead).filter(Lead.email == "test@example.com").first()
        assert created_lead is not None

    def test_submit_form_duplicate_email(self, client: TestClient, db: Session, existing_lead):
        payload = {
            "lead": {
                "email": "existing@example.com"
            },
            "preferences": {
                "start_date": datetime.now().date().isoformat(),
                "end_date": (datetime.now().date() + timedelta(days=7)).isoformat(),
                "preferred_centers_ids": []
            }
        }

        response = client.post(f"{settings.API_V1_STR}/lead/create", json=payload)
        assert response.status_code == 409

    def test_submit_form_invalid_center_ids(self, client: TestClient, db: Session):
        payload = {
            "lead": {
                "email": "test@example.com"
            },
            "preferences": {
                "start_date": datetime.now().date().isoformat(),
                "end_date": (datetime.now().date() + timedelta(days=7)).isoformat(),
                "preferred_centers_ids": [999]  # Non-existent center ID
            }
        }

        response = client.post(f"{settings.API_V1_STR}/lead/create", json=payload)
        assert response.status_code == 400

    def test_submit_form_invalid_dates(self, client: TestClient):
        payload = {
            "lead": {
                "email": "test@example.com"
            },
            "preferences": {
                "start_date": (datetime.now().date() + timedelta(days=7)).isoformat(),
                "end_date": datetime.now().date().isoformat(),
                "preferred_centers_ids": []
            }
        }

        response = client.post(f"{settings.API_V1_STR}/lead/create", json=payload)
        assert response.status_code == 422
