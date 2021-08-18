from typing import List, Optional
from pydantic import BaseModel


class ProjectBase(BaseModel):
    title: str
    description: str
    run_path: str


class ProjectCreate(ProjectBase):
    tags: Optional[str] = None  # separate by ;
    scheduled_at: str


class ProjectRead(ProjectBase):
    project_id: int
    owner_id: int

    class Config:
        orm_mode = True
