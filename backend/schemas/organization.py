from typing import List, Optional
from models import LokiBase

class OrganizationBase(LokiBase):
    id: Optional[int]
    name: str
    description: Optional[str]
    default: Optional[bool]
    banner_enabled: Optional[bool]
    banner_color: Optional[str]
    banner_text: Optional[str]


class OrganizationCreate(OrganizationBase):
    pass


class OrganizationUpdate(OrganizationBase):
    pass


class OrganizationRead(OrganizationBase):
    id: Optional[int]
    slug: Optional[str]


class OrganizationPagination(LokiBase):
    total: int
    items: List[OrganizationRead] = []