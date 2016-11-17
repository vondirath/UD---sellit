# [BEGIN IMPORTS]
# for mapper code
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, create_engine
# use in config and class
from sqlalchemy.ext.declarative import declarative_base
# for mapper
from sqlalchemy.orm import relationship
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
"""

class User(Base):
    __tablename__='user'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(80), nullable=False)
    location = Column(String(80), nullable=True)
    picture = Column(String(250))

    @property
    def serialize(self):
        return {
            'name': self.name,
            'id': self.id,
        }


class Posts(Base):
    __tablename__='posts'

    title = Column(String(80), nullable=False)
    description = Column(String(200), nullable=False)
    id = Column(Integer, primary_key=True)
    # created datetime and updated/edited datetime function.
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())
    img_name = Column(String (80))
    price = Column(String(20))
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)
    zipcode = Column(String(5), nullable=False)

    @property
    def serialize(self):
        return {
            'title' : self.title,
            'description' : self.description,
            'id' : self.id,
            'created' : self.time_created,
            'edited' : self.time_updated,
            'img' : self.img_name,
            'price' : self.price
        }

"""

class Questions(Base):
    __tablename__='questions'

    poster_name = Column(String(30), nullable=False)
    id = Column(Integer, primary_key=True)
    question = Column(String(250))
    post_id = Column(Integer, ForeignKey('posts.id'))
    post = relationship(Posts)
    time_created = Column(DateTime(timezone=True), server_default=func.now()) 
 
"""
# create a new file similar to a robust database
engine = create_engine(
    'sqlite:///sellitdata.db')
# goes into database and adds classes as new tables in database
Base.metadata.create_all(engine)
