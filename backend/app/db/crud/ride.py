from typing import List
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.db.models import Ride, Profile
from app.api.v1.schemas.ride import RideCreate
from app.core.scoring import compute_score  # your existing score fn

def create_ride(db: Session, payload: RideCreate) -> Ride:
    '''
    Create a new ride entry in the database.
    This endpoint is used to create a new ride entry in the database. It takes a RideCreate schema as input and returns
    the created Ride entry.

    :param payload: A JSON schema containing the ride data. The schema must contain all the fields specified in the RideCreate schema.
    :param db: Database session
    :return: Created Ride entry
    '''
    # Look up user’s profile for EPA & capacity
    profile: Profile | None = db.query(Profile).filter(Profile.id == payload.user_id).first()
    if not profile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Profile #{payload.user_id} not found")

    # Compute actual gallons used via start/end fuel_level_pct measurements
    #    (assumes you stored first/last measurement fuel_level_pct elsewhere)
    start_pct = getattr(payload, "start_fuel_pct", None)
    end_pct   = getattr(payload, "end_fuel_pct", None)
    if start_pct is None or end_pct is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Missing start_fuel_pct or end_fuel_pct")
    actual_used = (start_pct - end_pct) * profile.tank_capacity_gallons

    # EPA-baseline gallons = distance / epa_mpg
    expected_used = payload.distance / profile.epa_mpg

    # Fuel saved
    saved = expected_used - actual_used

    # Score as before
    score: float = compute_score(
        distance=payload.distance,
        avg_speed=payload.avg_speed,
        max_speed=payload.max_speed,
        avg_rpm=payload.avg_rpm,
        max_rpm=payload.max_rpm,
        duration=payload.duration,
    )

    ride = Ride(
        **payload.dict(),
        epa_mpg=profile.epa_mpg,
        actual_used_gal=actual_used,
        fuel_saved_gal=saved,
        score=score,
    )
    db.add(ride)
    db.commit()
    db.refresh(ride)
    return ride

def list_rides(db: Session) -> List[Ride]:
    '''
    List all rides in the database.

    :param db: Database session
    :return: List of all rides in the database
    '''
    rides: List[Ride] = db.query(Ride).order_by(Ride.start_time.desc()).all()
    if not rides:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No rides found")
    return rides

def get_ride(db: Session, ride_id: int) -> Ride:
    '''
    Get a ride by its ID.

    :param ride_id: ID of the ride to retrieve
    :param db: Database session
    :return: Ride entry with the specified ID
    '''
    ride: Ride | None = db.query(Ride).filter(Ride.id == ride_id).first()
    if not ride:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Ride #{ride_id} not found")
    return ride

def update_ride(db: Session, ride_id: int, payload: RideCreate) -> Ride:
    '''
    Update a ride by its ID.

    :param ride_id: ID of the ride to update
    :param payload: A JSON schema containing the ride data. The schema must contain all the fields specified in the RideCreate schema.
    :param db: Database session
    :return: Updated Ride entry
    '''
    ride: Ride = get_ride(db=db, ride_id=ride_id)

    profile: Profile | None = db.query(Profile).filter(Profile.id == payload.user_id).first()
    if not profile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Profile #{payload.user_id} not found")

    # same fuel calcs as in create
    start_pct = getattr(payload, "start_fuel_pct", None)
    end_pct   = getattr(payload, "end_fuel_pct", None)
    actual_used = (start_pct - end_pct) * profile.tank_capacity_gallons
    expected_used = payload.distance / profile.epa_mpg
    saved = expected_used - actual_used

    score = compute_score(
        distance=payload.distance,
        avg_speed=payload.avg_speed,
        max_speed=payload.max_speed,
        avg_rpm=payload.avg_rpm,
        max_rpm=payload.max_rpm,
        duration=payload.duration,
    )

    db.query(Ride).filter(Ride.id == ride_id).update({
        **payload.dict(),
        "epa_mpg": profile.epa_mpg,
        "actual_used_gal": actual_used,
        "fuel_saved_gal": saved,
        "score": score,
    })
    db.commit()
    db.refresh(ride)
    return ride

def delete_ride(db: Session, ride_id: int) -> None:
    '''
    Delete a ride by its ID.

    :param ride_id: ID of the ride to delete
    :param db: Database session
    :return: None
    '''
    # Check if the ride exists
    ride: Ride = db.query(Ride).filter(Ride.id == ride_id).first()

    if not ride:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Ride #{ride_id} not found")

    # Delete the ride
    db.delete(ride)
    db.commit()