from typing import List
from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.orm import Session
from database.core import get_db
import requests
import functools
import json


router = APIRouter()

url = 'https://hooks.slack.com/services/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'

headers = {'Content-type': 'application/json'}

@router.post("/slack")
def slack_bot(log: str):

    data = {"text": log}
    data = json.dumps(data)
    response = requests.post(url, headers=headers, data=data)
    return 'success'


