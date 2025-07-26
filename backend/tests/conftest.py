from urllib.parse import urljoin
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.config import settings
from app.db.base import Base
from app.main import app
from app.db.session import get_db
from app.models import Center, Lead


# Use an test dedicated database for testing
SQLALCHEMY_DATABASE_URL = settings.TEST_DATABASE_URL

engine = create_engine(SQLALCHEMY_DATABASE_URL)
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
def centers(db):
    centers = [
        Center(
            id=69,
            name="Center 1",
            pos_id=69,
            address="69 Poshti Street",
            city="No Town",
            url="http://sag.sag",
            postal_code="69",
            lat=69,
            lng=69,
        ),
        Center(
            id=85,
            name="Center 2",
            pos_id=85,
            address="85 Poshti Alley",
            city="Shahre No",
            url="http://gav.gov",
            postal_code="85",
            lat=85,
            lng=85,
        ),
        Center(
            id=6985,
            name="Center 3",
            pos_id=6985,
            address="Addresse Pedaret",
            city="Mahalle Zendegi Pedaret",
            url="http://khar.khar",
            postal_code="6985",
            lat=6985,
            lng=6985,
        ),
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


@pytest.fixture
def get_url():
    """Fixture to generate full URL for named endpoints."""
    def _get_url(name: str) -> str:
        return urljoin(settings.API_V1_STR, app.url_path_for(name))
    return _get_url
