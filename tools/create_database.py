from sqlalchemy import *

DB_CONNET_STRING = 'mysql://root:2316678@localhost/yangqh_db'

engine = create_engine(DB_CONNET_STRING, echo = True)

meta = MetaData(engine)

user_table1 = Table('blog', meta,
               Column('id', Integer, primary_key=True, nullable=False, autoincrement=True),
               Column('title', Binary, nullable=False),
               Column('content',Binary, nullable=False),
               Column('abstract', Binary),
               Column('date',DateTime, nullable=False),
               Column('file', Integer),
               Column('tag', Binary))

user_table2 = Table('comm', meta,
               Column('id',Integer, primary_key=True, nullable=False, autoincrement=True),
               Column('author', Binary),
               Column('blog', Integer, nullable=False),
               Column('date', DateTime, nullable=False),
               Column('content', Binary),
               Column('reply', SmallInteger))

user_table3 = Table('tag', meta,
               Column('id', Integer, primary_key=True, nullable=False, autoincrement=True),
               Column('tag', Binary),
               Column('blog', Integer))

user_table1.create(bind =engine)
#user_table2.create(bind =engine)
#user_table3.create(bind =engine)