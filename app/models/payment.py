from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey
from datetime import datetime
from app.database.base import Base

class Payment(Base):
    __tablename__ = "payments.py"

    id = Column(Integer, primary_key=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id", name="fk_payments_user_id"),
        nullable=False,
    )

    package_id = Column(
        Integer,
        ForeignKey("internet_packages.id", name="fk_payments_package_id"),
        nullable=False,
    )

    amount = Column(Float, nullable=False)

    method = Column(String, nullable=False)
    # cash | ecocash | onemoney | card | paypal | stripe

    reference = Column(String, nullable=True)
    # receipt no / transaction id

    status = Column(String, default="pending")
    # pending | paid | failed

    paid_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
