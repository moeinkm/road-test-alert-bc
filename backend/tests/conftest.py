import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.db.base import Base
from app.main import app
from app.db.session import get_db
from app.models import TestCenter, Lead

# Create an in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db():
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def client(db):
    def override_get_db():
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client

@pytest.fixture(scope="function")
def test_centers(db):
    centers = [
        TestCenter(name="Center 1", apos_id=69, address="69 Poshti Street", city="No Town"),
        TestCenter(name="Center 2", apos_id=85, address="85 Poshti Alley", city="Shahre No"),
        TestCenter(name="Center 3", apos_id=6985, address="Addresse Pedaret", city="Mahalle Zendegi Pedaret"),
    ]
    db.add_all(centers)
    db.commit()

    return centers

@pytest.fixture(scope="function")
def existing_lead(db):
    lead = Lead(email="existing@example.com")
    db.add(lead)
    db.commit()

    return lead