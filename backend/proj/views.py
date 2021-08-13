from typing import List
import subprocess
from pathlib import Path
import os

from fastapi import APIRouter, Depends, Request, HTTPException, Body
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from backend.database.core import get_db
from backend.database import models
from backend.schemas import project as project_schema
from .service import run_team_project
from .service import create_user_project

templates = Jinja2Templates(directory="templates")

router = APIRouter()

logs_path = Path(__file__).parent.resolve() / "logs"


@router.get("/")
def project_info(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    proj = db.query(models.Project).offset(skip).limit(limit).all()
    return proj


@router.post("/{user_id}/projects/", response_model=project_schema.Project)
def create_project_for_user(
    user_id: int, project: project_schema.ProjectCreate, db: Session = Depends(get_db)
):
    return create_user_project(db=db, project=project, user_id=user_id)


@router.post("/team-projects/")
def serve_my_app(payload=Body(...)):
    project_file_name = payload["project_file_name"]
    project = run_team_project.delay(project_file_name)
    return {"task_id": project.id}


#

# test dynamically view file
# @router.get("/{rest_of_path:path}")
# async def serve_my_app(request: Request, rest_of_path: str):
#     print("rest_of_path: "+rest_of_path)
#     return templates.TemplateResponse("project.html", {"request": request})

# test cmd SQL worked
ip_whitelist = ["192.168.1.1", "127.0.0.1", "8.21.11.25", "2a09:bac0:23::815:b19"]
query_success = "Use oa_platform; select id, next_run_time from apscheduler_jobs WHERE id = 'test1.py';"
query_pending = "Use oa_platform; select id, next_run_time from apscheduler_jobs WHERE id = 'test1.py';"
query_failed = "Use oa_platform; select id, next_run_time from apscheduler_jobs WHERE id = 'test1.py';"


def valid_ip(request):
    # client = request.remote_addr  Flask
    client = request.client.host
    print(client)
    if client in ip_whitelist:
        return True
    else:
        return False


@router.get("/subprocess-log/")
def subprocess_log(request: Request):
    if valid_ip(request):
        print("zz")
        command_success = f'mysql -uroot -p12345678 -e "{query_success}"'
        command_pending = f'mysql -uroot -p12345678 -e "{query_pending}"'
        command_failed = f'mysql -uroot -p12345678 -e "{query_failed}"'
        print(command_success)
        try:
            result_success = subprocess.run(
                [command_success], shell=True, stdout=subprocess.PIPE, text=True
            )
            # print(result_success.stdout)
            with open(logs_path / "output.txt", "w") as f:
                result_pending = subprocess.run([command_pending], stdout=f, shell=True)
            # result_failed = subprocess.check_output([command_failed], shell=True)
        except:
            return "An error occurred while trying to fetch task status updates."

        return "It works zzzzz"
    else:
        return (
            """<title>404 Not Found</title>
               <h1>Not Found</h1>
               <p>The requested URL was not found on the server.
               If you entered the URL manually please check your
               spelling and try again.</p>""",
            404,
        )
