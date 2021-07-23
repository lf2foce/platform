from sqlalchemy.orm import Session

from database import models
import schemas.project as project_schema



def get_projects(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Project).offset(skip).limit(limit).all()


def create_user_project(db: Session, project: project_schema.ProjectCreate, user_id: int):
    db_project = models.Project(**project.dict(), owner_id=user_id)
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project