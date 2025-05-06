from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.core.scoring import compute_score
from app.db.models import Ride
from app.api.v1.schemas.ride import RideCreate, RideRead

router = APIRouter()

@router.post(path="/rides", response_model=RideRead, status_code=status.HTTP_201_CREATED)
def create_ride(payload: RideCreate, db: Session = Depends(dependency=get_db)) -> Ride:
    '''
    Create a new ride entry in the database.
    This endpoint is used to create a new ride entry in the database. It takes a RideCreate schema as input and returns
    the created Ride entry.

    :param payload: A JSON schema containing the ride data. The schema must contain all the fields specified in the RideCreate schema.
    :param db: Database session dependency
    :return: Created Ride entry
    '''

    # Calculate score
    score: float = compute_score(distance=payload.distance,
                  avg_speed=payload.avg_speed,
                  max_speed=payload.max_speed,
                  avg_rpm=payload.avg_rpm,
                  max_rpm=payload.max_rpm,
                  duration=payload.duration)

    # Save to database
    # Ride(**payload.dict(), score=score) works because
    # Ride.__init__ accepts 'user_id', 'start_time', …, 'duration', and 'score'. The __init__ method is given by SQLAlchemy
    ride: Ride = Ride(**payload.dict(), score=score)
    db.add(ride)
    db.commit()
    db.refresh(ride)

    return ride

@router.get(path="/rides", response_model=list[RideRead])
def list_rides(db: Session = Depends(dependency=get_db)) -> List[Ride]:
    '''
    List all rides in the database. Use a GET request to retrieve all rides.
    :param db: Database session dependency
    :return: List of all rides in the database
    '''
    rides: List[Ride] = db.query(Ride).order_by(Ride.start_time.desc()).all()

    if not rides:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No rides found")

    return rides