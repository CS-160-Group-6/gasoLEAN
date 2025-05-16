from typing import Any
from fastapi import Query, HTTPException, status
from fastapi.routing import APIRouter
import obd
import logging

from app.core.obd_integration import connect_to_obd as connect

router = APIRouter()

@router.get("/obd_connection", status_code=status.HTTP_200_OK)
def connect_to_obd(use_emulator: bool = Query(default=True), internal: bool = Query(default=False, include_in_schema=False)) -> Any:
    """
    Check the OBD-II connection status.
    If using the emulator, it will return the PTY path.
    If using a real OBD-II device, it will return the connection status.

    If called externally (internal=False), return a JSON summary.
    If called internally (internal=True via Depends), return raw obd.OBD.

    :param use_emulator: Boolean flag to use ELM327-emulator
    :return: obd.OBD connection object
    """
    conn: obd.OBD = connect(use_emulator=use_emulator)
    if not conn or not conn.is_connected():
        raise HTTPException(
            status_code=status.HTTP_428_PRECONDITION_REQUIRED,
            detail="Failed to connect to OBD-II device"
        )

    if internal:
        return conn  # Used for dependency injection
    else:
        logging.info(f"Connected to OBD-II on port: {conn.port_name()}")
        return {
            "status": "connected",
            "port": conn.port_name(),
            "using_emulator": use_emulator
        }