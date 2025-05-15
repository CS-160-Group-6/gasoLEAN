from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.db.models import Measurement, Ride
from app.api.v1.schemas.measurement import MeasurementCreate

def create_measurement(db: Session, m: MeasurementCreate) -> Measurement:
    '''
    Create a new measurement in the database.
    This function takes a MeasurementCreate object as input and creates a new measurement in the database.
    It returns the created measurement object.
    '''
    db_obj: Measurement = Measurement(**m.dict())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def list_measurements(ride_id: int, db: Session) -> list[Measurement]:
    '''
    List all measurements for a specific ride, `ride_id`.
    This function takes a ride ID as input and returns a list of measurements associated with that ride.

    :param ride_id: ID of the ride to get measurements of
    :param db: SQLAlchemy session object
    :return: A list of measurements for the specified ride
    '''
    meas: Measurement | None = db.query(Measurement).filter(Measurement.ride_id == ride_id).order_by(Measurement.timestamp).all()

    if not meas:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No measurements found for ride ID: #{ride_id}.')

    return meas

def finalize_fuel_usage(db: Session, ride_id: int, start_pct: float, end_pct: float) -> Ride:
    '''
    Finalize the fuel usage for a ride.

    :param db: SQLAlchemy session object
    :param ride_id: ID of the ride to finalize
    :param start_pct: Starting fuel level percentage
    :param end_pct: Ending fuel level percentage

    :return: The updated ride object with actual_used_gal and fuel_saved_gal calculated
    '''
    ride = db.query(Ride).get(ride_id)
    if not ride:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Rdie #{ride_id} not found')

    baseline_mpg = ride.distance / ride.epa_mpg

    frac_used: float = (start_pct - end_pct) / 100.0
    ride.actual_used_gal = baseline_mpg * frac_used
    ride.fuel_saved_gal = baseline_mpg - ride.actual_used_gal

    db.commit()
    db.refresh(ride)
    return ride