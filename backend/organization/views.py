from typing import List
from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.orm import Session
from backend.database.core import get_db
from backend.database import models

# from organization import models

# from schemas import user as user_schema


router = APIRouter()


@router.get("/")
def read_orgs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    orgs = db.query(models.Organization).offset(skip).limit(limit).all()
    return orgs
