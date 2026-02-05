from typing import List, Optional, Type

from sqlalchemy.orm import Session
from app.models.router import Router


class RouterRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(
            self,
            mall_id: int,
            name: str,
            host: str,
            username: str,
            password: str,
            api_port: int = 8728,
    ):
        router = Router(
            mall_id=mall_id,
            name=name,
            host=host,
            username=username,
            password=password,
            api_port=api_port,
        )
        self.db.add(router)
        self.db.commit()
        self.db.refresh(router)
        return router

    def get_by_mall(self, mall_id: int) -> Optional[Router]:
        return (
            self.db.query(Router)
            .filter(Router.mall_id == mall_id)
            .first()
        )

    def get_by_id(self, router_id: int) -> Optional[Router]:
        return (
            self.db.query(Router)
            .filter(Router.id == router_id)
            .first()
        )

    def get_all(self) -> List[Type[Router]]:
        return self.db.query(Router).all()
