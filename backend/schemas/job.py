from typing import List, Optional
from pydantic import BaseModel, Json, ValidationError


class JobBase(BaseModel):
    name: str
    description: str
    run_path: str
    job_params: dict
    enabled: bool = True


class JobCreate(JobBase):
    tags: Optional[str] = None  # separate by ;


class JobRead(JobBase):
    id: int
    author_id: int

    class Config:
        orm_mode = True
