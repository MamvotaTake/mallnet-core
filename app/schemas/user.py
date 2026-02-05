from datetime import datetime
from pydantic import BaseModel


class UserResponse(BaseModel):
    id: int
    mall_id: int
    mac_address: str
    created_at: datetime

    class Config:
        from_attributes = True
