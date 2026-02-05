from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class VoucherCreate(BaseModel):
    package_id: int
    mall_id: int
    expires_at: Optional[datetime] = None


class VoucherRedeem(BaseModel):
    mall_id: int
    mac_address: str
    code: str
    pin: str


class VoucherResponse(BaseModel):
    id: int
    code: str
    pin: str
    mikrotik_profile: str
    duration_days: int
    package_id: int
    mall_id: int
    is_used: bool
    used_at: Optional[datetime]
    expires_at: Optional[datetime]
    created_at: datetime

    class Config:
        from_attributes = True
