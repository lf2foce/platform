from backend.database.models import APSchedulerJobsTable, Project
from backend.proj.service import aps_celery1
from ..config import BASE_PATH, PROJECTS_PATH


def create_schedule_for_project(db, project_id, desc, time_in_seconds, Schedule):
    current_project = db.query(Project).filter(Project.project_id == project_id).first()
    rel_file_path = current_project.run_path
    db.commit()
    # commit before open new connection
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
            )
            # time.sleep(1)
            schedule = (
                db.query(APSchedulerJobsTable)
                .filter(APSchedulerJobsTable.id == project_schedule_id)
                .first()
            )

            schedule.project_id = project_id
            db.add(schedule)
            db.commit()

            return {"scheduled": True, "job_id": my_job.id, "status": "success"}
        return {
            "scheduled": False,
            "job_id": None,
            "status": "file path does not exist",
        }
    return {"scheduled": False, "job_id": None, "status": "job-schedule id is existed"}
