import logging
from typing import List
from pytz import utc
from datetime import datetime, timedelta
from pathlib import Path

# import uvicorn
from fastapi import Depends, FastAPI, HTTPException, Request, Body
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from jinja2 import pass_environment, Environment

from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from celery.result import AsyncResult

from backend import config

from .scheduler.views import router as schedule_router
from .auth.views import user_router
from .report.views import router as report_router
from .organization.views import router as org_router
from .proj.views import router as project_router
from .file.views import router as job_router
from .team_projects.example.bigquery_example.views import router as bq_router
from .team_projects.example.celery_example.views import router as celery_router
from .team_projects.example.file_example.views import router as file_router
from .notification.views import router as slack_router

from .database.core import SessionLocal, engine, Base, get_db
from .database.models import Project, User, File
from .database.manage import init_database
from .database.seeds import seed_example

from .proj.celery import app as celery_app
from .proj.tasks import create_task
from .notification.service import send_slack_message

Base.metadata.drop_all(engine)  # TODO phải bỏ ra khi deploy

# Base.metadata.create_all(bind=engine)  # fastapi docs, init create DB
init_database(engine=engine)
seed_example()

app = FastAPI()

# js, css
app.mount("/static", StaticFiles(directory=str(config.STATIC_PATH)), name="static")
# template HTML
templates = Jinja2Templates(directory=str(config.TEMPLATE_PATH))


origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://127.0.0.1:5500",
    "http://127.0.0.1:5500/",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# jinja
def datetime_format(float_date, format="%Y-%m-%d %H:%M:%S"):
    return datetime.fromtimestamp(int(float_date)).strftime(format)


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app.include_router(schedule_router, prefix="/schedule", tags=["schedule"])
app.include_router(user_router, prefix="/api/users", tags=["users"])
app.include_router(project_router, prefix="/api/projects", tags=["projects"])
app.include_router(file_router, prefix="/api/files", tags=["files"])

app.include_router(report_router, prefix="/reports", tags=["reports"])
app.include_router(slack_router, tags=["notification"])
app.include_router(org_router, prefix="/api/orgs")

# example
app.include_router(bq_router, tags=["bigquery", "example"])
app.include_router(celery_router, tags=["example"])
app.include_router(file_router, tags=["example"])


@app.get("/event-api", response_class=HTMLResponse)
def event_api(request: Request):
    return templates.TemplateResponse("event-api.html", {"request": request})


@app.get("/users", response_class=HTMLResponse)
def users(request: Request):
    return templates.TemplateResponse("users.html", {"request": request})


from sqlalchemy import table, column, select, text
from sqlalchemy import MetaData, Table
from backend.database.core import engine
import pandas as pd


@app.get("/projects", response_class=HTMLResponse, tags=["projects"])
def projects(request: Request, db: Session = Depends(get_db)):
    projects = db.query(Project).all()

    templates.env.filters["datetime_format"] = datetime_format

    return templates.TemplateResponse(
        "projects.html",
        {"request": request, "projects": projects},
    )


@app.get("/files", response_class=HTMLResponse, tags=["files"])
def files(request: Request, db: Session = Depends(get_db)):
    files = db.query(File).all()

    templates.env.filters["datetime_format"] = datetime_format

    return templates.TemplateResponse(
        "files.html",
        {"request": request, "files": files},
    )


@app.post("/slackbot")
def run_project(payload=Body(...)):
    project_status = payload["status"]
    project = send_slack_message.delay(message=project_status)
    print(project, project.id)
    return {"task_id": project.id, "task_name": send_slack_message.name}


# dashboard view
@app.get("/", response_class=HTMLResponse)
def dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})


@app.post("/tasks", status_code=201)
def run_task(payload=Body(...)):
    task_type = payload["type"]
    task = create_task.delay(task_type)
    return {"task_id": task.id}


@app.get("/tasks/{task_id}")
def get_status(task_id):
    task_result = AsyncResult(task_id, app=celery_app)
    print(task_result)
    result = {
        "task_id": task_id,
        "task_status": task_result.status,
        "task_result": task_result.result,
    }
    print(result)
    return result


# image
@app.get("/logo", response_class=FileResponse)
async def logo():
    return "backend/storage/assets/image/task.jpg"


@app.get("/favicon.ico", response_class=FileResponse)
async def favicon():
    return "backend/storage/assets/image/ironman.ico"


# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=80)
