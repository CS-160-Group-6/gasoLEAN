from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.api.v1.schemas.measurement import MeasurementRead
from app.db.session import get_db
from app.services.measurement_stream_service import MeasurementStreamService
from app.db.crud import measurement as measurement_crud

router = APIRouter()

@router.post(path="/measurements/{ride_id}/start", status_code=status.HTTP_202_ACCEPTED)
def start_trip(ride_id: int, interval: float = Query(1.0, gt=0.0,
                                                     description="Polling interval in seconds"),
                svc: MeasurementStreamService = Depends()) -> dict[str, Any]:
    '''
    Begin recording speed and RPM measurements for a specific ride, `ride_id`, at the given interval,
    `interval`.

    :param ride_id: ID of the ride to start
    :param interval: Polling interval in seconds (default is 1.0 second)
    :return: A dictionary containing the status of the start operation, ride_id, and interval.
    '''

    svc.start_stream(ride_id=ride_id, interval=interval)

    return {"status": "Started Trip", "ride_id": ride_id, "interval": interval}

@router.post(path="/measurements/{ride_id}/stop", status_code=status.HTTP_202_ACCEPTED)
def stop_trip(ride_id: int, svc: MeasurementStreamService = Depends()) -> dict[str, Any]:
    '''
    Stops the recording of speed and RPM measurements for a specific ride, `ride_id`.

    :param ride_id: ID of the ride to stop
    :return: A dictionary containing the status of the stop operation and the ride_id.
    '''

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