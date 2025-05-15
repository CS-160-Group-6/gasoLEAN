from pydantic import BaseModel

class ProfileBase(BaseModel):
    '''
    Base schema for user profile.
    '''
    name: str
    epa_mpg: float
    tank_capacity_gallons: float

class ProfileCreate(ProfileBase):
    '''
    Schema for creating a new profile entry.
    This schema is used to validate the data when creating a
    new profile entry in the database. It must be in this
    format that the frontend will send the data to the backend.
    '''
    pass

class ProfileRead(ProfileBase):
    '''
    Extends the ProfileBase schema to include the profile ID.
    Allows SQLAlchemy to return model instances directly.
    '''
    id: int

    class ConfigDict:
        from_attributes = True
