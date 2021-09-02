from enum import Enum


class OAEnum(str, Enum):
    def __str__(self) -> str:
        return str.__str__(self)


# test
class UserRoles(OAEnum):
    admin = "Admin"  # full authorization
    author = "Author"  # dev, create job
    manager = "Manager"  # approval, triggle
    member = "Member"  # public
