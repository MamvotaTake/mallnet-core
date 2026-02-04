from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class VoucherCreate(BaseModel):
    package_id: int
    mall_id: int
    expires_at: Optional[datetime] = None


class VoucherResponse(BaseModel):
    id: int
    code: str
    package_id: int
    mall_id: int
    is_used: bool
    used_at: Optional[datetime]
    expires_at: Optional[datetime]

    class Config:
        from_attributes = True
