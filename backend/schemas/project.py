from typing import List, Optional
from pydantic import BaseModel

class ProjectBase(BaseModel):
    title: str
    description: Optional[str] = None



class ProjectCreate(ProjectBase):
    tags: Optional[str] = None
    scheduled_at: str


class Project(ProjectBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True
