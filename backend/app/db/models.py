import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey, String

Base = declarative_base()

class Profile(Base):
    '''
    ORM model for a user profile.
    This model represents a user profile in the database. It
    is used to store and retrieve user data from the database.
    Each profile has a unique ID, name, EPA MPG rating, and
    tank capacity in gallons. The EPA MPG rating is used to
    calculate the fuel efficiency of the car. The tank capacity
    is used to determine the maximum amount of fuel that can be
    stored in the car.
    '''
    __tablename__: str = "profiles"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, nullable=False)
    epa_mpg = Column(Float, nullable=False)
    tank_capacity_gallons = Column(Float, nullable=False)

class Ride(Base):
    '''
    ORM model for a car ride.
    This model represents a ride taken by a user, including various metrics such as speed, distance, and duration.
    It is used to store and retrieve ride data from the database.
    '''
    __tablename__: str = "rides"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, index=True)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    distance = Column(Float, nullable=False)
    epa_mpg = Column(Float, nullable=False)
    actual_used_gal = Column(Float, nullable=False, default=0.0)
    fuel_saved_gal = Column(Float, nullable=False, default=0.0)
    avg_speed = Column(Float, nullable=False)
    max_speed = Column(Float, nullable=False)
    avg_rpm = Column(Float, nullable=False)
    max_rpm = Column(Float, nullable=False)
    duration = Column(Integer, nullable=False)
    score = Column(Float, nullable=False)

class Measurement(Base):
    '''
    ORM model for a measurement.
    This model represents a measurement taken during a ride. The measurements taken are for speed, and RPM.
    Each measurement is associated with a ride and has a timestamp. It is used to store and retrieve
    measurement data from the database.
    '''
    __tablename__: str = "measurements"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    ride_id = Column(Integer, ForeignKey("rides.id"), nullable=False, index=True)
    timestamp = Column(DateTime, default=datetime.datetime.now, nullable=False)
    speed = Column(Float, nullable=False)
    rpm = Column(Float, nullable=False)
    fuel_level_pct = Column(Float, nullable=False)