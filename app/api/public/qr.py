from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.repositories.internet_package_repository import InternetPackageRepository
from app.repositories.mall_repository import MallRepository

router = APIRouter(prefix="/public", tags=["Public QR"])


@router.get("/mall/{mall_id}")
def mall_qr_page(mall_id: int, db: Session = Depends(get_db)):
    mall = MallRepository(db).get_by_id(mall_id)
    if not mall:
        raise HTTPException(status_code=404, detail="Mall not found")

    packages = InternetPackageRepository(db).get_all()

    return {
        "mall_id": mall.id,
        "mall_name": mall.name,
        "packages": packages,
    }
