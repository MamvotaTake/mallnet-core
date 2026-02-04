from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class PaymentCreate(BaseModel):
    user_id: int
    package_id: int
    method: str
    reference: Optional[str] = None


class PaymentResponse(BaseModel):
    id: int
    user_id: int
    package_id: int
    amount: float
    method: str
    reference: Optional[str] = None
    paid_at: datetime

    class Config:
        orm_mode = True
