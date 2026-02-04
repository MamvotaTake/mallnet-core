from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List


from app.database.session import get_db
from app.repositories.internet_package_repository import InternetPackageRepository
from app.schemas.internet_package import InternetPackageResponse

router = APIRouter(prefix="/packages", tags=["Internet Packages"])


@router.get("/", response_model=List[InternetPackageResponse])
def list_packages(db: Session = Depends(get_db)):
    """
    List all available internet packages
    """
    repo = InternetPackageRepository(db)
    return repo.get_all()
