import time
from datetime import datetime, timedelta
import os
import logging
from .celery import app
from pathlib import Path
import subprocess
from sqlalchemy.orm import Session
from backend.database import models
import backend.schemas.project as project_schema
from ..config import PROJECTS_PATH
from celery.utils.log import get_logger

logger = get_logger(__name__)  # celery logger

celery_logger = logging.getLogger(__name__)


LOGS_PATH = Path(__file__).parent.resolve() / "logs"

python_executable = "python3"


def get_projects(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Project).offset(skip).limit(limit).all()


# đang làm
def get_scheduled_projects(db: Session):
    return db.query(models.Project).all()


def create_user_project(
    db: Session, project: project_schema.ProjectCreate, user_id: int
):
    project_code = project.run_path.split(".")[0].replace("/", ".")
    db_project = models.Project(
        **project.dict(), owner_id=user_id, project_code=project_code
    )
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project


@app.task(name="python_subprocess_schedule")
def run_team_project_scheduler(file_path, project_schedule_id, executor=None):
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


def aps_celery1(project_file_path, project_schedule_id):
    # print(f"#####aps_cel called. {project_schedule_id}")
    logger.info(f"###!!!!!!!!!!!!! Tick! call by apscheduler job {project_schedule_id}")
    try:
        result = run_team_project_scheduler.delay(
            project_file_path, project_schedule_id
        )
    except run_team_project_scheduler.OperationalError as exc:
        celery_logger.exception("Sending task raised: %r", exc)
    # logger.info(result)
    return "hello, %s" % project_schedule_id  # k print ra


# without schedule - logs to file
@app.task(name="python_subprocess")
def run_team_project(file_path, executor=None):
    file_name = file_path.split(".")[0].replace("/", ".")
    file_path = PROJECTS_PATH / file_path
    print("file path: ", str(file_path))
    if file_path.exists():
        Path(LOGS_PATH / file_name).mkdir(parents=True, exist_ok=True)
        with open(
            LOGS_PATH / f"{file_name}/{datetime.now()}.log",
            "w",
        ) as f:
            result_success = subprocess.run(
                [f"python3 {str(file_path)}"],
                stdout=f,
                shell=True,
                text=True,  # , encoding="utf-8"
            )
        logger.info(result_success.stdout)
        return {
            "status": True,
            "result": "in log file",
        }
        # return "executed"
    return {"status": False, "result": "something wrong"}


# def aps_celery(project_file_name: str):
#     result = run_team_project.delay(project_file_name)
#     return result.id
