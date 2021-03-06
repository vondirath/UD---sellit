# [BEGIN IMPORTS]
# for mapper code
from sqlalchemy import (Column, ForeignKey, Integer,
                        String, DateTime, create_engine)
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


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(80), nullable=False)
    picture = Column(String(250))

    @property
    def serialize(self):
        return {
            'name': self.name,
            'id': self.id,
        }


class Store(Base):
    __tablename__ = 'store'

    id = Column(Integer, primary_key=True)
    name = Column(String(20), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        return {
            'name': self.name,
            'id': self.id,
        }


class Posts(Base):
    __tablename__ = 'posts'

    title = Column(String(80), nullable=False)
    description = Column(String(200), nullable=False)
    id = Column(Integer, primary_key=True)
    # created datetime and updated/edited datetime function.
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())
    img_name = Column(String(80))
    price = Column(String(20))
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)
    # update using google API when over https
    zipcode = Column(String(80), nullable=True)
    store_id = Column(Integer, ForeignKey('store.id'))
    store = relationship(Store)

    @property
    def serialize(self):
        return {
            'title': self.title,
            'description': self.description,
            'id': self.id,
            'created': self.time_created,
            'edited': self.time_updated,
            'img': self.img_name,
            'price': self.price
        }


# create a new file similar to a robust database
engine = create_engine(
    'sqlite:///sellitdata.db')
# goes into database and adds classes as new tables in database
Base.metadata.create_all(engine)
