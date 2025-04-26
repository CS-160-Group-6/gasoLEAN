import obd
import time
from config import settings

# Logger setup
obd.logging.basicConfig(
    level=obd.logging.INFO,
    format='[%(asctime)s] %(levelname)s - %(message)s',
    datefmt='%H:%M:%S'
)

def run_test():
    obd.logging.info("Connecting to OBD device...")

    connection = obd.OBD(portstr=settings.OBD_PORT, baudrate=38400, fast=False)

    if not connection.is_connected():
        obd.logging.error("Could not connect to OBD device.")
        return

    obd.logging.info("Connected to OBD device.")
    obd.logging.info("Collecting 10 samples from emulator...")

    speed_cmd = obd.commands.SPEED
    rpm_cmd = obd.commands.RPM
    data = []

    for i in range(10):
        timestamp = time.time()

        # Query values
        speed_response = connection.query(speed_cmd)
        rpm_response = connection.query(rpm_cmd)

        speed = speed_response.value or "N/A"
        rpm = rpm_response.value or "N/A"

        # Retry once if value is None
        if speed == "N/A":
            time.sleep(1)
            speed = connection.query(speed_cmd).value or "N/A"
        if rpm == "N/A":
            time.sleep(1)
            rpm = connection.query(rpm_cmd).value or "N/A"

        obd.logging.info(f"[Sample {i+1}] Speed: {speed}, RPM: {rpm}")

        data.append({
            "timestamp": timestamp,
            "speed": str(speed),
            "rpm": str(rpm)
        })

        time.sleep(2)

    obd.logging.info("Data collection complete.\n")

    print("--- Final Trip Data ---")
    for entry in data:
        print(f"{time.strftime('%H:%M:%S', time.localtime(entry['timestamp']))} | Speed: {entry['speed']:<10} | RPM: {entry['rpm']}")

if __name__ == "__main__":
    run_test()

