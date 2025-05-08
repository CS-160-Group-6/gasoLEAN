import time, logging, obd
from elm import Elm

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
                raise RuntimeError("Could not get PTY path from emulator")

            _emulator.connect_serial()
            _emulator.scenario = "car"
            logging.info("ELM327-emulator running on %s", _pty_path)

        if _conn is None:
            logging.info("Opening python-OBD connection to %s", _pty_path)
            _conn = obd.OBD(_pty_path, fast=False)
            # wait until OBD reports CAR_CONNECTED
            while _conn.status() != obd.OBDStatus.CAR_CONNECTED:
                time.sleep(0.05)

        return _conn

    else:
        if _conn is None:
            _conn = obd.OBD(fast=False)  # auto-scan for a real port
        return _conn