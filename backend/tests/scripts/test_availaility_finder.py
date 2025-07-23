import calendar
import datetime
import pytest
from unittest.mock import patch, MagicMock
from app.external_services.crawlers.availability_finder import find_available_dates
from app.schemas.center import CenterResponse

@patch("app.external_services.crawlers.availability_finder.get_auth_token")
@patch("app.external_services.crawlers.availability_finder.requests.post")
def test_find_available_dates_success(mock_requests_post, mock_get_auth_token, db, centers):
    mock_get_auth_token.return_value = "Bearer mock_token"

    # Prepare a different response for each test center
    def mock_post(url, headers, json):
        pos_id = json['aPosID']
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.raise_for_status = MagicMock()
        # Each center gets a unique appointment
        mock_response.json.return_value = [
            {
                "appointmentDt": {
                    "date": f"2023-12-01",  # unique date per center
                    "dayOfWeek": "Friday",
                },
                "dlExam": {
                    "code": "5-R-1",
                    "description": "5-R-ROAD"
                },
                "endTm": "10:30",
                "lemgMsgId": 35,
                "posId": pos_id,
                "resourceId": 21903,
                "signature": f"test_signature{pos_id}",
                "startTm": "09:00",
            }
        ]
        return mock_response

    mock_requests_post.side_effect = mock_post

    # Act
    results, available_not_only_today = find_available_dates(db)

    # Assert: Ensure the results are correctly processed
    assert len(results) == len(centers)
    assert available_not_only_today is True

    # Check each appointment's details
    for i, result in enumerate(results):
        center = centers[i]
        assert result.appointmentDt.date == datetime.date(2023, 12, 1)
        assert result.appointmentDt.dayOfWeek == calendar.FRIDAY
        assert result.center is not None
        assert isinstance(result.center, CenterResponse)
        assert result.center.pos_id == center.pos_id

    assert mock_requests_post.called
    assert mock_get_auth_token.called
