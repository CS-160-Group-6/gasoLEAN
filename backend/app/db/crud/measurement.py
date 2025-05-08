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