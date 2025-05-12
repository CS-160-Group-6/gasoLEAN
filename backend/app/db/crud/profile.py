from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.db.models import Profile
from app.api.v1.schemas.profile import ProfileCreate

def create_profile(db: Session, payload: ProfileCreate) -> Profile:
    """
    Insert a new Profile row.
    This endpoint is used to create a new profile entry in
    the database. It takes a ProfileCreate schema as input
    and returns the created Profile entry.

    :param payload: A JSON schema containing the profile data.
    The schema must contain all the fields specified in the
    ProfileCreate schema.
    :return: Created Profile entry
    """
    profile = Profile(**payload.dict())
    db.add(profile)
    db.commit()
    db.refresh(profile)
    return profile

def get_profile(db: Session, profile_id: int) -> Profile:
    """
    Fetch one Profile by ID.

    :param db: Database session
    :param profile_id: ID of the profile to fetch
    :return: Profile entry
    """
    profile: Profile | None = db.query(Profile).filter(Profile.id == profile_id).first()
    if not profile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Profile #{profile_id} not found")
    return profile

def list_profiles(db: Session) -> list[Profile]:
    """
    Fetch all profiles.

    :param db: Database session
    :return: List of all profiles in the database
    """
    return db.query(Profile).order_by(Profile.id).all()

def update_profile(db: Session, profile_id: int, payload: ProfileCreate) -> Profile:
    """
    Update an existing Profile.

    :param db: Database session
    :param profile_id: ID of the profile to update
    :param payload: A JSON schema containing the updated
    profile data. The schema must contain all the fields specified in the ProfileCreate schema.
    :return: Updated Profile entry
    """
    profile: Profile = get_profile(db=db, profile_id=profile_id)
    for field, value in payload.dict().items():
        setattr(profile, field, value)

    db.commit()
    db.refresh(profile)
    return profile

def delete_profile(db: Session, profile_id: int) -> None:
    """
    Delete a Profile row.

    :param db: Database session
    :param profile_id: ID of the profile to delete
    :return: None
    """
    profile: Profile = get_profile(db=db, profile_id=profile_id)

    if not profile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Profile #{profile_id} not found")

    db.delete(profile)
    db.commit()
