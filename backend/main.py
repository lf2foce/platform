from typing import List

from fastapi import Depends, FastAPI, HTTPException, Request, Body
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.responses import FileResponse

from auth.views import user_router
from report.views import router as report_router
from organization.views import router as org_router
from proj.views import router as project_router

from team_projects.example.bigquery_example.views import router as bq_router
from team_projects.example.celery_example.views import router as celery_router
from team_projects.example.file_example.views import router as file_router
from notification.views import router as slack_router

from database.core import SessionLocal, engine, Base

from proj.celery import app as celery_app
from proj.tasks import create_task
from notification.service import send_slack_message
from celery.result import AsyncResult


Base.metadata.create_all(bind=engine) #fastapi docs, init create DB

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

app.include_router(user_router, prefix="/api/users", tags=["users"])
app.include_router(project_router, prefix="/api/projects", tags=["projects"])
app.include_router(report_router, tags=["chart"])
app.include_router(slack_router, tags=["notification"])
app.include_router(org_router, prefix="/api/orgs")

# example
app.include_router(bq_router, tags=["bigquery", "example"])
app.include_router(celery_router, tags=["example"])
app.include_router(file_router, tags=["example"])




@app.get("/event-api", response_class=HTMLResponse)
def event_api(request: Request):
    return templates.TemplateResponse("event-api.html", {"request": request})

@app.get("/users", response_class=HTMLResponse)
def users(request: Request):
    return templates.TemplateResponse("users.html", {"request": request})

@app.get("/projects", response_class=HTMLResponse)
def dashboard(request: Request):
    return templates.TemplateResponse("projects.html", {"request": request})

@app.post("/slackbot")
def run_project(payload = Body(...)):
    project_status = payload["status"]
    project = send_slack_message.delay(message=project_status)
    print(project, project.id)
    return {"task_id": project.id, "task_name": send_slack_message.name}


# dashboard view
@app.get("/", response_class=HTMLResponse)
def dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})

@app.post("/tasks", status_code=201)
def run_task(payload = Body(...)):
    task_type = payload["type"]
    task = create_task.delay(task_type)
    return {"task_id": task.id}


@app.get("/tasks/{task_id}")
def get_status(task_id):
    task_result = AsyncResult(task_id,  app=celery_app)
    print(task_result)
    result = {
        "task_id": task_id,
        "task_status": task_result.status,
        "task_result": task_result.result
    }
    print(result)
    return result

# logo
@app.get("/logo", response_class=FileResponse)
async def logo():
    return "storage/assets/image/task.jpg"