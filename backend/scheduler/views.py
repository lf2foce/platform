import logging

# from pytz import utc
from pytz import timezone
from datetime import datetime, timedelta
from pathlib import Path
from fastapi import APIRouter, Depends, Request, HTTPException, Body
from sqlalchemy.orm import Session

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.triggers.cron import CronTrigger

# from apscheduler.jobstores.redis import RedisJobStore
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from apscheduler.events import EVENT_JOB_ERROR
from cron_descriptor import get_description, ExpressionDescriptor, CasingTypeEnum


from backend.database.core import get_db
from backend.schemas import scheduler as ss  # schedule schema
from backend.schemas.scheduler import IntervalScheduleCreate, CronJobCreate
from backend.proj.service import aps_celery1
from ..config import SQLALCHEMY_DATABASE_URI, TIMEZONE
from .service import create_cron_schedule_for_job
from .service import create_schedule_for_project


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
            "default": SQLAlchemyJobStore(url=SQLALCHEMY_DATABASE_URI),
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
            # timezone=vietnam,
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


@router.post("/cron_check/")
def cron_check(payload=Body(...)):
    cron_string = payload["cron_string"]
    print(cron_string)

    try:
        # desc = get_description(cron_string)
        descripter = ExpressionDescriptor(
            expression=cron_string,
            throw_exception_on_parse_error=True,
            casing_type=CasingTypeEnum.Sentence,
            use_24hour_time_format=True,
        )
        print(descripter)
        return {"status": "success", "desc": descripter.get_description()}
    except:
        return {"status": "fail", "desc": "sai định dạng"}


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
    just_add = Schedule.add_job(
        test_job,
        "cron",
        day_of_week="mon-fri",
        hour=hour,
        minute=minute,
        # start_date="2021-06-30",
        end_date="2021-12-31",
        args=[name],
    )
    return {"scheduled": True, "job_id": just_add.id}


@router.post(
    "/add_cronjob/", response_model=ss.JobCreateDeleteResponse, tags=["schedule"]
)
async def add_cronjob(cron_schedule: CronJobCreate, db: Session = Depends(get_db)):
    scheduled_job = create_cron_schedule_for_job(
        db=db,
        file_id=cron_schedule.file_id,
        desc=cron_schedule.desc,
        cron_string=cron_schedule.cron_string,
        Schedule=Schedule,
    )
    return scheduled_job


@router.post(
    "/add_project/",
    response_model=ss.JobCreateDeleteResponse,
    tags=["schedule"],
)
def add_project_interval(
    # project_id: int,
    # desc: str,
    # time_in_seconds: int = 60,
    interval_schedule: IntervalScheduleCreate,
    db: Session = Depends(get_db),
):
    scheduled_project = create_schedule_for_project(
        db=db,
        project_id=interval_schedule.project_id,
        desc=interval_schedule.desc,
        time_in_seconds=interval_schedule.time_in_seconds,
        Schedule=Schedule,
    )
    return scheduled_project


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
