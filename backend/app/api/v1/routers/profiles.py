from typing import List
from fastapi import APIRouter, Depends, status

from sqlalchemy.orm import Session
from app.db.session import get_db
from app.api.v1.schemas.profile import ProfileCreate, ProfileRead
import app.db.crud.profile as crud

router = APIRouter()

@router.post(path="/profiles", response_model=ProfileRead, status_code=status.HTTP_201_CREATED)
def create_profile( payload: ProfileCreate, db: Session = Depends(get_db)) -> ProfileRead:
    """
    Create a new user profile. This endpoint is used to create a new profile entry in
    the database. It takes a ProfileCreate schema as input and returns the created
    Profile entry.

    :param payload: A JSON schema containing the profile data. The schema must contain
    all the fields specified in the ProfileCreate schema.
    :param db: Database session
    :return: Created Profile entry
    """
    return crud.create_profile(db=db, payload=payload)

@router.get(path="/profiles", response_model=List[ProfileRead], status_code=status.HTTP_200_OK)
def list_profiles(db: Session = Depends(get_db)) -> List[ProfileRead]:
    """
    List all profiles.
    This endpoint is used to list all profiles in the database.
    It returns a list of all profiles in the database.

    :param db: Database session
    :return: List of all profiles in the database
    """
    return crud.list_profiles(db=db)

@router.get(path="/profiles/{profile_id}", response_model=ProfileRead, status_code=status.HTTP_200_OK)
def get_profile(profile_id: int, db: Session = Depends(get_db)) -> ProfileRead:
    """
    Get a single profile.
    This endpoint is used to fetch a single profile by its ID.
    It returns the profile entry.

    :param profile_id: ID of the profile to fetch
    :param db: Database session
    :return: Profile entry
    """
    return crud.get_profile(db=db, profile_id=profile_id)

@router.put(path="/profiles/{profile_id}", response_model=ProfileRead, status_code=status.HTTP_200_OK)
def update_profile(profile_id: int, payload: ProfileCreate, db: Session = Depends(get_db)) -> ProfileRead:
    """
    Update an existing profile.
    This endpoint is used to update an existing profile entry in the database.
    It takes a ProfileCreate schema as input and returns the updated Profile entry.

    :param profile_id: ID of the profile to update
    :param payload: A JSON schema containing the updated profile data.
    The schema must contain all the fields specified in the ProfileCreate schema.
    :param db: Database session
    :return: Updated Profile entry
    """
    return crud.update_profile(db=db, profile_id=profile_id, payload=payload)

@router.delete(path="/profiles/{profile_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_profile(profile_id: int, db: Session = Depends(get_db)) -> None:
    """
    Delete a profile.
    This endpoint is used to delete a profile entry from the database.
    It takes the profile ID as input and deletes the profile entry.

    :param profile_id: ID of the profile to delete
    :param db: Database session
    :return: None
    """
    crud.delete_profile(db=db, profile_id=profile_id)