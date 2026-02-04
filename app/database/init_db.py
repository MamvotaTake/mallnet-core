from app.database.session import engine
from app.database.base import Base

from app.models.mall import Mall
from app.models.router import Router
from app.models.internet_package import InternetPackage
from app.models.user import User
from app.models.subscription import Subscription
from app.models.payment import Payment

def init_db():
    Base.metadata.create_all(bind=engine)
