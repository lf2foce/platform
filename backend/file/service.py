import time
from datetime import datetime, timedelta
import os
import logging
from backend.proj.celery import app
from pathlib import Path
import subprocess
from sqlalchemy.orm import Session
from backend.database.models import File
from backend.schemas.file import FileCreate
from ..config import PROJECTS_PATH
from celery.utils.log import get_logger

logger = get_logger(__name__)

celery_logger = logging.getLogger(__name__)


python_executable = "python3"


def get_files(db: Session, skip: int = 0, limit: int = 100):
    return db.query(File).offset(skip).limit(limit).all()


# đang làm
def get_scheduled_files(db: Session):
    return db.query(File).all()


def create_user_file(db: Session, file: FileCreate, user_id: int):
    file_code = file.run_path.split(".")[0].replace("/", ".")
    db_file = File(**file.dict(), author_id=user_id, file_code=file_code)
    db.add(db_file)
    db.commit()
    db.refresh(db_file)
    return db_file


@app.task(name="file_subprocess_schedule")
def run_file_scheduler(file_path, project_schedule_id, executor=None):  # , file_params
    file_path = PROJECTS_PATH / file_path
    if file_path.exists():
        result_success = subprocess.run(
            [f"python3 {str(file_path)}"],
            shell=True,
            stdout=subprocess.PIPE,
            text=True,
        )
        # logger.info(result_success.stdout)

        return {
            "status": True,
            "result": result_success.stdout,
            "project_schedule_id": project_schedule_id,
        }
        # return "executed"
    return {"status": False, "result": "file_path changed"}


def aps_celery2(project_file_path, project_schedule_id):
    # print(f"#####aps_cel called. {project_schedule_id}")
    logger.info(f"###!!!!!!!!!!!!! Tick! call by apscheduler job {project_schedule_id}")
    try:
        result = run_file_scheduler.delay(project_file_path, project_schedule_id)
    except run_file_scheduler.OperationalError as exc:
        celery_logger.exception("Sending task raised: %r", exc)
    # logger.info(result)
    return "hello, %s" % project_schedule_id  # k print ra
