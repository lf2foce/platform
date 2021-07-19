from typing import List

from fastapi import Depends, FastAPI, HTTPException, Request, Body
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from auth.views import user_router
from report.views import router as report_router
from team_projects.bigquery_example.views import router as bq_router
from team_projects.celery_example.views import router as celery_router
from  notification.webhook_slack import router as slack_router

from database.core import SessionLocal, engine, Base

from proj.celery import app as celery_app
from proj.tasks import create_task
from celery.result import AsyncResult


Base.metadata.create_all(bind=engine) #fastapi docs, init create DB

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

app.include_router(user_router, prefix="/api/users", tags=["users"])
app.include_router(bq_router, tags=["bigquery"])
app.include_router(report_router, tags=["chart"])
app.include_router(celery_router)
app.include_router(slack_router)



@app.get("/", response_class=HTMLResponse)
def dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})

@app.get("/users", response_class=HTMLResponse)
def users(request: Request):
    return templates.TemplateResponse("users.html", {"request": request})


@app.post("/tasks", status_code=201)
def run_task(payload = Body(...)):
    task_type = payload["type"]
    task = create_task.delay(task_type)
    return {"task_id": task.id}


@app.get("/tasks/{task_id}")
def get_status(task_id):
    task_result = AsyncResult(task_id, app=celery_app)
    result = {
        "task_id": task_id,
        "task_status": task_result.status,
        "task_result": task_result.result
    }
    return result
