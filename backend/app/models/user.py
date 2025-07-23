from calendar import Day
import uuid

from sqlalchemy import Column, String, Boolean, DateTime, Integer, ForeignKey, Table, Date
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID, ARRAY

from app.db.base import Base


user_preferences_centers = Table(
    'user_preferences_centers',
    Base.metadata,
    Column('user_preference_id', UUID, ForeignKey('user_preferences.id')),
    Column('center_id', Integer, ForeignKey('centers.id'))
)

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, index=True, nullable=False)
    full_name = Column(String)
    hashed_password = Column(String, nullable=False)

    is_active = Column(Boolean, default=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    lead = relationship("Lead", back_populates="user", uselist=False)


class Lead(Base):
    __tablename__ = "leads"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    email = Column(String, unique=True, index=True, nullable=False)
    user_id = Column(UUID, ForeignKey("users.id"), nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    user = relationship("User", back_populates="lead", uselist=False)

    preference = relationship("UserPreference", back_populates="lead", uselist=False)


class UserPreference(Base):
    __tablename__ = "user_preferences"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    lead_id = Column(UUID, ForeignKey("leads.id"), nullable=False)
    start_date = Column(Date)
    end_date = Column(Date)
    preferred_days = Column(ARRAY(Integer))

    preferred_centers = relationship("Center", secondary=user_preferences_centers,
                                     back_populates="user_preferences")

    lead = relationship("Lead", back_populates="preference", uselist=False)

    @property
    def days_of_week(self):
        return [Day(day) for day in self.preferred_days]

    @days_of_week.setter
    def days_of_week(self, days):
        self.preferred_days = [day.value for day in days]

