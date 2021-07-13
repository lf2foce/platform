
from typing import List, Optional

from pydantic import BaseModel



# Pydantic models...
class LokiBase(BaseModel):
    class Config:
        orm_mode = True
        # bên dưới từ dispatch
        # validate_assignment = True
        # arbitrary_types_allowed = True
        # anystr_strip_whitespace = True


class ItemBase(BaseModel):
    title: str
    description: Optional[str] = None


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    items: List[Item] = []

    class Config:
        orm_mode = True