from typing import List
import subprocess
from pathlib import Path
import os

from fastapi import APIRouter, Depends
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from backend.database.core import get_db
from backend.database.models import File
from backend.schemas.file import FileRead, FileCreate
from .service import run_file_scheduler, create_user_file

templates = Jinja2Templates(directory="templates")

router = APIRouter()


@router.get("/")
def file_info(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    file = db.query(File).offset(skip).limit(limit).all()
    return file


@router.post("/{user_id}/files/", response_model=FileRead)
def create_file_for_user(
    user_id: int,
    file: FileCreate,
    db: Session = Depends(get_db),
):
    file = create_user_file(db=db, file=file, user_id=user_id)
    return file
