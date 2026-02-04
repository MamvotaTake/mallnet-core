from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.sql import func
from app.database.base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    mall_id = Column(
        Integer,
        ForeignKey("malls.id", name="fk_users_mall_id"),
        nullable=False,
        index=True,
    )

    mac_address = Column(String, nullable=True, index=True)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
