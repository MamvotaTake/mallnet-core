from pydantic import BaseModel
from datetime import datetime


class SubscriptionCreate(BaseModel):
    mall_id: int
    package_id: int
    mac_address: str


class SubscriptionResponse(BaseModel):
    id: int
    user_id: int
    package_id: int
    start_date: datetime
    end_date: datetime
    is_active: bool

    class Config:
        from_attributes = True
