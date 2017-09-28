from sqlalchemy import *
from engine import engine
from sqlalchemy.ext.declarative import declarative_base

meta = MetaData(bind=engine)
Base = declarative_base(engine)

"""
    ORM SCHEMA LOAD FROM DATABASE
"""
class HouseInfos(Base):
    __tablename__ = 'WebHouseCase'
    __table_args__ = { 'autoload': True }

class RentInfos(Base):
    __tablename__ = 'WebHouseCasePart2'
    __table_args__ = { 'autoload': True }

class EnvironmentInfos(Base):
    __tablename__ = 'WebHouseCasePart3'
    __table_args__ = { 'autoload': True }

