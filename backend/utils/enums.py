from enum import Enum


class OAEnum(str, Enum):
    def __str__(self) -> str:
        return str.__str__(self)


class UserRoles(OAEnum):
    owner = "Owner"
    manager = "Manager"
    admin = "Admin"
    member = "Member"
