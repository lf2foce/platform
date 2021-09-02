import time
from datetime import datetime, timedelta
import os
import logging
from backend.proj.celery import app
from pathlib import Path
import subprocess
from sqlalchemy.orm import Session
from backend.database.models import Job
from backend.schemas.job import JobCreate
from ..config import PROJECTS_PATH
from celery.utils.log import get_logger

logger = get_logger(__name__)

celery_logger = logging.getLogger(__name__)


python_executable = "python3"


def get_jobs(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Job).offset(skip).limit(limit).all()


# đang làm
def get_scheduled_jobs(db: Session):
    return db.query(Job).all()


def create_user_job(db: Session, job: JobCreate, user_id: int):
    job_code = job.run_path.split(".")[0].replace("/", ".")
    db_job = Job(**job.dict(), author_id=user_id, job_code=job_code)
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    return db_job


@app.task(name="job_subprocess_schedule")
def run_job_scheduler(file_path, project_schedule_id, executor=None):  # , job_params
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
        result = run_job_scheduler.delay(project_file_path, project_schedule_id)
    except run_job_scheduler.OperationalError as exc:
        celery_logger.exception("Sending task raised: %r", exc)
    # logger.info(result)
    return "hello, %s" % project_schedule_id  # k print ra
