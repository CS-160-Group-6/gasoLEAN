from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.db.models import Vehicle
from app.api.v1.schemas.vehicle import VehicleCreate


def get_vehicle_by_vin(db: Session, vin: str) -> Vehicle | None:
    """
    Retrieve a vehicle from the database using its VIN.

    :param db: Database session
    :param vin: VIN string to search
    :return: Vehicle record or None if not found
    """
    return db.query(Vehicle).filter(Vehicle.vin == vin).first()


def create_vehicle(db: Session, payload: VehicleCreate) -> Vehicle:
    """
    Insert a new decoded vehicle record into the database.

    :param db: Database session
    :param payload: VehicleCreate schema with decoded VIN info
    :return: Created Vehicle object
    """
    existing = get_vehicle_by_vin(db, payload.vin)
    if existing:
        return existing  # Prevent duplicate VINs

    vehicle = Vehicle(**payload.dict())
    db.add(vehicle)
    db.commit()
    db.refresh(vehicle)
    return vehicle


def list_vehicles(db: Session) -> list[Vehicle]:
    """
    List all stored vehicle records.

    :param db: Database session
    :return: List of Vehicle objects
    """
    vehicles = db.query(Vehicle).order_by(Vehicle.id.desc()).all()
    if not vehicles:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No vehicles found")
    return vehicles


def delete_vehicle_by_vin(db: Session, vin: str) -> None:
    """
    Delete a vehicle entry from the database by VIN.

    :param db: Database session
    :param vin: VIN of the vehicle to delete
    :return: None
    """
    vehicle: Vehicle | None = get_vehicle_by_vin(db, vin)
    if not vehicle:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Vehicle with VIN {vin} not found"
        )

    db.delete(vehicle)
    db.commit()
