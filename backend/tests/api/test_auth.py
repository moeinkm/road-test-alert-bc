from urllib.parse import urljoin
from typing import Any

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.models import User
from app.core.security import get_password_hash

from app.main import app
from app.models import User
from app.schemas import UserCreate
from app.core.security import get_password_hash
from app.core.config import settings


class TestAuthEndpoints:
    """Test suite for authentication endpoints."""

    @pytest.mark.parametrize(
        "email,password,expected_status,expected_message",
        [
            ("test@example.com", "password123", 200, None),
            ("dup@example.com", "password", 409, "Email already registered"),
        ]
    )
    def test_signup_scenarios(
        self, 
        client: TestClient, 
        db: Session, 
        get_url: callable,
        email: str, 
        password: str, 
        expected_status: int,
        expected_message: str
    ) -> None:
        """Test various signup scenarios."""
        # Setup duplicate user if needed
        if expected_status == 409:
            user = User(email=email, hashed_password=get_password_hash(password))
            db.add(user)
            db.commit()

        # Execute request
        data = {"email": email, "password": password}
        response = client.post(get_url("auth:signup"), json=data)
        
        # Assert results
        assert response.status_code == expected_status, f"Unexpected status code: {response.status_code}, Expected: {expected_status}, Response: {response.text}"
        if expected_message:
            assert expected_message in response.text
        elif expected_status == 200:
            assert response.json()["email"] == email

    @pytest.mark.parametrize(
        "email,password,db_password,expected_status,expected_message",
        [
            ("signin@example.com", "mypassword", "mypassword", 200, None),
            ("wrongpass@example.com", "wrongpass", "rightpass", 401, "Incorrect email or password"),
            ("nouser@example.com", "any", None, 401, "Incorrect email or password"),
        ]
    )
    def test_signin_scenarios(
        self,
        client: TestClient,
        db: Session,
        get_url: callable,
        email: str,
        password: str,
        db_password: str | None,
        expected_status: int,
        expected_message: str
    ) -> None:
        """Test various signin scenarios."""
        # Setup user if password is provided
        if db_password:
            user = User(email=email, hashed_password=get_password_hash(db_password))
            db.add(user)
            db.commit()

        # Execute request
        data = {"username": email, "password": password}
        response = client.post(get_url("auth:signin"), data=data)

        # Assert results
        assert response.status_code == expected_status, f"Unexpected status code: {response.status_code}, Expected: {expected_status}, Response: {response.text}"
        if expected_message:
            assert expected_message in response.text
        elif expected_status == 200:
            assert "access_token" in response.json()
            assert response.json()["token_type"] == "bearer"
