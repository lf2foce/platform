import logging
import os

import click
import uvicorn
from backend import __version__, config
from backend.utils.enums import UserRoles

from scheduler.views import Schedule
from backend.database.core import SessionLocal
from backend.utils.logging import configure_logging


log = logging.getLogger(__name__)


@click.group()
@click.version_option(version=__version__)
def oa_platform_cli():
    """Command-line interface to"""
    configure_logging()


@oa_platform_cli.group("database")
def oa_platform_database():
    """Container for all oa_platform database commands."""
    pass


@oa_platform_database.command("init")
def database_init():
    """Initializes a new database."""
    click.echo("Initializing new database...")
    from .database.core import engine
    from .database.manage import (
        init_database,
    )

    init_database(engine)
    click.secho("Success.", fg="green")


@oa_platform_cli.group("user")
def oa_platform_user():
    """Container for all user commands."""
    pass


# development
@oa_platform_user.command("update")
@click.argument("email")
@click.option(
    "--organization",
    "-o",
    required=True,
    help="Organization to set role for.",
)
@click.option(
    "--role",
    "-r",
    required=True,
    type=click.Choice(UserRoles),
    help="Role to be assigned to the user.",
)
def update_user(email: str, role: str, organization: str):
    """Updates a user's roles."""
    from backend.database.core import SessionLocal
    from backend.auth import service as user_service
    from backend.database.models import UserUpdate, UserOrganization

    db_session = SessionLocal()
    user = user_service.get_user_by_email(email=email, db=db_session)
    if not user:
        click.secho(f"No user found. Email: {email}", fg="red")
        return

    click.secho("User successfully updated.", fg="green")
