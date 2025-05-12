from sqlalchemy.orm import Session
from app.db.models import Measurement
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
    return db.query(Measurement).filter(Measurement.ride_id == ride_id).order_by(Measurement.timestamp).all()