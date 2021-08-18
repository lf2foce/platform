import re
from sqlalchemy import create_engine
from sqlalchemy import inspect

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from backend import config


# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

engine = create_engine(
    str(config.SQLALCHEMY_DATABASE_URL),
    # connect_args={"check_same_thread": False},  # nếu dùng SQLite
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# print(inspect(engine).get_table_names())
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


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
