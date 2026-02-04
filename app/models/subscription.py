from sqlalchemy import Column, Integer, ForeignKey, DateTime, Boolean
from datetime import datetime
from app.database.base import Base

class Subscription(Base):
    __tablename__ = "subscriptions"

    id = Column(Integer, primary_key=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id", name="fk_subscriptions_user_id"),
        nullable=False,
    )

    package_id = Column(
        Integer,
        ForeignKey("internet_packages.id", name="fk_subscriptions_package_id"),
        nullable=False,
    )

    start_date = Column(DateTime, default=datetime.utcnow)
    end_date = Column(DateTime, nullable=False)
    is_active = Column(Boolean, default=True)
