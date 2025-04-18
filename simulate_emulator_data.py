# simulate_emulator_data.py

import time
import serial

# Match the correct emulator port and baudrate
emulator_port = "/dev/ttys004"
ser = serial.Serial(emulator_port, 38400, timeout=1)

# Simulated trip data (customizable)
speed_values = [0, 20, 40, 60, 80, 100, 80, 60, 40, 20, 0]  # in km/h
rpm_values   = [700, 1000, 1500, 2000, 2500, 3000, 2500, 2000, 1500, 1000, 700]  # in RPM

# Send simulated data to emulator
for speed, rpm in zip(speed_values, rpm_values):
    speed_hex = format(speed, '02X')
    rpm_val = int(rpm * 4)
    rpm_hex = format(rpm_val, '04X')
    A, B = rpm_hex[:2], rpm_hex[2:]

    ser.write(f"edit 010D 7E8 03 41 0D {speed_hex}\n".encode())
    ser.write(f"edit 010C 7E8 04 41 0C {A} {B}\n".encode())

    print(f"[SENT] Speed: {speed} km/h | RPM: {rpm}")
    time.sleep(2)  # every 2 seconds

