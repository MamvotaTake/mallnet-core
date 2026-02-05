from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.database.base import Base


class Voucher(Base):
    __tablename__ = "vouchers"

    id = Column(Integer, primary_key=True)

    code = Column(String, unique=True, nullable=False, index=True)

    pin = Column(String, nullable=False)

    mikrotik_profile = Column(String, nullable=False)

    duration_days = Column(Integer, nullable=False)

    package_id = Column(
        Integer,
        ForeignKey("internet_packages.id"),
        nullable=False,
    )

    mall_id = Column(
        Integer,
        ForeignKey("malls.id"),
        nullable=False,
    )

    is_used = Column(Boolean, default=False)
    used_at = Column(DateTime, nullable=True)

    expires_at = Column(DateTime, nullable=True)

    created_at = Column(DateTime, server_default=func.now())
