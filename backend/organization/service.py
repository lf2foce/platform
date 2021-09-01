from typing import List, Optional
from pydantic.error_wrappers import ErrorWrapper, ValidationError
from sqlalchemy.sql.expression import true

from backend.schemas.user import UserBase  # OAProjectOrganization
from backend.utils.enums import UserRoles

from backend.utils.exceptions import NotFoundError
from backend.schemas.organization import (
    OrganizationBase,
    OrganizationCreate,
    # OrganizationRead,
    # OrganizationUpdate,
)


def create(*, db_session, organization_in: OrganizationCreate):
    """Creates an organization."""
    organization = OrganizationBase(
        **organization_in.dict(),
    )

    db_session.add(organization)
    db_session.commit()
    return organization
