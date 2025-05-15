from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import Result
from sqlalchemy.orm import Session
from sqlalchemy.sql import text

from app.db.session import get_db
from app.api.v1.schemas.health import HealthResponse

router = APIRouter()

@router.get(path="/health", response_model=HealthResponse)
def health_check(db: Session = Depends(dependency=get_db)) -> HealthResponse:
    '''
    Health check endpoint to verify the API is running and the database connection is healthy.
    This endpoint returns a simple status message indicating the health of the API and database.
    :param db: Database session dependency
    '''

    result = db.execute(text('SELECT 1'))
    if not isinstance(result, Result):
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE , detail="Database connection failed")

    return HealthResponse(status="ok")