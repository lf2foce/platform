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
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from celery.result import AsyncResult

from .scheduler.views import router as schedule_router
from .auth.views import user_router
from .report.views import router as report_router
from .organization.views import router as org_router
from .proj.views import router as project_router
from .team_projects.example.bigquery_example.views import router as bq_router
from .team_projects.example.celery_example.views import router as celery_router
from .team_projects.example.file_example.views import router as file_router
from .notification.views import router as slack_router

from .database.core import SessionLocal, engine, Base
from .database.core import get_db
from .database.models import Project

from .proj.celery import app as celery_app
from .proj.tasks import create_task
from .notification.service import send_slack_message

Base.metadata.create_all(bind=engine)  # fastapi docs, init create DB

app = FastAPI()

app.mount("/backend/static", StaticFiles(directory="backend/static"), name="static")
templates = Jinja2Templates(directory="backend/templates")

origins = [
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app.include_router(schedule_router, prefix="/schedule", tags=["schedule"])
app.include_router(user_router, prefix="/api/users", tags=["users"])
app.include_router(project_router, prefix="/api/projects", tags=["projects"])

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
    projects = db.query(Project).all()  # old

    metadata = MetaData()
    with engine.connect() as connection:
        projects_df = pd.read_sql_table("projects", con=connection)
        job_scheduled_df = pd.read_sql_table("apscheduler_jobs", con=connection)
        job_scheduled_df = job_scheduled_df[["id", "next_run_time"]]
        job_scheduled_df["scheduler_group_code"] = job_scheduled_df["id"].apply(
            lambda x: x.split("_")[0]
        )
        job_scheduled_df = job_scheduled_df.groupby("scheduler_group_code").agg(
            {
                "id": lambda x: list(x),
                "next_run_time": lambda x: list(x),
            },
        )
        projects_df = pd.merge(
            projects_df,
            job_scheduled_df,
            left_on="project_code",
            right_on="scheduler_group_code",  # have many scheduler_id
            how="left",
        )

        projects_df.loc[projects_df["id"].isnull(), ["id"]] = projects_df.loc[
            projects_df["id"].isnull(), "id"
        ].apply(lambda x: [])

        # print(projects_df)
        # print(job_scheduled_df)

        # projects = projects_df['project_id', 'title', 'run_path', 'project_code', 'id', 'next_run_time'].to_dict(orient=records)
        projects = projects_df.to_dict(orient="records")
        print(projects)
    return templates.TemplateResponse(
        "projects.html",
        {"request": request, "projects": projects},
    )


# @app.post("/projects/scheduled", tags=["projects"])
# def projects(project_code: str, db: Session = Depends(get_db)):
#     # scheduled job, slow code
#     metadata = MetaData()
#     with engine.connect() as connection:
#         # metadata.reflect(connection)
#         apscheduler_jobs_table = Table(
#             "apscheduler_jobs", metadata, autoload_with=connection
#         )
#         result = connection.execute(apscheduler_jobs_table.select())
#         print(result.fetchall())
#         projects_df = pd.read_sql_table("projects", con=connection)
#         job_scheduled_df = pd.read_sql_table("apscheduler_jobs", con=connection)
#         job_scheduled_df = job_scheduled_df[["id", "next_run_time"]]
#         job_scheduled_df["scheduler_group_code"] = job_scheduled_df["id"].apply(
#             lambda x: x.split("_")[0]
#         )
#         projects_df = pd.merge(
#             projects_df,
#             job_scheduled_df,
#             left_on="project_code",
#             right_on="scheduler_group_code",  # have many scheduler_id
#             how="left",
#         )
#         print(projects_df)
#         print(job_scheduled_df)
#         return projects_df
#     #


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
