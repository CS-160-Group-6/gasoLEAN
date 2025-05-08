from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status, Query

from app.services.measurement_stream_service import MeasurementStreamService

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
    try:
        svc.start_stream(ride_id=ride_id, interval=interval)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=str(e))

    return {"status": "Started Trip", "ride_id": ride_id, "interval": interval}

@router.post("/measurements/{ride_id}/stop", status_code=status.HTTP_202_ACCEPTED)
def stop_trip(ride_id: int, svc: MeasurementStreamService = Depends()) -> dict[str, Any]:
    '''
    Stops the recording of speed and RPM measurements for a specific ride, `ride_id`.

    :param ride_id: ID of the ride to stop
    :return: A dictionary containing the status of the stop operation and the ride_id.
    '''
    try:
        svc.stop_stream(ride_id=ride_id)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=str(e))

    return {"status": "Stopped Trip", "ride_id": ride_id}