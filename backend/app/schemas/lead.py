from calendar import Day
import uuid
from datetime import date
from typing import List

from pydantic import BaseModel, model_validator, EmailStr

from .center import CenterResponse


class LeadCreate(BaseModel):
    email: EmailStr

class LeadResponse(BaseModel):
    id: uuid.UUID
    email: EmailStr

    class Config:
        from_attributes = True


class UserPreferenceCreate(BaseModel):
    start_date: date
    end_date: date
    preferred_centers_ids: List[int]
    preferred_days: List[Day]

    @model_validator(mode='after')
    def check_dates(self):
        if self.end_date <= self.start_date:
            raise ValueError('end_date must be after start_date')
        return self


class UserPreferenceResponse(BaseModel):
    id: uuid.UUID
    lead: LeadResponse
    start_date: date
    end_date: date
    preferred_centers: List[CenterResponse]
    preferred_days: List[Day]

    class Config:
        from_attributes = True