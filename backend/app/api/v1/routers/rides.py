from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.db.crud import ride as ride_crud
from app.api.v1.schemas.ride import RideCreate, RideRead

router = APIRouter()

@router.post(path="/rides", response_model=RideRead, status_code=status.HTTP_201_CREATED)
def create_ride(payload: RideCreate, db: Session = Depends(get_db)) -> RideRead:
    '''
    Create a new ride entry in the database.
    This endpoint is used to create a new ride entry in the database. It takes a RideCreate schema as input and returns
    the created Ride entry.

    :param payload: A JSON schema containing the ride data. The schema must contain all the fields specified in the RideCreate schema.
    :return: Created Ride entry
    '''

    return ride_crud.create_ride(payload=payload, db=db)

@router.get(path="/rides", response_model=list[RideRead], status_code=status.HTTP_200_OK)
def list_rides(db: Session = Depends(get_db)) -> List[RideRead]:
    '''
    List all rides in the database. Use a GET request to retrieve all rides.

    :return: List of all rides in the database
    '''

    return ride_crud.list_rides(db=db)

@router.get(path="/rides/{ride_id}", response_model=RideRead, status_code=status.HTTP_200_OK)
def get_ride(ride_id: int, db: Session = Depends(get_db)) -> RideRead:
    '''
    Get a ride by its ID. Use a GET request to retrieve a ride by its ID.

    :param ride_id: ID of the ride to retrieve
    :return: Ride entry with the specified ID
    '''

    return ride_crud.get_ride(ride_id=ride_id, db=db)

@router.put(path="/rides/{ride_id}", response_model=RideRead, status_code=status.HTTP_200_OK)
def update_ride(ride_id: int, payload: RideCreate, db: Session = Depends(get_db)) -> RideRead:
    '''
    Update a ride by its ID. Use a PUT request to update a ride by its ID.

    :param ride_id: ID of the ride to update
    :param payload: A JSON schema containing the ride data. The schema must contain all the fields specified in the RideCreate schema.
    :return: Updated Ride entry
    '''

    return ride_crud.update_ride(ride_id=ride_id, payload=payload, db=db)

@router.delete(path="/rides/{ride_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_ride(ride_id: int, db: Session = Depends(get_db)) -> None:
    '''
    Delete a ride by its ID. Use a DELETE request to delete a ride by its ID.

    :param ride_id: ID of the ride to delete
    :return: None
    '''

    return ride_crud.delete_ride(ride_id=ride_id, db=db)