from sqlalchemy import Column, Integer, String
from app.database.base import Base

class Mall(Base):
    __tablename__ = "malls"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    location = Column(String)
