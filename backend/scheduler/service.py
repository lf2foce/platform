from apscheduler.triggers.cron import CronTrigger
from sqlalchemy.orm import Session

from backend.database.core import SessionLocal
from backend.database.models import APSchedulerJobsTable, Project, File
from backend.proj.service import aps_celery1
from backend.file.service import aps_celery2
from backend.database.core import SessionLocal
from ..config import BASE_PATH, PROJECTS_PATH, TIMEZONE


def get_project_path(project_id: int):
    db = SessionLocal()
    current_project = db.query(Project).filter(Project.project_id == project_id).first()
    # db.close()  # without this might cause error
    return current_project.run_path


def get_job_from_id(file_id, desc, db):
    rel_file_path = get_file_path(file_id)

    project_schedule_id = (
        rel_file_path.split(".")[0].replace("/", ".") + "_" + str(desc)
    )

    job = (
        db.query(APSchedulerJobsTable)
        .filter(APSchedulerJobsTable.id == project_schedule_id)
        .first()
    )
    return job


def get_file_path(file_id: int):
    db = SessionLocal()
    current_file = db.query(File).filter(File.id == file_id).first()
    # db.close()  # without this might cause error
    return current_file.run_path


def create_schedule_for_project(db, project_id, desc, time_in_seconds, Schedule):

    # rel_file_path = current_project.run_path
    rel_file_path = get_project_path(project_id)
    full_path = PROJECTS_PATH / rel_file_path
    project_schedule_id = (
        rel_file_path.split(".")[0].replace("/", ".") + "_" + str(desc)
    )

    job_ids = [str(job.id) for job in Schedule.get_jobs()]

    if project_schedule_id not in job_ids:
        if full_path.exists():
            my_job = Schedule.add_job(
                aps_celery1,
                "interval",  # cron
                seconds=time_in_seconds,
                id=project_schedule_id,
                args=(rel_file_path, project_schedule_id),
                # replace_existing=True
            )
            # Cách 1
            # schedule = (
            #     db.query(APSchedulerJobsTable)
            #     .filter(APSchedulerJobsTable.id == project_schedule_id)
            #     .first()
            # )
            # schedule.project_id = project_id
            # db.add(schedule)

            # Cách 2
            schedule = (
                db.query(APSchedulerJobsTable)
                .filter(APSchedulerJobsTable.id == project_schedule_id)
                .update({"project_id": project_id})
            )

            db.commit()

            return {"scheduled": True, "job_id": my_job.id, "status": "success"}
        return {
            "scheduled": False,
            "job_id": None,
            "status": "file path does not exist",
        }
    return {"scheduled": False, "job_id": None, "status": "job-schedule id is existed"}


def create_cron_schedule_for_job(db, file_id, desc, cron_string, Schedule):

    rel_file_path = get_file_path(file_id)
    full_path = PROJECTS_PATH / rel_file_path
    project_schedule_id = (
        rel_file_path.split(".")[0].replace("/", ".") + "_" + str(desc)
    )

    file_ids = [str(job.id) for job in Schedule.get_jobs()]

    if project_schedule_id not in file_ids:
        if full_path.exists():
            my_job = Schedule.add_job(
                aps_celery2,
                CronTrigger.from_crontab(cron_string),
                id=project_schedule_id,
                args=(rel_file_path, project_schedule_id),
            )

            schedule = (
                db.query(APSchedulerJobsTable)
                .filter(APSchedulerJobsTable.id == project_schedule_id)
                .update({"file_id": file_id})
            )

            db.commit()

            return {"scheduled": True, "job_id": my_job.id, "status": "success"}
        return {
            "scheduled": False,
            "job_id": None,
            "status": "file path does not exist",
        }
    return {"scheduled": False, "job_id": None, "status": "job-schedule id is existed"}
