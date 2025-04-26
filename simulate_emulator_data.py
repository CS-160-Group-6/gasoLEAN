import time
import serial  # Used to communicate with the ELM327 emulator over serial
from utils.logger import get_logger
import obd

logger = get_logger("simulator")
emulator_port = "/dev/pts/2"
baudrate = 38400

#idk whatt this is but necessary
ser = serial.Serial(emulator_port, baudrate, timeout=1)
conn = obd.OBD(emulator_port, baudrate, fast=False)

if not conn.is_connected():
    logger.error("Could not connect to OBD device.")
    exit()

time.sleep(2)  # Allow emulator to warm up and start feeding values

logger.info("Connected to OBD device.")
speed_query_cmd = obd.commands.SPEED
rpm_query_cmd = obd.commands.RPM

# === DRIVING PROFILE ===
# Realistic simulation of a staged trip: idle, acceleration, cruise, highway, deceleration
profile = [
    (0, 700), (0, 700), (0, 700),               # Idle
    (30, 1200), (30, 1200), (30, 1200),         # Acceleration
    (60, 1800), (60, 1800),                     # Cruising
    (90, 2600), (90, 2700), (90, 2800),         # Highway
    (60, 1800), (30, 1200), (0, 700)            # Deceleration to stop
]

logger.info("Starting OBD-II trip simulation\n")

i = 0
#MAIN LOOP
for speed, rpm in profile:
    # Convert speed to a 1-byte hex value for PID 010D
    speed_hex = format(speed, '02X')

    # Convert RPM to 2-byte hex value for PID 010C (actual RPM = ((A*256) + B) / 4)
    rpm_val = int(rpm * 4)
    rpm_hex = format(rpm_val, '04X')
    A = rpm_hex[:2]
    B = rpm_hex[2:]

    # Prepare ELM327 edit commands (use \r at end) CHECK THIS POSING EDIT COMMAND ERROR LOG ON EMULATOR CONSOLE BUT IT IS STILL WORKING FINE, I THINK WHEN WE PLUG IN REAL DEVICE EVERYTHING SHOULD WORK FINE.
    speed_cmd = f"edit SPEED 0x02 {speed_hex}\r"
    rpm_cmd = f"edit RPM 0x02 {A} {B}\r"

    # Send the commands to emulator (one at a time)
    ser.write(speed_cmd.encode('ascii'))
    ser.flush()
    time.sleep(0.1)

    ser.write(rpm_cmd.encode('ascii'))
    ser.flush()
    time.sleep(0.1)

    # loggong
    logger.info(f"[SENT] Speed: {speed} km/h | RPM: {rpm}")

    # Stimulate real-time update frequency
    time.sleep(2)

    speed_response = conn.query(speed_query_cmd)
    rpm_response = conn.query(rpm_query_cmd)

    speed = speed_response.value or "N/A"
    rpm = rpm_response.value or "N/A"

    logger.info(f"[Sample {i+1}] Speed: {speed}, RPM: {rpm}")

ser.close()

