from sqlalchemy import Column,BigInteger,Text, DateTime, Integer, SmallInteger

from blogDB import Base
class tbl_blog(Base):

    __tablename__  = 'blog'

    id = Column(Integer, primary_key = True, nullable=False, autoincrement=True)
    title = Column(Text, nullable = False)
    content = Column(Text, nullable = False)
    abstract = Column(Text)
    date = Column(DateTime, nullable = False)
    file =  Column(Integer)


class tbl_comm(Base):

    __tablename__ = 'comm'

    id = Column(Integer, primary_key = True, nullable = False, autoincrement=True)
    author = Column(Text)
    blog = Column(Integer, nullable = False)
    date = Column(DateTime, nullable = False)
    reply = Column(SmallInteger)

class tbl_tag(Base):
    __tablename__ = 'tag'

    id = Column(Integer, primary_key = True, nullable = False, autoincrement=True)
    tag = Column(Text)
    blog = Column(Integer)