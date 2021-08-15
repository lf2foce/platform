from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Integer,
    String,
    event,
    ForeignKey,
    Text,
)
from sqlalchemy.orm import relationship, validates
from .core import Base

from slugify import slugify
from sqlalchemy.ext.hybrid import hybrid_property
from datetime import datetime

# from sqlalchemy.ext.declarative import declared_attr


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(50), unique=True, index=True)
    hashed_password = Column(String(50))
    is_active = Column(Boolean, default=True)

    items = relationship("Item", back_populates="owner")
    projects = relationship("Project", back_populates="proj_owner")


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(Text, index=True)
    knowledge = Column(Text, index=True)
    description = Column(Text, index=True)
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))

    owner = relationship("User", back_populates="items")


class Project(Base):
    __tablename__ = "projects"

    project_id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), index=True)
    run_path = Column(String(50), index=True, unique=True, nullable=False)
    description = Column(Text)
    scheduled_at = Column(Text)
    tags = Column(Text)
    project_code = Column(String(255))

    owner_id = Column(Integer, ForeignKey("users.id"))
    proj_owner = relationship("User", back_populates="projects")


class Organization(Base):
    __tablename__ = "organization"
    id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True)
    default = Column(Boolean)
    description = Column(Text)

    @hybrid_property
    def slug(self):
        return slugify(self.name)


# chưa dùng
class TimeStampMixin(object):
    """Timestamping mixin"""

    created_at = Column(DateTime, default=datetime.utcnow)
    created_at._creation_order = 9998
    updated_at = Column(DateTime, default=datetime.utcnow)
    updated_at._creation_order = 9998

    @staticmethod
    def _updated_at(mapper, connection, target):
        target.updated_at = datetime.utcnow()

    @classmethod
    def __declare_last__(cls):
        event.listen(cls, "before_update", cls._updated_at)
