from typing import List
from fastapi import APIRouter, Depends, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.responses import FileResponse
# from .service


router = APIRouter()


@router.get("/example/files", response_class=FileResponse)
async def my_file():
    return "storage/assets/image/task.jpg"