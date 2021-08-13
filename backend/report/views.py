from textwrap import dedent
import black
import sqlparse
from pathlib import Path
from typing import Optional
from fastapi import Depends, FastAPI, HTTPException, Request, APIRouter
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from google.cloud import bigquery
from .gbq import BQConnection
from .service import between_date_bq
from pretty_html_table import build_table


templates = Jinja2Templates(directory="templates")

router = APIRouter()

sql_temp_path = Path(__file__).parent.resolve()


class SqlTemplateRequest(BaseModel):
    start_date: str = "2021-06-01"
    end_date: str = "2021-07-25"


@router.get("/report", response_class=HTMLResponse)
def report(request: Request):
    return templates.TemplateResponse("report.html", {"request": request})


@router.get("/sql-view", response_class=HTMLResponse)
def report(request: Request):
    query_temp = """
                SELECT
                    COUNT(DISTINCT tcb_transaction_id) as total_transaction,
                    SUM(amount) as total_amount
                FROM `vinid-data-selfservice-prod.ONELOYALTY_MART.F_TCB_FILE_TRANSACTION`
                WHERE calendar_dim_id BETWEEN '{{start_date}}' AND '{{end_date}}'
                """
    query_temp = dedent(query_temp).strip("\n")
    # format text in py file
    # project_file_name = "bq_temp"
    # project_file_path = sql_temp_path / (project_file_name + ".py")
    # if project_file_path.exists():
    #     with open(project_file_path, encoding="UTF-8") as f:
    #         code = f.read()
    #         code = dedent(code).strip("\n")
    #     formatted = black.format_str(code, mode=black.FileMode(line_length=79)) # để print

    # df, query = between_date_bq(query_temp, auto=False)
    return templates.TemplateResponse(
        "sql-view.html", {"request": request, "code": query_temp}
    )


@router.post("/sql")
def report(template: SqlTemplateRequest):
    print(template)
    query_temp = """
                SELECT COUNT(DISTINCT tcb_transaction_id) as total_transaction, SUM(amount) as total_amount
                FROM `vinid-data-selfservice-prod.ONELOYALTY_MART.F_TCB_FILE_TRANSACTION`
                WHERE calendar_dim_id BETWEEN '{{start_date}}' AND '{{end_date}}'
                """
    df, query = between_date_bq(
        query_temp,
        start_date=template.start_date,
        end_date=template.end_date,
        auto=False,
    )
    if len(df) > 0:
        html_body = "<hr><h6 class='mt-3'>Total transaction</h6>\n"
        html_body += build_table(df, "blue_light")
    print(html_body)
    return {"a": query, "b": html_body}


@router.get("/bq", response_class=HTMLResponse)
def bq(request: Request):
    # client = bigquery.Client()
    bqcon = BQConnection(project="vinid-data-selfservice-prod")
    # Perform a query.
    QUERY = """
            SELECT COUNT(DISTINCT tcb_transaction_id) as total_transaction, SUM(amount)as total_amount
            FROM `vinid-data-selfservice-prod.ONELOYALTY_MART.F_TCB_FILE_TRANSACTION`
            WHERE calendar_dim_id BETWEEN  '2021-06-01' AND '2021-07-25'     
            """

    query_job = bqcon.client.query(QUERY)
    rows = query_job.result()  # Waits for query to finish, jinja worked
    df = query_job.result().to_dataframe()
    print(df)

    return templates.TemplateResponse(
        "bq_temp.html", {"request": request, "rows": rows}
    )
