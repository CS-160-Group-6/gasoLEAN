from pydantic_settings import BaseSettings
import datetime

class MeasurementCreate(BaseSettings):
    '''
    Pydantic model for creating a measurement.
    This model is used to validate the data when creating a new measurement.
    '''
    ride_id: int
    speed: float
    rpm: float
    fuel_level_pct: float

class MeasurementRead(BaseSettings):
    '''
    Pydantic model for reading a measurement.
    This model is used to validate the data when reading a measurement from the database.
    '''
    id: int
    ride_id: int
    timestamp: datetime.datetime
    speed: float
    rpm: float
    fuel_level_pct: float

    class ConfigDict:
        from_attributes = True