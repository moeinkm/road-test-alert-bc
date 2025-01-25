from pydantic import BaseModel

class TestCenterBase(BaseModel):
    apos_id: int
    name: str
    address: str
    city: str

class TestCenterCreate(TestCenterBase):
    pass

class TestCenterResponse(TestCenterBase):
    id: int

    class Config:
        from_attributes = True
