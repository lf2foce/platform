from typing import List
import subprocess
from pathlib import Path
import os

from fastapi import APIRouter, Depends
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from backend.database.core import get_db
from backend.database.models import Job
from backend.schemas.job import JobRead, JobCreate
from .service import run_job_scheduler, create_user_job

templates = Jinja2Templates(directory="templates")

router = APIRouter()


@router.get("/")
def job_info(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    job = db.query(Job).offset(skip).limit(limit).all()
    return job


@router.post("/{user_id}/jobs/", response_model=JobRead)
def create_job_for_user(
    user_id: int,
    job: JobCreate,
    db: Session = Depends(get_db),
):
    job = create_user_job(db=db, job=job, user_id=user_id)
    return job
