from sqlalchemy import Column, Integer, String

from .database import Base


class Country(Base):
    __tablename__ = "countries"

    id = Column(Integer, primary_key=True)
    code = Column(String, index=True)
    description = Column(String, index=True)
