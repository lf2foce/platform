from typing import List
from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.orm import Session
from database.core import get_db
from database import models
from schemas import project as project_schema
from proj import service

router = APIRouter()

# @router.get("/project-info")
# def project_info(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     celery_project = db.query(models.CeleryT).offset(skip).limit(limit).all()
#     return celery_project


@router.get("/")
def read_orgs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    proj = db.query(models.Project).offset(skip).limit(limit).all()
    return proj


@router.post("/{user_id}/projects/", response_model=project_schema.Project)
def create_project_for_user(
    user_id: int, project: project_schema.ProjectCreate, db: Session = Depends(get_db)
):
    return service.create_user_project(db=db, project=project, user_id=user_id)
