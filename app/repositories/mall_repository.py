from typing import List, Optional, Type

from sqlalchemy.orm import Session
from app.models.mall import Mall


class MallRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, name: str) -> Mall:
        mall = Mall(name=name)
        self.db.add(mall)
        self.db.commit()
        self.db.refresh(mall)
        return mall

    def get_by_id(self, mall_id: int) -> Optional[Mall]:
        return (
            self.db.query(Mall)
            .filter(Mall.id == mall_id)
            .first()
        )

    def get_all(self) -> List[Type[Mall]]:
        return self.db.query(Mall).all()
