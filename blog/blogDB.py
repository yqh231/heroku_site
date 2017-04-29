# -*- coding: utf-8 -*-

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session
from sqlalchemy.ext.declarative import declarative_base

DB_CONNET_STRING = 'mysql://root:2316678@localhost/yangqh_db'

Base = declarative_base()
Session = scoped_session(sessionmaker())

Base.query = Session.query_property()

def make_engine():

    #engine = 'mysql+mysqlconnector'

    options = {}
    options['connect_timeout'] = 1

    #options['read_timeout'] = read_timeout

    return create_engine(
        DB_CONNET_STRING,
        pool_size=2,  #XXX 开发阶段，先用2个连接试试
        max_overflow=-1,
        pool_recycle=120,
        echo=True,
        connect_args=options,
    )

def config_db_session():
    engine = make_engine()
    Session.configure(bind = engine, autocommit = False)
