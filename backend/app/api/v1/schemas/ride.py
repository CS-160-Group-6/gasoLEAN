from datetime import datetime
from pydantic_settings import BaseSettings

class RideCreate(BaseSettings):
    '''
    Schema for creating a new ride entry.
    This schema is used to validate the data when creating a new ride entry in the database. It must be in this format that
    the frontend will send the data to the backend.
    '''
    user_id: int
    start_time: datetime
    end_time: datetime
    distance: float
    avg_speed: float # Average speed in km/h
    max_speed: float # Maximum speed in km/h
    avg_rpm: float # Average revolutions per minute
    max_rpm: float # Maximum revolutions per minute
    duration: int # Duration in seconds

class RideRead(RideCreate):
    '''
    Extends the RideCreate schema to include the ride ID and score.
    Allows SQLAlchemy to return model instances directly.
    '''
    id: int
    score: float

    class ConfigDict:
        from_attributes = True