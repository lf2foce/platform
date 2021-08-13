import time
import os
import logging
from .celery import app
from pathlib import Path
import subprocess
from sqlalchemy.orm import Session
from backend.database import models
import backend.schemas.project as project_schema

logger = logging.getLogger(__name__)


def get_projects(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Project).offset(skip).limit(limit).all()


def create_user_project(
    db: Session, project: project_schema.ProjectCreate, user_id: int
):
    db_project = models.Project(**project.dict(), owner_id=user_id)
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project


BASE_PATH = Path(__file__).parents[1]
projects_path = BASE_PATH / "team_projects"
python_executable = "python3"


@app.task(name="python_subprocess")
def run_team_project(file_path, executor=None):
    file_path = projects_path / file_path
    print("file name: ", str(file_path))
    if file_path.exists():
        result_success = subprocess.run(
            [f"python3 {str(file_path)}"],
            shell=True,
            stdout=subprocess.PIPE,
            text=True,
        )
        return result_success.stdout
        # return "executed"
    return "not exists"


def aps_celery1(project_file_name):
    print(f"#####aps_cel called. {project_file_name}")
    logger.info(f"###!!!!!!!!!!!!! Tick! call by apscheduler job {project_file_name}")
    result = run_team_project.delay(project_file_name)
    logger.info(result)
    return "hello, %s" % project_file_name


# def aps_celery(project_file_name: str):
#     result = run_team_project.delay(project_file_name)
#     return result.id
