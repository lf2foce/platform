import click
import json


default_params = {"start_date": "2021-01-01", "end_date": "2021-01-01"}
default_params_string = json.dumps(default_params)


@click.command()
@click.argument("params", default=default_params_string)
# @click.option("--params", default=default_params_string)
def hello(params):
    print(params)
    params = json.loads(params)
    start_date = params["start_date"]
    end_date = params["end_date"]
    print(start_date, end_date)


if __name__ == "__main__":
    hello()

# def do_something(num1, num2, **kwargs):
#     print(num1)
#     print(num2)
#     for k,v in kwargs.items():
#         print(k,v)

# do_something(5,6,x=7,y=8)
