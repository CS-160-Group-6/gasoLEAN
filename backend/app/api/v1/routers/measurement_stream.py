from typing import Any
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.services.measurement_stream_service import MeasurementStreamService
from app.db.crud import measurement as measurement_crud
from app.api.v1.schemas.measurement import MeasurementRead
from app.db.session import get_db

router = APIRouter()

@router.post(path="/measurements/start", status_code=status.HTTP_202_ACCEPTED)
def start_trip(user_id: int = Query(gt=0),
    interval: float = Query(
        1.0,
        gt=0.0),
    svc: MeasurementStreamService = Depends()) -> Any:
    """
    Creates a Ride record for `user_id`, begins streaming OBD-II data,
    and returns the new ride_id along with the polling interval.

    :param user_id: ID of the user starting the ride
    :param interval: Time interval (in seconds) between measurements
    :param svc: MeasurementStreamService instance
    :return: A dictionary containing the status, ride_id, and interval.
    """
    ride_id = svc.start_stream(user_id=user_id, interval=interval)
    return {"status": "Started Trip", "ride_id": ride_id, "interval": interval}

@router.post(path="/measurements/{ride_id}/stop", status_code=status.HTTP_200_OK)
def stop_trip(ride_id: int, svc: MeasurementStreamService = Depends()) -> Any:
    """
    Stops the measurement loop for `ride_id`, computes all final metrics
    (distance, duration, speed/RPM stats, fuel usage), and updates the Ride.

    :param ride_id: ID of the ride to stop
    :param svc: MeasurementStreamService instance
    :return: A dictionary containing the status and ride_id.
    """
    svc.stop_stream(ride_id=ride_id)
    return {"status": "Stopped Trip", "ride_id": ride_id}

@router.get(path="/rides/{ride_id}/measurements", response_model=list[MeasurementRead], status_code=status.HTTP_200_OK)
def list_measurements_for_ride(ride_id: int, db: Session = Depends(get_db)) -> list[MeasurementRead]:
    '''
    List all measurements for a specific ride, `ride_id`.

    :param ride_id: ID of the ride to list measurements for
    :return: A list of measurements for the specified ride.
    '''

    return measurement_crud.list_measurements(ride_id=ride_id, db=db)