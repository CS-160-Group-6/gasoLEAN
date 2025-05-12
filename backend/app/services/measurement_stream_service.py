from typing import Dict, Tuple
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
import threading, time, logging
import obd

from app.core.obd_integration import connect_to_obd
from app.db.crud.measurement import create_measurement, finalize_fuel_usage, list_measurements
from app.db.crud.ride import get_ride
from app.db.models import Measurement
from app.db.session import get_db
from app.api.v1.schemas.measurement import MeasurementCreate

class MeasurementStreamService:
    """
    MeasurementStreamService is responsible for streaming measurements from the OBD-II device.
    It handles the connection to the OBD-II device, retrieves measurements, and stores them in the database.
    """

    _registry: Dict[int, Tuple[threading.Thread, threading.Event]] = {}
    def __init__(self, db: Session = Depends(get_db), conn: obd.OBD = Depends(connect_to_obd)) -> None:
        self.db: Session = db
        self.conn: obd.OBD = conn

    def start_stream(self, ride_id: int, interval: float = 1.0) -> None:
        '''
        Start streaming measurements from the OBD-II device every `interval` seconds and storing them under `ride_id`.

        :param ride_id: ID of the ride to associate with the measurements
        :param interval: Time interval in seconds between measurements
        '''

        # Check if the OBD-II device is connected
        if not self.conn.is_connected():
            raise HTTPException(status_code=status.HTTP_428_PRECONDITION_REQUIRED, detail="OBD-II device is not connected")

        # Check if the ride ID is already being streamed
        elif ride_id in self.__class__._registry:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Stream already running for this ride ID: #{ride_id}")

        # Check if the ride ID exists in the database
        # The function get_ride() will raise an HTTPException if the ride ID does not exist
        get_ride(ride_id=ride_id, db=self.db)

        stop_evt: threading.Event = threading.Event()

        def _loop():
            while not stop_evt.is_set():
                # Get measurements from OBD-II device
                speed: obd.OBDResponse = self.conn.query(cmd=obd.commands.SPEED)
                rpm: obd.OBDResponse = self.conn.query(cmd=obd.commands.RPM)
                fuel_pct: obd.OBDResponse = self.conn.query(cmd=obd.commands.FUEL_LEVEL)

                # Check if we received both speed and RPM
                if not speed.is_null() or not rpm.is_null() or not fuel_pct.is_null():
                    record = {
                        "ride_id": ride_id,
                        "speed": float(speed.value.magnitude),
                        "rpm": float(rpm.value.magnitude),
                        "fuel_level_pct": float(fuel_pct.value.magnitude)
                    }

                    logging.info("Recorded measurement: %s", record)

                    payload = MeasurementCreate(**record)
                    create_measurement(self.db, payload)
                else:
                    logging.warning("Skipping measurement: speed or RPM is null for ride ID %s", ride_id)

                time.sleep(interval)

        thread = threading.Thread(target=_loop, daemon=True)
        self.__class__._registry[ride_id] = (thread, stop_evt)
        thread.start()
        logging.info("Started streaming measurements for ride ID %s every %.1fs", ride_id, interval)

    def stop_stream(self, ride_id: int):
        '''
        Stop streaming measurements for the given ride ID, `ride_id`.

        :param ride_id: ID of the ride to stop streaming measurements for
        '''
        try:
            detail: Tuple[threading.Thread, threading.Event] = self.__class__._registry.pop(ride_id, None)
        except KeyError:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"No active stream found for ride_id: {ride_id}")

        thread: threading.Thread = detail[0]
        stop_evt: threading.Event = detail[1]

        stop_evt.set()
        thread.join()
        logging.info("Stopped streaming measurements for ride ID %s", ride_id)

        measurements: list[Measurement] = list_measurements(ride_id=ride_id, db=self.db)

        start_pct: float = measurements[0].fuel_level_pct
        end_pct: float = measurements[-1].fuel_level_pct
        logging.info("Finalizing fuel usage for ride ID %s: start_pct=%.2f, end_pct=%.2f", ride_id, start_pct, end_pct)

        finalize_fuel_usage(db=self.db, ride_id=ride_id, start_pct=start_pct, end_pct=end_pct)
        logging.info("Finalized fuel usage for ride ID %s", ride_id)