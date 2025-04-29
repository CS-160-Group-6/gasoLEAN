import time
import obd
from elm import Elm
from elm.interpreter import Edit

emulator = None
pty_path = None

def start_emulator():
    global emulator, pty_path
    emulator = Elm()
    emulator.set_defaults()
    emulator.threadState = emulator.THREAD.ACTIVE
    emulator.__enter__() # Start its internal PTY + interpreter

    # A small timeout if required
    timeout, interval, elapsed = 5.0, 0.1, 0.0
    pty_path = None
    while elapsed < timeout:
        pty_path = emulator.get_pty()
        if pty_path:
            break
        time.sleep(interval)
        elapsed += interval
    if not pty_path:
        raise RuntimeError("Unable to get PTY path from emulator")

    emulator.connect_serial()
    emulator.scenario = "car" # Set the scenario to 'car' for OBD-II emulation
    print(f"Emulator started on {pty_path}")

def stop_emulator():
    global emulator
    if emulator:
        emulator.__exit__(None, None, None)
        emulator = None
        print("Emulator stopped")

def run_simulation():
    global pty_path

    try:
        start_emulator()
        time.sleep(0.5)

        print(f"Connecting to emulator at {pty_path}")
        conn = obd.OBD(pty_path, fast=False)

				# Ensure connectivity
        while conn.status() != obd.OBDStatus.CAR_CONNECTED:
            time.sleep(0.05)

        # open both Edit contexts _around_ the queries
        with Edit(emulator, 'SPEED') as e_speed, \
             Edit(emulator, 'RPM')   as e_rpm:

            e_speed.answer(2, '3C', 'SPEED') # 60 kph
            # The RPM value must be multiplied by 4 due to the protocol's encoding requirements.
            e_rpm.answer(2, '1F40', 'RPM')

            speed_response = conn.query(obd.commands.SPEED)
            rpm_response   = conn.query(obd.commands.RPM)

            print(f"Queried SPEED: {speed_response.value}")
            print(f"Queried RPM: {rpm_response.value}")

    finally:
        stop_emulator()

if __name__ == "__main__":
    run_simulation()
