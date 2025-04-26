
import time
import json
from typing import List, Dict

def send_to_emulator(pty_path: str, cmd: str):
    """Send a command to the ELM327 emulator via PTY."""
    with open(pty_path, "w") as f:
        f.write(cmd + "\n")

def format_speed(speed_kph: int) -> str:
    """Convert speed in km/h to hex format (1 byte)."""
    return f"{speed_kph:02X}"

def format_rpm(rpm_value: int) -> str:
    """Convert RPM to two-byte hex format (A * 256 + B)."""
    a = rpm_value // 256
    b = rpm_value % 256
    return f"{a:02X} {b:02X}"

def simulate_trip(pty_path: str, trip_profile: List[Dict[str, int]], interval: float = 5.0):
    """
    Emulate a driving trip by setting speed and rpm values at intervals.

    Args:
        pty_path: Path to the emulator's PTY (e.g., /dev/pts/3).
        trip_profile: List of dicts, each with 'speed' and 'rpm' keys.
        interval: Time in seconds to wait between each profile entry.
    """
    for i, step in enumerate(trip_profile):
        speed = step.get("speed", 0)
        rpm = step.get("rpm", 0)

        hex_speed = format_speed(speed)
        hex_rpm = format_rpm(rpm)

        print(f"[{i+1}] Setting speed={speed} km/h, rpm={rpm}")
        send_to_emulator(pty_path, f"edit SPEED 0x00 {hex_speed}")
        send_to_emulator(pty_path, f"edit RPM 0x00 {hex_rpm}")

        time.sleep(interval)

def load_trip_from_json(path: str) -> List[Dict[str, int]]:
    """Load a trip profile from a JSON file."""
    with open(path, "r") as f:
        return json.load(f)

if __name__ == "__main__":
    # Example static trip (can be replaced by loading from JSON)
    trip = [
        {"speed": 0, "rpm": 0},
        {"speed": 20, "rpm": 1000},
        {"speed": 40, "rpm": 1800},
        {"speed": 60, "rpm": 2200},
        {"speed": 45, "rpm": 1700},
        {"speed": 25, "rpm": 1100},
        {"speed": 0, "rpm": 0},
    ]

    emulate_pty = "/dev/pts/2"  # <-- replace with actual PTY from emulator output
    simulate_trip(emulate_pty, trip, interval=5.0)
