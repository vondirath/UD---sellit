# [BEGIN IMPORTS]
import datetime
import os
# manipulate python runtime
import sys
# for mapper code
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
# use in config and class
from sqlalchemy.ext.declarative import declarative_base
# for mapper
from sqlalchemy.orm import relationship
# use in config code
from sqlalchemy import create_engine
# for relationship table
from sqlalchemy.schema import Table
from sqlalchemy.sql import func
# [END IMPORTS]

# Lets sqlalchemy know that our classes are special sqlalchemy
# classes that correspond to tables in database
Base = declarative_base()

#implement later on? associate posts to comments first
"""
# locate remote tables posts belong to users (for ease of deletion)
association_table = Table('association', Base.metadata,
    Column('user_id', Integer, ForeignKey('user.id')),
    Column('posts_id', Integer, ForeignKey('posts.id'))
)

# questions association
class User(Base):
    __tablename__='user'

    # nullable if no name cant create
    name = Column(String(20), nullable=False)
    id = Column(Integer, primary_key=True)
    password = Column(String(80), nullable=False)
    email = Column(String(80), nullable=False)
    location = Column(String(80), nullable=False)
    # association table related. check if backref is necessary
    posts = relationship("Posts",
                    secondary=association_table,
                    backref="users")
"""


class Posts(Base):
    __tablename__='posts'

    title = Column(String(80), nullable=False)
    description = Column(String(200), nullable=False)
    id = Column(Integer, primary_key=True)
    # created datetime and updated/edited datetime function.
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())
    post_img_path = Column(String (80))
    price = Column(String(20))


class Questions(Base):
    __tablename__='questions'

    poster_name = Column(String(30), nullable=False)
    id = Column(Integer, primary_key=True)
    question = Column(String(250))
    post_id = Column(Integer, ForeignKey('posts.id'))
    post = relationship(Posts)
    time_created = Column(DateTime(timezone=True), server_default=func.now())  

# create a new file similar to a robust database
engine = create_engine(
    'sqlite:///sellitdata.db')
# goes into database and adds classes as new tables in database
Base.metadata.create_all(engine)
