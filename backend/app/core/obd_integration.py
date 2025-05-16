import time, logging, obd
from fastapi import HTTPException, status
from elm import Elm
from app.vinner.decoder import decode_vin, VINDecoderError
from elm.interpreter import Edit

_emulator: Elm | None = None
_conn: obd.OBD | None = None
_pty_path: str | None = None

def connect_to_obd(use_emulator: bool = True) -> obd.OBD:
    global _emulator, _conn, _pty_path

    if use_emulator:
        if _emulator is None:
            logging.info("Starting ELM327-emulator…")
            _emulator = Elm()
            _emulator.set_defaults()
            _emulator.threadState = _emulator.THREAD.ACTIVE
            _emulator.__enter__()

            # wait for PTY
            timeout, interval, elapsed = 5.0, 0.1, 0.0
            while elapsed < timeout:
                _pty_path = _emulator.get_pty()

                if _pty_path:
                    break

                time.sleep(interval)
                elapsed += interval
            if not _pty_path:
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Could not get PTY path from emulator")

            _emulator.connect_serial()
            _emulator.scenario = "car"
            #checking vehicle info based on vin
            edit_values(emulator=_emulator, position=10,
                         new_value="35555857583743352A4241", field='VIN')
            logging.info("VIN overridden")
            print("THE VIN:", _emulator.edit_values)
            logging.info("ELM327-emulator running on %s", _pty_path)

        if _conn is None:
            logging.info("Opening python-OBD connection to %s", _pty_path)
            _conn = obd.OBD(_pty_path, fast=False)

            # Wait until OBD reports CAR_CONNECTED
            timeout, interval, elapsed = 5.0, 0.1, 0.0
            while _conn.status() != obd.OBDStatus.CAR_CONNECTED and elapsed < timeout:
                logging.info("Waiting for ELM327-emulator to report CAR_CONNECTED")
                elapsed += interval
                time.sleep(interval)

            if elapsed >= timeout:
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Timeout waiting for ELM327-emulator to report CAR_CONNECTED")

        return _conn

    else:
        if _conn is None:
            _conn = obd.OBD(fast=False, timeout=30)  # Auto-scan for a real port
        return _conn

def get_decoded_vehicle_info() -> dict:
    """
    Uses the active OBD connection (real or emulator) to retrieve and decode VIN.
    
    Returns:
        dict: Decoded vehicle details (Make, Model, Year, Type)

    Raises:
        HTTPException: If OBD or NHTSA decoding fails
    """
    try:
        conn = connect_to_obd(use_emulator=True)

        vin_cmd = obd.commands.VIN
        response = conn.query(vin_cmd)

        if response.is_null():
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="VIN retrieval failed from OBD"
            )

        vin = response.value
        logging.info(f"VIN retrieved from OBD: {vin}")

        try:
            vehicle_info = decode_vin(vin)
            logging.info(f"Vehicle info decoded: {vehicle_info}")
            return vehicle_info
        except VINDecoderError as e:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail=f"NHTSA decoding failed: {str(e)}"
            )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"VIN processing failed: {str(e)}"
        )

def edit_values(emulator: Elm, position:int, new_value: str,  field: str) -> bool:
    '''
    Edit the emulator's values for speed and RPM.
    
    :param emulator: The Elm emulator instance.
    :param position: The position in the data structure to edit.
    :param new_value: The new value to set (as a hex string).
    :param field: The field to edit ('SPEED' or 'RPM', etc.).
    '''
    edit_speed = Edit(emulator, pid=field)
    return edit_speed.answer(position=position, replace_bytes=new_value, pid=field)
