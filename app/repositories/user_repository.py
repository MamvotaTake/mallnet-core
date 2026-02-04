from sqlalchemy.orm import Session
from app.repositories.base import BaseRepository
from app.models.user import User


class UserRepository(BaseRepository):
    def __init__(self, db: Session):
        super().__init__(db)

    def get_by_id(self, user_id: int):
        return self.db.query(User).filter(User.id == user_id).first()

    def get_or_create(self, mall_id: int, mac_address: str):
        user = (
            self.db.query(User)
            .filter(
                User.mall_id == mall_id,
                User.mac_address == mac_address,
            )
            .first()
        )
        if user:
            return user

        user = User(
            mall_id=mall_id,
            mac_address=mac_address,
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user
