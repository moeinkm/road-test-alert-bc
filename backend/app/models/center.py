from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.db.base import Base
from app.models.user import user_preferences_centers

# todo: rename to Center to not confuse with test_ files

class Center(Base):
    __tablename__ = "centers"

    id = Column(Integer, primary_key=True, index=True)
    pos_id = Column(Integer, unique=True, nullable=False)
    name = Column(String, unique=True, nullable=False)
    address = Column(String, unique=True, nullable=False)
    city = Column(String, nullable=False)
    url = Column(String, unique=True, nullable=False)
    postal_code = Column(String, unique=True, nullable=False)
    lat = Column(Integer, nullable=False)
    lng = Column(Integer, nullable=False)

    user_preferences = relationship(
        "UserPreference",
        secondary=user_preferences_centers,
        back_populates="preferred_centers"
    )
