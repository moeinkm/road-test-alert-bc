from datetime import date
from typing import List

from pydantic import BaseModel, model_validator, EmailStr

from .test_center import TestCenterResponse


class LeadCreate(BaseModel):
    email: EmailStr

class LeadResponse(BaseModel):
    id: int
    email: EmailStr

    class Config:
        from_attributes = True


class UserPreferenceCreate(BaseModel):
    start_date: date
    end_date: date
    preferred_centers_ids: List[int]

    @model_validator(mode='after')
    def check_dates(self):
        if self.end_date <= self.start_date:
            raise ValueError('end_date must be after start_date')
        return self


class UserPreferenceResponse(BaseModel):
    id: int
    lead: LeadResponse
    start_date: date
    end_date: date
    preferred_centers: List[TestCenterResponse]

    class Config:
        from_attributes = True