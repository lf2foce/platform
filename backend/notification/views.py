from typing import List
from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.orm import Session
from backend.database.core import get_db
import requests
import json
from .service import send_slack_message

router = APIRouter()


@router.post("/slack")
def slack_bot(message: str):
    response = send_slack_message(message=message)
    print(response)
    return "success"
