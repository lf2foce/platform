from typing import List, Optional
from pydantic import BaseModel, Json, ValidationError
from .scheduler import CronJobRead


class FileBase(BaseModel):
    name: str
    description: str
    run_path: str
    is_params_required: bool = False
    is_active: bool = True


class FileCreate(FileBase):
    tags: Optional[str] = None  # separate by ;


class FileUpdate(FileBase):
    file_params: Optional[dict] = {"params": "value"}


class FileRead(FileBase):
    id: int
    author_id: int
    scheduled_jobs: List[CronJobRead] = []

    class Config:
        orm_mode = True
