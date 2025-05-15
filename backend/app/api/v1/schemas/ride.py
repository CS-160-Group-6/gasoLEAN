from datetime import datetime
from pydantic import BaseModel, Field
from pydantic import ConfigDict

class RideBase(BaseModel):
    '''
    Base only has things every schema shares
    '''
    user_id: int

class RideCreate(RideBase):
    '''
    RideCreate asks ONLY for what the client supplies. Everything else is set by the service)
    '''
    start_fuel_pct: float
    end_fuel_pct: float

class RideRead(BaseModel):
    '''
    RideRead exposes every field the frontend needs
    '''
    id: int
    user_id: int
    start_time: datetime
    end_time: datetime
    duration: int
    distance: float
    avg_speed: float
    max_speed: float
    avg_rpm: float
    max_rpm: float
    epa_mpg: float
    actual_used_gal: float
    fuel_saved_gal: float

    class ConfigDict:
        from_attributes = True
