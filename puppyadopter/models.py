## BOILERPLATE: NECESSARY FOR SQLALCHEMY

import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Date, Enum, Float, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base() # object lets SQLAlchemy know that our classes correspond to tables in our database

## DEFINE CLASSES

#association table is used to define many-to-many relationships
association_table = Table('association', Base.metadata,
    Column('puppy_id', Integer, ForeignKey('puppy.id')),
    Column('owmner_id', Integer, ForeignKey('owner.id'))
)

class Shelter(Base):

	# define tablename
	__tablename__ = 'shelter'

	# define mapping
	id = Column(Integer, primary_key = True)
	name = Column(String(250), nullable=False)
	current_occupancy = Column(Integer)
	maximum_capacity = Column(Integer, nullable=False)
	address = Column(String(80))
	city = Column(String(80))
	state = Column(String(80))
	zipCode = Column(String(5))
	website = Column(String(250))
	



class Puppy(Base):

	__tablename__ = 'puppy'
	id = Column(Integer, primary_key = True)
	name = Column(String(80), nullable=False)
	shelter_id = Column(Integer, ForeignKey('shelter.id'))
	shelter = relationship(Shelter)
	dateOfBirth = Column(Date)
	picture = Column(String(250))
	gender = Column(Enum('male', 'female', 'unknown'))
	weight = Column(Float)
	owners = relationship("Owner", secondary=association_table)
	#additional_information = relationship("PuppyProfiles", uselist =False, back_populates = 'puppy')
	puppyprofiles = relationship("PuppyProfiles",uselist=False, back_populates="puppy")


class Owner(Base):
	"""Many-to-many association with Puppy:
	One Owner can adopt many puppies; one Puppy may have many Owners"""
	__tablename__ = 'owner'
	id = Column(Integer, primary_key = True)
	name = Column(String(80), nullable=False)

class PuppyProfiles(Base):
	"""One-to-one association with class Puppy to store additional info on each puppy."""
	__tablename__ = 'puppyprofiles'
	id = Column(Integer, ForeignKey('puppy.id'), primary_key=True)
	puppy = relationship("Puppy", back_populates='puppyprofiles')


## BOILERPLATE: NECESSARY FOR SQLALCHEMY
#### keep at end of file ####
engine = create_engine('sqlite:///puppyshelter.db')

Base.metadata.create_all(engine)