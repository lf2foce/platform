from typing import List, Optional
from pydantic import BaseModel, Field

# https://github.com/cryptoroo/fastapi-scheduled-ssl-checks/blob/master/main.py
class CurrentScheduledJob(BaseModel):
    job_id: str = Field(
        title="The Job ID in APScheduler", description="The Job ID in APScheduler"
    )
    run_frequency: str = Field(
        title="The Job Interval in APScheduler",
        description="The Job Interval in APScheduler",
    )
    next_run: str = Field(
        title="Next Scheduled Run for the Job",
        description="Next Scheduled Run for the Job",
    )

    class Config:
        schema_extra = {
            "example": {
                "job_id": "www.google.com",
                "run_frequency": "interval[0:05:00]",
                "next_run": "2020-11-10 22:12:09.397935+10:00",
            }
        }


class CurrentScheduledJobsResponse(BaseModel):
    jobs: List[CurrentScheduledJob]


class JobCreateDeleteResponse(BaseModel):
    scheduled: bool = Field(
        title="Whether the job was scheduler or not",
        description="Whether the job was scheduler or not",
    )
    job_id: Optional[str] = Field(
        title="The Job ID in APScheduler", description="The Job ID in APScheduler"
    )
    status: Optional[str] = Field(
        title="The Job status in APScheduler", description="Reason"
    )

    class Config:
        schema_extra = {"example": {"scheduled": True, "job_id": "www.google.com"}}


# from cronjob
class IntervalScheduleCreate(BaseModel):
    project_id: int
    desc: str
    time_in_seconds: int = 60


class CronJobCreate(BaseModel):
    file_id: int
    desc: str
    cron_string: str = "* * * * *"


class CronJobRead(BaseModel):
    id: str
    file_id: int
    next_run_time: str

    class Config:
        orm_mode = True
