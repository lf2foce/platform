from typing import List
from fastapi import APIRouter, Depends, Request, HTTPException, APIRouter
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from google.cloud import bigquery

router = APIRouter()

templates = Jinja2Templates(directory="templates")


@router.get("/bq", response_class=HTMLResponse)
def bq(request: Request):
    client = bigquery.Client()

    # Perform a query.
    QUERY = (
        'SELECT name FROM `bigquery-public-data.usa_names.usa_1910_2013` '
        'WHERE state = "TX" '
        'LIMIT 10')
    query_job = client.query(QUERY)  # API request
    rows = query_job.result() # Waits for query to finish, jinja worked

    return templates.TemplateResponse("bq.html", {"request": request, "rows": rows})    
