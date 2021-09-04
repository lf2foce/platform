from typing import List, Optional
from pydantic import BaseModel, Json


class ProjectBase(BaseModel):
    title: str
    description: str
    run_path: str


class ProjectCreate(ProjectBase):
    tags: Optional[str] = None  # separate by ;
    # job_priority: List[int] = []


class ProjectRead(ProjectBase):
    project_id: int
    owner_id: int

    class Config:
        orm_mode = True
