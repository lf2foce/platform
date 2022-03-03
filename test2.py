import click


@click.command()
@click.argument("start_date", default="2021-01-01")  # string
@click.argument("end_date", default="2021-12-01")
def main(start_date, end_date):
    print("data from: ", start_date, end_date)


if __name__ == "__main__":
    main()
