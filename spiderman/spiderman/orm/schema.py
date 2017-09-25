from sqlalchemy import *
from engine import engine
from sqlalchemy.ext.declarative import declarative_base

meta = MetaData(bind=engine)

Base = declarative_base(engine)

"""
    ORM SCHEMA LOAD FROM DATABASE
"""
class HouseInfo1(Base):
    __tablename__ = 'WebHouseCase'
    __table_args__ = { 'autoload': True }

class HouseInfo2(Base):
    __tablename__ = 'WebHouseCasePart2'
    __table_args__ = { 'autoload': True }

class HouseInfo3(Base):
    __tablename__ = 'WebHouseCasePart3'
    __table_args__ = { 'autoload': True }

class HouseInfo4(Base):
    __tablename__ = 'WebHouseCasePart4'
    __table_args__ = { 'autoload': True }
