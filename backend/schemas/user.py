from typing import List, Optional
from pydantic import BaseModel

from pydantic.networks import EmailStr  # pydantic[email]
from pydantic import validator, Field
import bcrypt
from .item import Item
from .project import ProjectRead


def hash_password(password: str):
    """Generates a hashed version of the provided password."""
    pw = bytes(password, "utf-8")
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(pw, salt)


# Pydantic models...
class OABase(BaseModel):
    class Config:
        """
        orm_mode = True allows the app to take ORM objects and translate them into responses automatically.
        This automation saves us from manually taking data out of ORM, making it into a dictionary,
        then loading it in with Pydantic.
        """

        orm_mode = True


class UserProject(OABase):
    project: ProjectRead


class UserBase(OABase):
    email: EmailStr
    # projects: Optional[List[UserProject]] = []
    @validator("email")
    def email_required(cls, v):
        if not v:
            raise ValueError("Must not be empty string and must be a email")
        return v


class UserCreate(UserBase):
    password: str

    @validator("password")
    def password_required(cls, v):
        if not v:
            raise ValueError("Must not be empty string")
        return v


class UserRead(UserBase):
    id: int
    role: Optional[str] = Field(None, nullable=True)


class UserUpdate(OABase):
    id: int
    password: Optional[str] = Field(None, nullable=True)
    projects: Optional[List[UserProject]]
    # organizations: Optional[List[UserOrganization]]
    role: Optional[str] = Field(None, nullable=True)

    @validator("password", pre=True, always=True)
    def hash(cls, v):
        return hash_password(str(v))


class User(UserBase):
    id: int
    is_active: bool
    items: List[Item] = []
    projects: List[ProjectRead] = []

    class Config:
        orm_mode = True
