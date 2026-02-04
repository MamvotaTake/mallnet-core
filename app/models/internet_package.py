from sqlalchemy import Column, Integer, String, Float
from app.database.base import Base

class InternetPackage(Base):
    __tablename__ = "internet_packages"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    duration_days = Column(Integer, nullable=False)

    mikrotik_profile = Column(String, nullable=False)

    def __repr__(self):
        return f"<InternetPackage(name={self.name}, price={self.price})>"
