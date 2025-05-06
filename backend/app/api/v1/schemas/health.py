from pydantic import BaseModel

class HealthResponse(BaseModel):
    '''
    Represents the health status of the API and database connection.
    This schema is used to return a simple status message indicating whether the API is running and the database connection is healthy.
    '''
    status: str