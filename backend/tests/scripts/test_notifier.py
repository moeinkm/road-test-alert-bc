import calendar
import pytest
from unittest.mock import patch, MagicMock, Mock
from datetime import date
from calendar import Day
from collections import defaultdict
from sqlalchemy import Row
from typing import Optional, List

from app.external_services import notifier
from app.external_services.availability_serializer import AvailabilityItem, AppointmentDt, DlExam
from app.schemas.center import CenterResponse



@pytest.fixture
def sample_availability_item(centers):
    """Create a sample AvailabilityItem."""
    appointment_dt = AppointmentDt(
        date=date(2024, 6, 10),
        dayOfWeek=Day.MONDAY
    )
    dl_exam = DlExam(
        code="5-R-1",
        description="5-R-ROAD"
    )
    
    item = AvailabilityItem(
        appointmentDt=appointment_dt,
        dlExam=dl_exam,
        endTm="10:30",
        lemgMsgId=35,
        posId=274,
        resourceId=21903,
        signature="test_signature",
        startTm="09:00",
        center=CenterResponse.model_validate(centers[0])
    )
    return item


@pytest.fixture
def sample_lead_preference(centers):
    """Create a sample Lead ORM object with preference and preferred_centers."""
    # Mock the UserPreference object
    mock_preference = Mock()
    mock_preference.preferred_centers = [centers[0], centers[1]]
    mock_preference.preferred_days = [0, 1, 4]  # Monday, Tuesday, Friday
    mock_preference.start_date = date(2024, 6, 1)
    mock_preference.end_date = date(2024, 6, 30)
    
    # Mock the Lead object
    mock_lead = Mock()
    mock_lead.email = "test@example.com"
    mock_lead.preference = mock_preference

    return mock_lead


@pytest.fixture
def sample_availability_data(sample_availability_item):
    """Create sample availability data."""
    return [sample_availability_item]


@pytest.fixture
def mock_gmail_service():
    """Create a mock Gmail service."""
    service = MagicMock()
    service.create_message.return_value = "mock_message"
    service.send_message.return_value = None
    return service


class TestMatchAvailabilityToUsers:
    """Test the match_availability_to_users function."""
    
    def test_matches_user_preferences(self, sample_availability_data, sample_lead_preference, centers):
        """Test that availability is correctly matched to user preferences."""
        result = notifier.match_availability_to_users(sample_availability_data, sample_lead_preference)
        assert isinstance(result, defaultdict)
        expected_name = sample_availability_data[0].center.name
        assert expected_name in result.keys()
        assert len(result[expected_name]) == 1
        assert result[expected_name][0] == sample_availability_data[0]
    
    def test_no_matches_when_center_not_preferred(self, sample_availability_data, sample_lead_preference, centers):
        """Test that items are not matched when center is not in user preferences."""
        sample_lead_preference.preference.preferred_centers = [centers[2]]  # Different center
        
        result = notifier.match_availability_to_users(sample_availability_data, sample_lead_preference)
        
        assert len(result) == 0
    
    def test_no_matches_when_day_not_preferred(self, sample_availability_data, sample_lead_preference):
        """Test that items are not matched when day is not in user preferences."""
        sample_lead_preference.preference.preferred_days = [3, 4]  # Wednesday, Thursday
        
        result = notifier.match_availability_to_users(sample_availability_data, sample_lead_preference)
        
        assert len(result) == 0
    
    def test_no_matches_when_date_out_of_range(self, sample_availability_data, sample_lead_preference):
        """Test that items are not matched when date is out of user's preferred range."""
        sample_lead_preference.preference.start_date = date(2024, 7, 1)
        sample_lead_preference.preference.end_date = date(2024, 7, 31)
        
        result = notifier.match_availability_to_users(sample_availability_data, sample_lead_preference)
        
        assert len(result) == 0


class TestPrepareMessage:
    """Test the prepare_message function."""
    
    def test_generates_valid_html(self, sample_availability_data):
        """Test that the function generates valid HTML content."""
        available_slots = defaultdict(list)
        available_slots["Vancouver ICBC Test Center"] = sample_availability_data
        
        html = notifier.prepare_message(available_slots)
        
        assert "<html>" in html
        assert "<body>" in html
        assert "ICBC Road Test Availability" in html
        assert "Vancouver ICBC Test Center" in html
        assert "2024-06-10" in html
        assert "Monday" in html
        assert "09:00" in html
        assert "10:30" in html
    
    def test_handles_empty_slots(self):
        """Test that function handles empty availability slots."""
        available_slots = defaultdict(list)
        
        html = notifier.prepare_message(available_slots)
        
        assert "<html>" in html
        assert "ICBC Road Test Availability" in html
        assert "<ul></ul>" in html
    
    def test_handles_multiple_centers(self, sample_availability_data):
        """Test that function handles multiple centers correctly."""
        available_slots = defaultdict(list)
        available_slots["Center A"] = sample_availability_data
        available_slots["Center B"] = sample_availability_data
        
        html = notifier.prepare_message(available_slots)
        
        assert "Center A" in html
        assert "Center B" in html


class TestNotifyLeadByPreference:
    """Test the notify_lead_by_preference function."""
    
    def test_notifies_leads_with_matches(self, sample_lead_preference, sample_availability_data, mock_gmail_service):
        """Test that leads with matching availability are notified."""
        lead_preferences = [sample_lead_preference]  # type: ignore
        
        notifier.notify_lead_by_preference(lead_preferences, sample_availability_data, mock_gmail_service)
        
        mock_gmail_service.create_message.assert_called_once()
        mock_gmail_service.send_message.assert_called_once()
    
    def test_skips_leads_without_email(self, sample_availability_data, mock_gmail_service):
        """Test that leads without email addresses are skipped."""
        lead_preference = Mock()
        lead_preference.email = None  # No email
        # Add a .preference attribute with required fields
        mock_pref = Mock()
        mock_pref.preferred_centers = []
        mock_pref.preferred_days = []
        mock_pref.start_date = date(2024, 6, 1)
        mock_pref.end_date = date(2024, 6, 30)
        lead_preference.preference = mock_pref
        lead_preferences = [lead_preference]
        
        notifier.notify_lead_by_preference(lead_preferences, sample_availability_data, mock_gmail_service)
        
        mock_gmail_service.create_message.assert_not_called()
        mock_gmail_service.send_message.assert_not_called()
    
    def test_skips_leads_without_matches(self, sample_lead_preference, mock_gmail_service, centers):
        """Test that leads without matching availability are skipped."""
        sample_lead_preference.preference.preferred_centers = [centers[2]]  # No matching centers
        lead_preferences = [sample_lead_preference]
        availability_data = []
        
        notifier.notify_lead_by_preference(lead_preferences, availability_data, mock_gmail_service)
        
        mock_gmail_service.create_message.assert_not_called()
        mock_gmail_service.send_message.assert_not_called()
    
    def test_handles_email_send_failures(self, sample_lead_preference, sample_availability_data, mock_gmail_service):
        """Test that email send failures are handled gracefully."""
        mock_gmail_service.send_message.side_effect = Exception("Send failed")
        lead_preferences = [sample_lead_preference]
        
        # Should not raise exception
        notifier.notify_lead_by_preference(lead_preferences, sample_availability_data, mock_gmail_service)


class TestMainFunction:
    """Test the main function end-to-end."""
    
    def test_successful_notification_flow(self, sample_availability_data, sample_lead_preference):
        """Test the complete notification flow from start to finish."""
        # Mock all external dependencies
        mock_db = Mock()
        mock_session = Mock()
        mock_gmail_service = MagicMock()
        mock_gmail_service.create_message.return_value = "mock_message"
        
        with patch('app.external_services.notifier.db_session_as_context') as mock_context, \
             patch('app.external_services.notifier.find_available_dates', return_value=(sample_availability_data, True)), \
             patch('app.external_services.notifier.get_lead_preferences', return_value=[sample_lead_preference]), \
             patch('app.external_services.notifier.SMTPGmailService', return_value=mock_gmail_service):
            
            mock_context.return_value.__enter__.side_effect = [mock_db, mock_session]
            mock_context.return_value.__exit__.return_value = None
            
            notifier.main()
        
        mock_gmail_service.close_connection.assert_called_once()
    
    def test_handles_no_availability_data(self):
        """Test that main function handles case when no availability data is found."""
        with patch('app.external_services.notifier.db_session_as_context'), \
             patch('app.external_services.notifier.find_available_dates', return_value=None):
            
            notifier.main()
    
    def test_handles_empty_availability_list(self):
        """Test that main function handles case when availability list is empty."""
        with patch('app.external_services.notifier.db_session_as_context'), \
             patch('app.external_services.notifier.find_available_dates', return_value=([], True)):
            
            notifier.main()
    
    def test_handles_gmail_service_error(self, sample_availability_data, sample_lead_preference):
        """Test that main function handles Gmail service errors gracefully."""
        mock_db = Mock()
        mock_session = Mock()
        
        with patch('app.external_services.notifier.db_session_as_context') as mock_context, \
             patch('app.external_services.notifier.find_available_dates', return_value=(sample_availability_data, True)), \
             patch('app.external_services.notifier.get_lead_preferences', return_value=[sample_lead_preference]), \
             patch('app.external_services.notifier.SMTPGmailService', side_effect=Exception("Gmail error")):
            
            mock_context.return_value.__enter__.side_effect = [mock_db, mock_session]
            mock_context.return_value.__exit__.return_value = None
            
            # Should not raise exception
            notifier.main()


class TestEndToEndIntegration:
    """End-to-end integration tests for the notifier system."""
    
    def test_complete_notification_workflow(self, centers):
        """Test the complete notification workflow with real data structures."""
        # Create realistic test data
        appointment_dt = AppointmentDt(
            date=date(2024, 6, 10),
            dayOfWeek=Day.MONDAY
        )
        dl_exam = DlExam(code="5-R-1", description="5-R-ROAD")
        
        availability_item = AvailabilityItem(
            appointmentDt=appointment_dt,
            dlExam=dl_exam,
            endTm="10:30",
            lemgMsgId=35,
            posId=centers[0].pos_id,
            resourceId=21903,
            signature="test_signature",
            startTm="09:00",
            center=CenterResponse.model_validate(centers[0])
        )
        
        lead_preference = Mock()
        lead_preference.email = "test@example.com"
        lead_preference.preference = Mock()
        lead_preference.preference.preferred_centers = [centers[0]]
        lead_preference.preference.preferred_days = [0]  # Monday
        lead_preference.preference.start_date = date(2024, 6, 1)
        lead_preference.preference.end_date = date(2024, 6, 30)
        
        # Test the complete flow
        availability_data = [availability_item]
        lead_preferences = [lead_preference]
        mock_gmail_service = MagicMock()
        mock_gmail_service.create_message.return_value = "mock_message"
        
        # Test matching
        matched = notifier.match_availability_to_users(availability_data, lead_preference)
        expected_name = centers[0].name
        assert expected_name in matched
        assert len(matched[expected_name]) == 1
        
        # Test message preparation
        html = notifier.prepare_message(matched)
        assert expected_name in html
        assert "2024-06-10" in html
        assert "Monday" in html
        
        # Test notification
        notifier.notify_lead_by_preference(lead_preferences, availability_data, mock_gmail_service)  # type: ignore
        mock_gmail_service.create_message.assert_called_once()
        mock_gmail_service.send_message.assert_called_once()


class TestAvailabilitySerializerIntegration:
    """Test integration with the availability serializer."""
    
    def test_availability_item_with_center(self, centers):
        """Test creating AvailabilityItem with center attached."""
        raw_data = {
            "appointmentDt": {
                "date": "2024-06-10",
                "dayOfWeek": "Monday"
            },
            "dlExam": {
                "code": "5-R-1",
                "description": "5-R-ROAD"
            },
            "endTm": "10:30",
            "lemgMsgId": 35,
            "posId": 69,
            "resourceId": 21903,
            "signature": "test_signature",
            "startTm": "09:00"
        }

        item = AvailabilityItem.with_center(raw_data, centers[0])
        
        assert item.center == CenterResponse.model_validate(centers[0])
        assert item.posId == centers[0].pos_id
        assert item.appointmentDt.date == date(2024, 6, 10)
        assert item.appointmentDt.dayOfWeek == Day.MONDAY
    
    def test_availability_serializer_with_centers(self, centers):
        """Test creating AvailabilitySerializer with centers attached."""
        from app.external_services.availability_serializer import AvailabilitySerializer
        
        raw_data = [{
            "appointmentDt": {
                "date": "2024-06-10",
                "dayOfWeek": "Monday"
            },
            "dlExam": {
                "code": "5-R-1",
                "description": "5-R-ROAD"
            },
            "endTm": "10:30",
            "lemgMsgId": 35,
            "posId": 69,
            "resourceId": 21903,
            "signature": "test_signature",
            "startTm": "09:00"
        }]
        
        mock_db = Mock()
        mock_db.query.return_value.filter.return_value.all.return_value = [centers[0]]
        
        serializer = AvailabilitySerializer.with_centers(raw_data, mock_db)
        
        assert len(serializer.root) == 1
        assert serializer.root[0].center == CenterResponse.model_validate(centers[0])
        assert serializer.root[0].posId == 69
