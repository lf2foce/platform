import re
from sqlalchemy import create_engine
from sqlalchemy import inspect

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from backend import config


# SQLALCHEMY_DATABASE_URI = "postgresql://user:password@postgresserver/db"

engine = create_engine(
    str(config.SQLALCHEMY_DATABASE_URI),
    # connect_args={"check_same_thread": False},  # nếu dùng SQLite
)
SessionLocal = sessionmaker(bind=engine, future=True)  # future=True 2.0 syntax

Base = declarative_base()
# all models inherit from and how they get SQLAlchemy ORM functionality


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# print(inspect(engine).get_table_names())

# # low level
# from sqlalchemy import MetaData, Table

# metadata = MetaData()

# with engine.connect() as connection:
#     # reflect all tables
#     metadata.reflect(connection)
#     # reflect individual table
#     apscheduler_jobs_table = Table(
#         "apscheduler_jobs", metadata, autoload_with=connection
#     )
#     # execute SQL statements
#     result = connection.execute(apscheduler_jobs_table.select())

# print(repr(apscheduler_jobs_table))  # column type
