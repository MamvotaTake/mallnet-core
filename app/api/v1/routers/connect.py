from typing import Optional
from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.repositories.internet_package_repository import InternetPackageRepository

router = APIRouter(tags=["Connect"])

templates = Jinja2Templates(directory="app/templates")


@router.get("/connect", response_class=HTMLResponse)
def connect(
    request: Request,
    mall_id: int,
    mac: Optional[str] = None,
    db: Session = Depends(get_db),
):
    repo = InternetPackageRepository(db)
    packages = repo.get_all()

    return templates.TemplateResponse(
        "packages.html",
        {
            "request": request,
            "mall_id": mall_id,
            "mac": mac,
            "packages": packages,
        },
    )
