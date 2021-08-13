from jinja2 import Template
from .gbq import BQConnection
from datetime import datetime, date, timedelta

today = datetime.today().strftime("%Y-%m-%d")
first_date_of_month = format(date.today().replace(day=1), "%Y-%m-%d")
cutoff_date = format(date.today().replace(day=26), "%Y-%m-%d")
# fdom = "select DATE_TRUNC(date( '2008-12-25 15:30:00'), month)"
# first_date_of_month = f"select DATE_TRUNC(date('{today}'), month)" #BQ SQL


bqcon = BQConnection(project="vinid-data-selfservice-prod")


def between_date_bq(
    template_query, start_date=first_date_of_month, end_date=cutoff_date, auto=True
):
    if auto and template_query:
        print(start_date, end_date)
        if datetime.now().day == 26:
            QUERY = Template(template_query).render(
                start_date=start_date, end_date=end_date
            )
            query_job = bqcon.client.query(QUERY)
            df = query_job.result().to_dataframe()
            return df, QUERY
    else:
        if template_query:
            print(start_date, end_date)
            QUERY = Template(template_query).render(
                start_date=start_date, end_date=end_date
            )
            query_job = bqcon.client.query(QUERY)
            df = query_job.result().to_dataframe()
            return df, QUERY
        return False


bq_query = """
                SELECT COUNT(DISTINCT tcb_transaction_id) as total_transaction, SUM(amount) as total_amount
                FROM `vinid-data-selfservice-prod.ONELOYALTY_MART.F_TCB_FILE_TRANSACTION`
                WHERE calendar_dim_id BETWEEN '{{start_date}}' AND '{{end_date}}'
                """

# a = between_date_bq(bq_template_query, '2021-06-01', '2021-07-25')
# print(a)

# a = between_date_bq(bq_query, start_date='2021-06-01', auto=False)
# print(a)
