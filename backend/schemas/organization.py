from typing import List, Optional
from pydantic import BaseModel


class OABase(BaseModel):
    class Config:
        """
        orm_mode = True allows the app to take ORM objects and translate them into responses automatically.
        This automation saves us from manually taking data out of ORM, making it into a dictionary,
        then loading it in with Pydantic.
        """

        orm_mode = True


class OrganizationBase(OABase):
    id: Optional[int]
    name: str
    description: Optional[str]


class OrganizationCreate(OrganizationBase):
    pass


class OrganizationUpdate(OrganizationBase):
    pass


class OrganizationRead(OrganizationBase):
    id: Optional[int]
    slug: Optional[str]


class OrganizationPagination(OABase):
    total: int
    items: List[OrganizationRead] = []
