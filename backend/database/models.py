from sqlalchemy import (
    Boolean,
    Column,
    Integer,
    String,
    event,
    ForeignKey,
    Text,
    Float,
    LargeBinary,
    TIMESTAMP,
    DateTime,
    Unicode,
)
from sqlalchemy.orm import relationship, validates
from .core import Base, engine
from slugify import slugify
from sqlalchemy.ext.hybrid import hybrid_property
from datetime import datetime

# from sqlalchemy.ext.declarative import declared_attr

# auto add created_at & updated_at
class TimeStampMixin(object):
    """Timestamping mixin"""

    created_at = Column(DateTime, default=datetime)  # .utcnow
    created_at._creation_order = 9998
    updated_at = Column(DateTime, default=datetime)
    updated_at._creation_order = 9998

    @staticmethod
    def _updated_at(mapper, connection, target):
        target.updated_at = datetime  # .utcnow()

    @classmethod
    def __declare_last__(cls):
        event.listen(cls, "before_update", cls._updated_at)


class User(Base, TimeStampMixin):
    __tablename__ = "users"
    # __table_args__ = {"schema": "oa_platform"}

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(50), unique=True, index=True)
    hashed_password = Column(String(50))
    is_active = Column(Boolean, default=True)

    items = relationship("Item", back_populates="owner")
    projects = relationship("Project", back_populates="proj_owner")


class Item(Base, TimeStampMixin):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), index=True)
    knowledge = Column(Text)
    description = Column(Text)

    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    owner = relationship("User", back_populates="items")


class Project(Base, TimeStampMixin):
    __tablename__ = "projects"
    # __table_args__ = {"schema": "oa_platform"}

    project_id = Column(Integer, primary_key=True, index=True)  # , autoincrement=True
    title = Column(String(255), index=True)
    run_path = Column(String(50), index=True, unique=True, nullable=False)
    description = Column(Text)
    scheduled_at = Column(Text)
    tags = Column(Text)
    project_code = Column(String(255))

    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    proj_owner = relationship("User", back_populates="projects")

    schedules = relationship("APSchedulerJobsTable", back_populates="schedule_owner")


current_time = datetime.now()


class APSchedulerJobsTable(Base):
    __tablename__ = "apscheduler_jobs"
    # 191 = max key length in MySQL for InnoDB/utf8mb4 tables, 25 = precision that translates to an 8-byte float
    id = Column(Unicode(191, _warn_on_bytestring=False), primary_key=True)
    next_run_time = Column(Float(25))
    job_state = Column(LargeBinary, nullable=False)
    desc = Column(String(255))
    tag = Column(String(255))
    project_id = Column(Integer, ForeignKey("projects.project_id", ondelete="CASCADE"))
    created_at = Column(DateTime)  # default=datetime.utcnow

    schedule_owner = relationship("Project", back_populates="schedules")


class Organization(Base):
    __tablename__ = "organization"
    id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True)
    slug = Column(String)
    description = Column(Text)

    @hybrid_property
    def slug(self):
        return slugify(self.name)
