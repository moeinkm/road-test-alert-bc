import uuid

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.db.base import Base
from app.models.user import user_preferences_centers


class TestCenter(Base):
    __tablename__ = "test_centers"

    id = Column(Integer, primary_key=True, index=True)
    apos_id = Column(Integer)
    name = Column(String)
    address = Column(String)
    city = Column(String)

    user_preferences = relationship(
        "UserPreference",
        secondary=user_preferences_centers,
        back_populates="preferred_centers"
    )
