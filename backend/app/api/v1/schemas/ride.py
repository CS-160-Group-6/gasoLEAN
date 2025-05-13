from datetime import datetime
from pydantic import BaseModel, Field

class RideBase(BaseModel):
    user_id: int = Field(..., description="The ID of the user/profile")
    start_time: datetime
    end_time: datetime
    distance: float
    avg_speed: float
    max_speed: float
    avg_rpm: float
    max_rpm: float
    duration: int

class RideCreate(RideBase):
    """Nothing extra—use user_id to look up profile for epa_mpg & capacity."""

class RideRead(RideBase):
    id: int
    epa_mpg: float = Field(..., description="User\'s EPA MPG at time of ride")
    actual_used_gal: float = Field(..., description="Gallons actually used")
    fuel_saved_gal: float = Field(..., description="Gallons saved vs EPA baseline")

    class ConfigDict:
        from_attributes = True