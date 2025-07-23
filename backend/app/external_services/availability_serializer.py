from sqlite3.dbapi2 import Date
from pydantic import BaseModel, RootModel, field_validator
from typing import Dict, List, Optional
from datetime import datetime
from calendar import Day
from app.models.center import Center
from app.schemas.center import CenterResponse
from sqlalchemy.orm import Session


class AppointmentDt(BaseModel):
    date: Date
    dayOfWeek: Day

    @field_validator('date', mode='before')
    @classmethod
    def _parse_date(cls, v):
        if isinstance(v, str):
            return datetime.strptime(v, '%Y-%m-%d').date()
        return v

    @field_validator('dayOfWeek', mode='before')
    @classmethod
    def _parse_day(cls, v):
        if isinstance(v, str):
            return Day[v.strip().upper()]
        return v


class DlExam(BaseModel):
    code: str
    description: str


class AvailabilityItem(BaseModel):
    appointmentDt: AppointmentDt
    dlExam: DlExam
    endTm: str
    lemgMsgId: int
    posId: int
    resourceId: int
    signature: str
    startTm: str
    center: Optional[CenterResponse] = None  # The Center schema this slot belongs to

    @classmethod
    def with_center(cls, data: Dict, center: Center) -> 'AvailabilityItem':
        """
        Create an AvailabilityItem with the center object already attached.
        
        Args:
            data: Raw availability item data
            center: The Center object to attach
            
        Returns:
            AvailabilityItem with center attached
        """
        item = cls.model_validate(data)
        # Convert SQLAlchemy model to Pydantic schema
        item.center = CenterResponse.model_validate(center) if center else None
        return item


class AvailabilitySerializer(RootModel[List[AvailabilityItem]]):
    
    @classmethod
    def with_centers(cls, data: List, db: Session) -> 'AvailabilitySerializer':
        """
        Create an AvailabilitySerializer with Center objects attached to each item.
        
        Args:
            data: Raw availability data from API
            db: Database session to lookup centers
            
        Returns:
            AvailabilitySerializer with centers attached
        """
        # Get all unique pos_ids
        pos_ids = list(set(item.get('posId') for item in data))
        
        # Query only the specific centers we need by pos_id
        centers = db.query(Center).filter(Center.pos_id.in_(pos_ids)).all()
        center_map = {center.pos_id: center for center in centers}
        
        # Create items with centers attached during creation
        items_with_centers = []
        for item_data in data:
            center = center_map.get(item_data.get('posId'))
            item = AvailabilityItem.with_center(item_data, center)
            items_with_centers.append(item)
            
        return cls.model_validate(items_with_centers)
