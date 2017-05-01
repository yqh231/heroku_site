from sqlalchemy import Column,BigInteger,Text, DateTime, Integer, SmallInteger,Binary

from blogDB import Base
class tbl_blog(Base):

    __tablename__  = 'blog'

    id = Column(Integer, primary_key = True, nullable=False, autoincrement=True)
    title = Column(Binary, nullable = False)
    content = Column(Binary, nullable = False)
    abstract = Column(Binary)
    date = Column(DateTime, nullable = False)
    file =  Column(Integer)
    tag = Column(Binary)


class tbl_comm(Base):

    __tablename__ = 'comm'

    id = Column(Integer, primary_key = True, nullable = False, autoincrement=True)
    author = Column(Binary)
    blog = Column(Integer, nullable = False)
    date = Column(DateTime, nullable = False)
    content = Column(Binary)
    reply = Column(SmallInteger)

class tbl_tag(Base):
    __tablename__ = 'tag'

    id = Column(Integer, primary_key = True, nullable = False, autoincrement=True)
    tag = Column(Binary)
    blog = Column(Integer)