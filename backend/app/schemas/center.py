from pydantic import BaseModel



class CenterResponse(BaseModel):
    id: int
    pos_id: int
    name: str
    address: str
    city: str

    class Config:
        from_attributes = True
