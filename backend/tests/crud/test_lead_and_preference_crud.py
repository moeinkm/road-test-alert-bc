from calendar import Day
from datetime import datetime, timedelta

import pytest
from sqlalchemy.orm import Session
from app.crud.crud_lead import (
    create_lead_with_preference,
    get_lead_preferences
)
from app.schemas import LeadCreate, UserPreferenceCreate


class TestLeadAndPreferenceCRUD:
    """Test class for lead and preference CRUD operations."""
    
    @pytest.fixture(autouse=True)
    def setup(self, db: Session, centers):
        """Setup test data for each test method."""
        self.db = db
        self.centers = centers
        self.base_date = datetime.now().date()
        self.end_date = self.base_date + timedelta(days=7)
    
    def test_create_lead_with_preference_logic(self):
        """Test creating a lead with associated preferences."""
        # Arrange
        lead_data = LeadCreate(email="test@example.com")
        preferences_data = UserPreferenceCreate(
            start_date=self.base_date,
            end_date=self.end_date,
            preferred_centers_ids=[self.centers[0].id, self.centers[1].id],
            preferred_days=[Day.MONDAY, Day.WEDNESDAY]
        )

        # Act
        result = create_lead_with_preference(self.db, lead_data, preferences_data)

        # Assert
        assert result.lead.email == "test@example.com"
        assert len(result.preferred_centers) == 2
        assert self.centers[0] in result.preferred_centers
        assert self.centers[1] in result.preferred_centers

    def test_get_lead_preferences_raw_query(self):
        """
        Test the raw query logic of get_lead_preferences.
        Ensure it returns the correct data structure and values.
        """
        # Arrange: Create a lead and associated preferences
        lead_data = LeadCreate(email="test@example.com")
        preferences_data = UserPreferenceCreate(
            start_date=self.base_date,
            end_date=self.end_date,
            preferred_centers_ids=[self.centers[0].id, self.centers[2].id],
            preferred_days=[Day.MONDAY, Day.TUESDAY]
        )

        create_lead_with_preference(self.db, lead_data, preferences_data)

        # Act: Call the function under test
        result = get_lead_preferences(self.db)

        # Assert: Ensure the results match the stored data
        assert len(result) == 1
        lead = result[0]
        assert lead.email == "test@example.com"
        pref = lead.preference
        assert pref is not None
        assert set([c.id for c in pref.preferred_centers]) == {self.centers[0].id, self.centers[2].id}
        assert pref.start_date == self.base_date
        assert pref.end_date == self.end_date
        assert pref.preferred_days == [Day.MONDAY, Day.TUESDAY]
