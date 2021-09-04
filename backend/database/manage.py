from backend import config
from .core import Base
from sqlalchemy_utils import create_database, database_exists

# init from click
def init_database(engine):
    """Initializes a the database."""
    if not database_exists(str(config.SQLALCHEMY_DATABASE_URI)):
        create_database(str(config.SQLALCHEMY_DATABASE_URI))

    with engine.connect() as connection:
        pass

    Base.metadata.create_all(bind=engine)
