from slugify import slugify

from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy import Column, Integer, String, Boolean

from database.core import Base



class Organization(Base):
    __tablename__ = "organization"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    default = Column(Boolean)
    description = Column(String)

    @hybrid_property
    def slug(self):
        return slugify(self.name)
