from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from app.crud.crud_lead import create_lead_with_preference, get_lead_preferences, \
    get_lead_preference_to_filter_for_email
from app.schemas import LeadCreate, UserPreferenceCreate

def test_create_lead_with_preference_logic(db: Session, test_centers):
    lead_data = LeadCreate(email="test@example.com")
    preferences_data = UserPreferenceCreate(
        start_date=datetime.now().date(),
        end_date=datetime.now().date() + timedelta(days=7),
        preferred_centers_ids=[test_centers[0].id, test_centers[1].id]
    )

    result = create_lead_with_preference(db, lead_data, preferences_data)

    assert result.lead.email == "test@example.com"
    assert len(result.preferred_centers) == 2
    assert test_centers[0] in result.preferred_centers
    assert test_centers[1] in result.preferred_centers

def test_get_lead_preferences_raw_query(db: Session, test_centers):
    """
    Test the raw query logic of get_lead_preferences.
    Ensure it returns the correct data structure and values.
    """
    # Arrange: Create a lead and associated preferences
    lead_data = LeadCreate(email="test@example.com")
    preferences_data = UserPreferenceCreate(
        start_date=datetime.now().date(),
        end_date=datetime.now().date() + timedelta(days=7),
        preferred_centers_ids=[test_centers[0].id, test_centers[2].id]
    )

    create_lead_with_preference(db, lead_data, preferences_data)

    # Act: Call the function under test
    result = get_lead_preferences(db)

    # Assert: Ensure the results match the stored data
    assert len(result) == 1
    email, preferred_centers, start_date, end_date = result[0]
    assert email == "test@example.com"
    assert set(preferred_centers) == {69, 6985}  # Test center names
    assert start_date == datetime.now().date()
    assert end_date == datetime.now().date() + timedelta(days=7)


def test_get_lead_preference_to_filter_for_email(db: Session, test_centers):
    """
    Test the get_lead_preference_to_filter_for_email function, including
    data transformation via _transform_preferences.
    """
    # Arrange: Create leads and associated preferences
    lead_data1 = LeadCreate(email="lead1@example.com")
    lead_data2 = LeadCreate(email="lead2@example.com")
    preferences_data1 = UserPreferenceCreate(
        start_date=datetime(2023, 11, 1).date(),
        end_date=datetime(2023, 11, 15).date(),
        preferred_centers_ids=[test_centers[0].id, test_centers[1].id],  # 69 and 85
    )
    preferences_data2 = UserPreferenceCreate(
        start_date=datetime(2023, 12, 1).date(),
        end_date=datetime(2023, 12, 10).date(),
        preferred_centers_ids=[test_centers[1].id, test_centers[2].id],  # 85 and 6985
    )
    create_lead_with_preference(db, lead_data1, preferences_data1)
    create_lead_with_preference(db, lead_data2, preferences_data2)

    # Act: Call the function under test
    result = get_lead_preference_to_filter_for_email(db)

    # Assert: Verify the structure and correctness of the transformed data
    expected = [
        {
            "email": "lead1@example.com",
            "preferred_locations": [69, 85],
            "start_date": "2023-11-01",
            "end_date": "2023-11-15",
        },
        {
            "email": "lead2@example.com",
            "preferred_locations": [85, 6985],
            "start_date": "2023-12-01",
            "end_date": "2023-12-10",
        },
    ]
    assert len(result) == len(expected)
    for item, expected_item in zip(result, expected):
        assert item["email"] == expected_item["email"]
        assert set(item["preferred_locations"]) == set(expected_item["preferred_locations"])
        assert item["start_date"] == expected_item["start_date"]
        assert item["end_date"] == expected_item["end_date"]
