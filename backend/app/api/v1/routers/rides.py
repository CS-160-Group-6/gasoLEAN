from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.db.models import Ride
from app.db.crud import ride as ride_crud
from app.core.scoring import compute_score
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

@router.get(path="/rides", response_model=list[RideRead], status_code=status.HTTP_200_OK)
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

@router.get(path="/rides/{ride_id}", response_model=RideRead, status_code=status.HTTP_200_OK)
def get_ride(ride_id: int, db: Session = Depends(dependency=get_db)) -> Ride:
    '''
    Get a ride by its ID. Use a GET request to retrieve a ride by its ID.
    :param ride_id: ID of the ride to retrieve
    :param db: Database session dependency
    :return: Ride entry with the specified ID
    '''
    ride: Ride = db.query(Ride).filter(Ride.id == ride_id).first()

    if not ride:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Ride #{ride_id} not found")

    return ride

@router.put(path="/rides/{ride_id}", response_model=RideRead, status_code=status.HTTP_200_OK)
def update_ride(ride_id: int, payload: RideCreate, db: Session = Depends(dependency=get_db)) -> Ride:
    '''
    Update a ride by its ID. Use a PUT request to update a ride by its ID.
    :param ride_id: ID of the ride to update
    :param payload: A JSON schema containing the ride data. The schema must contain all the fields specified in the RideCreate schema.
    :param db: Database session dependency
    :return: Updated Ride entry
    '''
    ride: Ride = db.query(Ride).filter(Ride.id == ride_id).first()
    if not ride:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Ride #{ride_id} not found")

    score: float = compute_score(distance=payload.distance,
                          avg_speed=payload.avg_speed,
                          max_speed=payload.max_speed,
                          avg_rpm=payload.avg_rpm,
                          max_rpm=payload.max_rpm,
                          duration=payload.duration)

    db.query(Ride).filter(Ride.id == ride_id).update(values={
        "user_id": payload.user_id,
        "start_time": payload.start_time,
        "end_time": payload.end_time,
        "distance": payload.distance,
        "avg_speed": payload.avg_speed,
        "max_speed": payload.max_speed,
        "avg_rpm": payload.avg_rpm,
        "max_rpm": payload.max_rpm,
        "duration": payload.duration,
        "score": score
    })

    db.commit()
    db.refresh(ride)
    return ride

    # Another way to do the above
    """ ride.user_id = payload.user_id
    ride.start_time = payload.start_time
    ride.end_time = payload.end_time
    ride.distance = payload.distance
    ride.avg_speed = payload.avg_speed
    ride.max_speed = payload.max_speed
    ride.avg_rpm = payload.avg_rpm
    ride.max_rpm = payload.max_rpm
    ride.duration = payload.duration
    ride.score = score """

@router.delete(path="/rides/{ride_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_ride(ride_id: int, db: Session = Depends(dependency=get_db)) -> None:
    '''

    '''
    # Check if the ride exists
    ride: Ride = db.query(Ride).filter(Ride.id == ride_id).first()

    if not ride:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Ride #{ride_id} not found")

    # Delete the ride
    db.delete(ride)
    db.commit()