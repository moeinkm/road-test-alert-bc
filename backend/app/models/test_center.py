from sqlalchemy import Column, Integer, String
from app.db.base import Base

class TestCenter(Base):
    id = Column(Integer, primary_key=True, index=True)
    apos_id = Column(Integer, index=True)
    name = Column(String, index=True)
    address = Column(String)
    city = Column(String, index=True)