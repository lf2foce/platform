import logging

# from pytz import utc
from pytz import timezone
from datetime import datetime, timedelta
from pathlib import Path
from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.orm import Session

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore

# from apscheduler.jobstores.redis import RedisJobStore
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from apscheduler.events import EVENT_JOB_ERROR

from backend.database.core import get_db
from backend.schemas import scheduler as ss  # schedule schema
from backend.proj.service import aps_celery1
from ..config import SQLALCHEMY_DATABASE_URL, TIMEZONE


router = APIRouter()
# Add job schedule on the fly
logger = logging.getLogger(__name__)

BASE_PATH = Path(__file__).parents[1]

vietnam = timezone(TIMEZONE)


def report_error(event):
    if event.exception:
        print(event.exception)


@router.on_event("startup")
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
            "processpool": ProcessPoolExecutor(4),  # multiple CPU cores
        }
        job_defaults = {
            "coalesce": False,  # default
            "max_instances": 20,  # Maximum instances of job running
        }
        Schedule = AsyncIOScheduler(
            jobstores=jobstores,
            executors=executors,
            job_defaults=job_defaults,
            timezone=vietnam,
        )
        # Schedule = AsyncIOScheduler(jobstores=jobstores)
        Schedule.start()
        Schedule.add_listener(report_error, EVENT_JOB_ERROR)
        logger.info("Created Schedule Object")
    except:
        logger.error("Unable to Create Schedule Object")


def get_scheduler():
    return Schedule


@router.on_event("shutdown")
async def pickle_schedule():
    """
    An Attempt at Shutting down the schedule to avoid orphan jobs
    """
    global Schedule
    Schedule.shutdown()
    logger.info("Disabled Schedule")


@router.get(
    "/show_schedules/",
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
    return f"hello, {name}"


@router.post("/add_job/", response_model=ss.JobCreateDeleteResponse, tags=["schedule"])
async def add_daily_job(name):
    exec_time = datetime.now() + timedelta(minutes=1)
    hour = exec_time.strftime("%H")
    minute = exec_time.strftime("%M")
    # here to choose 'cron'
    # In addition, job_id can be set according to your own situation, it will be used for remove_job
    just_add = Schedule.add_job(test_job, "cron", hour=hour, minute=minute, args=[name])
    return {"scheduled": True, "job_id": just_add.id}


@router.post("/add_job2/", response_model=ss.JobCreateDeleteResponse, tags=["schedule"])
async def add_interval_job(name, time_in_seconds: int = 60):
    """
    Add a New Job to a Schedule
    """
    my_job = Schedule.add_job(
        test_job, "interval", seconds=time_in_seconds, id=name, args=[name]
    )
    return {"scheduled": True, "job_id": my_job.id}


@router.post(
    "/add_project/",
    response_model=ss.JobCreateDeleteResponse,
    tags=["schedule"],
)
def add_project(rel_file_path: str, desc: str, time_in_seconds: int = 60):
    projects_path = BASE_PATH / "team_projects"
    full_path = projects_path / rel_file_path
    project_schedule_id = (
        rel_file_path.split(".")[0].replace("/", ".") + "_" + str(desc)
    )

    job_ids = [str(job.id) for job in Schedule.get_jobs()]

    if project_schedule_id not in job_ids:
        if full_path.exists():
            my_job = Schedule.add_job(
                aps_celery1,
                "interval",
                seconds=time_in_seconds,
                id=project_schedule_id,
                args=(rel_file_path, project_schedule_id),
            )
            return {"scheduled": True, "job_id": my_job.id, "status": "success"}
        return {
            "scheduled": False,
            "job_id": None,
            "status": "file path does not exist",
        }
    return {"scheduled": False, "job_id": None, "status": "job-schedule id is existed"}


@router.delete(
    "/remove_job/",
    response_model=ss.JobCreateDeleteResponse,
    tags=["schedule"],
)
async def remove_job(name):
    """
    Remove a Job from a Schedule
    """
    Schedule.remove_job(name)
    return {"scheduled": False, "job_id": name}
