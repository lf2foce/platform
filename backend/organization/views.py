from typing import List
from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.orm import Session
from backend.database.core import get_db
from backend.database import models
from .service import create

# from organization import models

# from schemas import user as user_schema


router = APIRouter()


@router.get("/")
def read_orgs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    orgs = db.query(models.Organization).offset(skip).limit(limit).all()
    return orgs


from backend.schemas.organization import OrganizationRead, OrganizationCreate


@router.post(
    "",
    response_model=OrganizationRead,
)
def create_organization(
    *,
    db: Session = Depends(get_db),
    organization_in: OrganizationCreate,
):
    """Create a new organization."""
    organization = create(db=db, organization_in=organization_in)
    return organization
