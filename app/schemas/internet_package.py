from pydantic import BaseModel

class InternetPackageResponse(BaseModel):
    id: int
    name: str
    price: int
    duration_days: int
    mikrotik_profile: str

    class Config:
        from_attributes = True

class InternetPackageCreate(BaseModel):
    name: str
    price: int
    duration_days: int
    mikrotik_profile: str