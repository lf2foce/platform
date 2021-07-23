import os
import logging
import config
from .core import Base, sessionmaker
from sqlalchemy_utils import create_database, database_exists

# đang test, chưa dùng đến

def get_core_tables():
    """Fetches tables are belong to the 'oa_core' schema."""
    core_tables = []
    for _, table in Base.metadata.tables.items():
        if table.schema == "oa_core":
            core_tables.append(table)
    return core_tables

def init_database(engine):
    """Initializes a the database."""
    if not database_exists(str(config.SQLALCHEMY_DATABASE_URI)):
        create_database(str(config.SQLALCHEMY_DATABASE_URI))
    
    tables = get_core_tables()
    
    Base.metadata.create_all(engine, tables=tables)