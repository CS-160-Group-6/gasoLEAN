from fastapi import APIRouter
from app.core.obd_integration import get_decoded_vehicle_info

router = APIRouter()

@router.get("/vehicle/info")
def fetch_vehicle_info():
    return get_decoded_vehicle_info()

