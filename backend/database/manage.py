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
