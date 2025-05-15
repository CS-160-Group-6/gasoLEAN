from typing import Any, Dict, Tuple
from fastapi import Depends, HTTPException, status
from sqlalchemy import Float
from sqlalchemy.orm import Session
import threading, time, logging
import obd
from datetime import datetime

from app.core.obd_integration import connect_to_obd
from app.db.crud.measurement import create_measurement, finalize_fuel_usage, list_measurements
from app.db.crud.ride import create_ride, update_distance, get_ride, update_ride
from app.db.crud.profile import get_profile
from app.db.session import get_db
from app.api.v1.schemas.measurement import MeasurementCreate
from app.api.v1.schemas.ride import RideCreate
from app.db.models import Measurement, Ride

class MeasurementStreamService:
    """
    Responsible for:
      1. Creating a new Ride
      2. Streaming OBD-II measurements (speed, RPM, fuel level)
      3. Storing them in the Measurement table
      4. On stop, computing total distance and fuel used, updating the Ride
    """

    # Maps ride_id → (thread, stop_event, initial_distance, start_time)
    _registry: Dict[int, Tuple[threading.Thread, threading.Event, float, datetime]] = {}

    def __init__(self, db: Session    = Depends(get_db), conn: obd.OBD = Depends(connect_to_obd)) -> None:
        self.db: Session = db
        self.conn: obd.OBD = conn
        self._initial_distance = 0.0

    def start_stream(self, user_id: int, interval: float = 1.0) -> int:
        """
        Creates a Ride record, captures initial distance,
        then begins recording measurements every `interval` seconds.
        Returns the new ride_id.

        :param user_id: ID of the user starting the ride
        :param interval: Time interval (in seconds) between measurements
        :return: The ID of the created Ride record
        """
        if (not self.conn.is_connected()):
            raise HTTPException(
                status_code=status.HTTP_428_PRECONDITION_REQUIRED,
                detail="OBD-II device is not connected"
            )

        if not get_profile(db=self.db, profile_id=user_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Profile #{user_id} not found"
            )

        init_fuel_pct: obd.OBDResponse | Any = self.conn.query(cmd=obd.commands.FUEL_LEVEL)
        if (init_fuel_pct.is_null()):
            raise HTTPException(
                status_code=status.HTTP_428_PRECONDITION_REQUIRED,
                detail="Car does not support fuel level querying."
            )

        now: datetime = datetime.utcnow()
        ride_payload = RideCreate(
            user_id=user_id,
            start_time=now,
            end_time=now,
            distance=0.0,
            avg_speed=0.0,
            max_speed=0.0,
            avg_rpm=0.0,
            max_rpm=0.0,
            duration=0,
            start_fuel_pct=init_fuel_pct.value.magnitude,
            end_fuel_pct=init_fuel_pct.value.magnitude
        )
        ride: Ride = create_ride(db=self.db, payload=ride_payload)
        ride_id = ride.id

        dist_resp: obd.OBDResponse | Any = self.conn.query(cmd=obd.commands.DISTANCE_SINCE_DTC_CLEAR)
        self._initial_distance = (dist_resp.value.magnitude
            if (not dist_resp.is_null())
            else 0.0
        )

        stop_evt = threading.Event()
        def _loop() -> None:
            while (not stop_evt.is_set()):
                speed_resp: obd.OBDResponse | Any = self.conn.query(cmd=obd.commands.SPEED)
                rpm_resp: obd.OBDResponse | Any   = self.conn.query(cmd=obd.commands.RPM)
                fuel_resp: obd.OBDResponse | Any  = self.conn.query(cmd=obd.commands.FUEL_LEVEL)

                if ((not speed_resp.is_null())
                    or (not rpm_resp.is_null())
                    or (not fuel_resp.is_null())):
                    meas = MeasurementCreate(
                        ride_id=ride_id,
                        speed=float(speed_resp.value.magnitude),
                        rpm=float(rpm_resp.value.magnitude),
                        fuel_level_pct=float(fuel_resp.value.magnitude),
                        timestamp=datetime.utcnow()
                    )
                    logging.info("Recording measurement: %s", meas)
                    create_measurement(self.db, meas)
                else:
                    logging.warning("Skipping null measurement for ride_id=%s", ride_id)

                time.sleep(interval)

        thread = threading.Thread(target=_loop, daemon=True)
        thread.start()
        # stash thread, stop_event, initial_distance, start_time
        self.__class__._registry[ride_id] = (thread, stop_evt,
                                             self._initial_distance,
                                             now)
        return ride_id

    def stop_stream(self, ride_id: int) -> None:
        """
        Stops the measurement loop for `ride_id`, computes total distance,
        updates timestamps, stats, and fuel usage on the Ride record.
        """
        if not get_ride(db=self.db, ride_id=ride_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Ride #{ride_id} not found in any active stream."
            )

        if (not self.conn.is_connected()):
            raise HTTPException(
                status_code=status.HTTP_428_PRECONDITION_REQUIRED,
                detail="OBD-II device is not connected"
            )

        try:
            entry: Tuple[threading.Thread | threading.Event | float | datetime] | None = self.__class__._registry.pop(ride_id, None)
        except KeyError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"No active stream for ride_id: {ride_id}")

        thread, stop_evt, initial_distance, start_time = entry
        stop_evt.set()
        thread.join()
        logging.info("Stopped streaming for ride_id=%s", ride_id)

        # Compute total distance via PID 31 displacement
        dist_resp: obd.OBDResponse | Any = self.conn.query(cmd=obd.commands.DISTANCE_SINCE_DTC_CLEAR)
        final_distance: Float | Any = (dist_resp.value.magnitude
            if (not dist_resp.is_null())
            else initial_distance
        )
        distance_traveled: Float = final_distance - initial_distance
        update_distance(db=self.db, ride_id=ride_id, distance=distance_traveled)

        # Fetch and update Ride timestamps & duration
        ride: Ride = get_ride(db=self.db, ride_id=ride_id)
        if (not ride):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Ride #{ride_id} not found in any active stream."
            )
        end_time: datetime = datetime.utcnow()
        ride.start_time = start_time
        ride.end_time = end_time
        ride.duration = int((end_time - start_time).total_seconds())

        # Compute speed & RPM stats
        measurements: list[Measurement] = list_measurements(ride_id=ride_id, db=self.db)
        if (not measurements):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No measurements for ride_id: {ride_id}, in any active stream."
            )
        speeds = [m.speed for m in measurements]
        rpms = [m.rpm for m in measurements]
        ride.avg_speed = sum(speeds) / len(speeds)
        ride.max_speed = max(speeds)
        ride.avg_rpm = sum(rpms) / len(rpms)
        ride.max_rpm = max(rpms)

        update_ride(db=self.db, ride_id=ride_id, ride=ride)

        # Finalize fuel usage (uses first & last measurements)
        start_pct = measurements[0].fuel_level_pct
        end_pct   = measurements[-1].fuel_level_pct
        finalize_fuel_usage(
            db=self.db,
            ride_id=ride_id,
            start_pct=start_pct,
            end_pct=end_pct
        )

        logging.info(
            "Ride #%s complete: %.2fmi, %ds, fuel %.2f%%→%.2f%%",
            ride_id,
            distance_traveled,
            ride.duration,
            start_pct,
            end_pct,
        )