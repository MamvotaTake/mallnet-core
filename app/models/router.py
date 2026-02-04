from sqlalchemy import Column, Integer, String, ForeignKey
from app.database.base import Base

class Router(Base):
    __tablename__ = "routers"

    id = Column(Integer, primary_key=True)

    mall_id = Column(
        Integer,
        ForeignKey("malls.id", name="fk_routers_mall_id"),
        nullable=False,
    )

    name = Column(String, nullable=False)
    host = Column(String, nullable=False)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)
    api_port = Column(Integer, default=8728)
