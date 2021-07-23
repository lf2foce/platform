from sqlalchemy import Boolean, Column, DateTime, Integer, String, event, ForeignKey
from sqlalchemy.orm import relationship
from database.core import Base
from slugify import slugify
from sqlalchemy.ext.hybrid import hybrid_property



class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    items = relationship("Item", back_populates="owner")
    projects = relationship("Project", back_populates="proj_owner")


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="items")

class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    scheduled_at = Column(String, index=True)
    tags = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))

    proj_owner = relationship("User", back_populates="projects")


class Organization(Base):
    __tablename__ = "organization"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    default = Column(Boolean)
    description = Column(String)

    @hybrid_property
    def slug(self):
        return slugify(self.name)
