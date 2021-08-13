import logging
from typing import List
from pytz import utc
from datetime import datetime, timedelta

# import uvicorn

from fastapi import Depends, FastAPI, HTTPException, Request, Body
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.responses import FileResponse

# from fastapi.logger import logger
from fastapi.middleware.cors import CORSMiddleware

from .auth.views import user_router
from .report.views import router as report_router
from .organization.views import router as org_router
from .proj.views import router as project_router
from .team_projects.example.bigquery_example.views import router as bq_router
from .team_projects.example.celery_example.views import router as celery_router
from .team_projects.example.file_example.views import router as file_router
from .notification.views import router as slack_router

from .database.core import SessionLocal, engine, Base

from .proj.celery import app as celery_app
from .proj.tasks import create_task
from .notification.service import send_slack_message
from .schemas import schedule as ss
from .config import SQLALCHEMY_DATABASE_URL

from celery.result import AsyncResult

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore

# from apscheduler.jobstores.redis import RedisJobStore
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor


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

# config schedule


@app.on_event("startup")
async def load_schedule_or_create_blank():
    """
    Instatialise the Schedule Object as a Global Param and also load existing Schedules from SQLite
    This allows for persistent schedules across server restarts.
    """
    global Schedule
    try:
        jobstores = {
            "default": SQLAlchemyJobStore(url=SQLALCHEMY_DATABASE_URL),
            # "default": RedisJobStore(host="localhost", port=6379)
        }
        executors = {
            "default": ThreadPoolExecutor(20),  # maximum thread count of 20
            "processpool": ProcessPoolExecutor(5),  # multiple CPU cores
        }
        job_defaults = {
            "coalesce": False,  # default
            "max_instances": 10,  # Maximum instances of job running
        }
        Schedule = AsyncIOScheduler(
            jobstores=jobstores,
            executors=executors,
            job_defaults=job_defaults,
            timezone=utc,
        )
        # Schedule = AsyncIOScheduler(jobstores=jobstores)
        Schedule.start()
        logger.info("Created Schedule Object")
    except:
        logger.error("Unable to Create Schedule Object")


@app.on_event("shutdown")
async def pickle_schedule():
    """
    An Attempt at Shutting down the schedule to avoid orphan jobs
    """
    global Schedule
    Schedule.shutdown()
    logger.info("Disabled Schedule")


########


##

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


from .database.models import Project
from sqlalchemy.orm import Session
from .database.core import get_db


@app.get("/projects", response_class=HTMLResponse)
def projects(request: Request, db: Session = Depends(get_db)):
    projects = db.query(Project).all()

    return templates.TemplateResponse(
        "projects.html",
        {"request": request, "projects": projects},
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


# Add job schedule on the fly
@app.get(
    "/schedule/show_schedules/",
    response_model=ss.CurrentScheduledJobsResponse,
    tags=["schedule"],
)
async def get_scheduled_syncs():
    """
    Will provide a list of currently Scheduled Tasks
    """
    schedules = []
    for job in Schedule.get_jobs():
        schedules.append(
            {
                "job_id": str(job.id),
                "run_frequency": str(job.trigger),
                "next_run": str(job.next_run_time),
            }
        )
    return {"jobs": schedules}


def test_job(name):
    logger.info(f"###!!!!!!!!!!!!! Tick! call by apscheduler job {name}")
    return "hello, %s" % name


@app.post(
    "/schedule/add_job/", response_model=ss.JobCreateDeleteResponse, tags=["schedule"]
)
async def add_daily_job(name):
    exec_time = datetime.now() + timedelta(minutes=1)
    hour = exec_time.strftime("%H")
    minute = exec_time.strftime("%M")
    # here to choose 'cron'
    # In addition, job_id can be set according to your own situation, it will be used for remove_job
    just_add = Schedule.add_job(test_job, "cron", hour=hour, minute=minute, args=[name])
    return {"scheduled": True, "job_id": just_add.id}


@app.post(
    "/schedule/add_job2/", response_model=ss.JobCreateDeleteResponse, tags=["schedule"]
)
async def add_interval_job(name, time_in_seconds: int = 60):
    """
    Add a New Job to a Schedule
    """
    my_job = Schedule.add_job(
        test_job, "interval", seconds=time_in_seconds, id=name, args=[name]
    )
    return {"scheduled": True, "job_id": my_job.id}


from backend.proj.service import run_team_project, aps_celery1


@app.post(
    "/schedule/add_project/",
    response_model=ss.JobCreateDeleteResponse,
    tags=["schedule"],
)
async def add_project(file_path, time_in_seconds: int = 60):
    my_job = Schedule.add_job(
        aps_celery1, "interval", seconds=time_in_seconds, id=file_path, args=[file_path]
    )
    return {"scheduled": True, "job_id": my_job.id}


@app.delete(
    "/schedule/remove_job/",
    response_model=ss.JobCreateDeleteResponse,
    tags=["schedule"],
)
async def remove_job(name):
    """
    Remove a Job from a Schedule
    """
    Schedule.remove_job(name)
    return {"scheduled": False, "job_id": name}


# logo
@app.get("/logo", response_class=FileResponse)
async def logo():
    return "storage/assets/image/task.jpg"


# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=80)
