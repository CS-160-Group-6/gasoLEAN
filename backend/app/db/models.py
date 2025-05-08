import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, ForeignKey, Integer, Float, DateTime

# Base class for all ORM models
Base = declarative_base()

class Ride(Base):
    '''
    ORM model for a car ride.
    This model represents a ride taken by a user, including various metrics such as speed, distance, and duration.
    It is used to store and retrieve ride data from the database.
    '''
    __tablename__: str = 'rides'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, index=True)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    distance = Column(Float, nullable=False)
    avg_speed = Column(Float, nullable=False) # Average speed in km/h
    max_speed = Column(Float, nullable=False) # Maximum speed in km/h
    avg_rpm = Column(Float, nullable=False) # Average revolutions per minute
    max_rpm = Column(Float, nullable=False) # Maximum revolutions per minute
    duration = Column(Integer, nullable=False) # Duration in seconds
    score = Column(Float, nullable=False)

class Measurement(Base):
    '''
    ORM model for a measurement.
    This model represents a measurement taken during a ride. The measurements taken are for speed, and RPM.
    Each measurement is associated with a ride and has a timestamp. It is used to store and retrieve
    measurement data from the database.
    '''
    __tablename__: str = 'measurements'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    ride_id = Column(Integer, ForeignKey(column="rides.id"), nullable=False, index=True)
    timestamp = Column(DateTime, default=datetime.datetime.now, nullable=False)
    speed = Column(Float, nullable=False) # Speed in km/h
    rpm = Column(Float, nullable=False) # Revolutions per minute