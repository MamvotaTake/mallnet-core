from typing import Optional, List
from app.models.internet_package import InternetPackage
from app.repositories.base import BaseRepository


class InternetPackageRepository(BaseRepository):

    def create(
        self,
        name: str,
        price: float,
        validity_days: int,
        mikrotik_profile: str
    ) -> InternetPackage:
        package = InternetPackage(
            name=name,
            price=price,
            validity_days=validity_days,
            mikrotik_profile=mikrotik_profile
        )
        self.db.add(package)
        self.db.commit()
        self.db.refresh(package)
        return package

    def get_by_id(self, package_id: int) -> Optional[InternetPackage]:
        return (
            self.db.query(InternetPackage)
            .filter(InternetPackage.id == package_id)
            .first()
        )

    def get_by_name(self, name: str) -> Optional[InternetPackage]:
        return (
            self.db.query(InternetPackage)
            .filter(InternetPackage.name == name)
            .first()
        )

    def get_all(self) -> List[InternetPackage]:
        return self.db.query(InternetPackage).all()

    def delete(self, package_id: int) -> bool:
        package = self.get_by_id(package_id)
        if not package:
            return False

        self.db.delete(package)
        self.db.commit()
        return True
