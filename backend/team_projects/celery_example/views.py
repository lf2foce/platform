from team_projects.celery_example.service import create_task2

from fastapi import APIRouter

router = APIRouter()


@router.get("/celery")
def read_root():
    task = create_task2.delay()
    return {"Hello": "World", "task_id": task.id}