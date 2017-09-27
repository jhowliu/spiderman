from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import meta

# [driver]://user:password@host/dbname
engine = create_engine('mysql://{}:{}@{}/WebEXTDW?charset=utf8'.format( \
                meta['username'], meta['password'], meta['host']), encoding='utf-8')


Session = sessionmaker(bind=engine)
Session.configure(bind=engine)

sess = Session()
