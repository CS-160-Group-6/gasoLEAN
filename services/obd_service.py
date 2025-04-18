import obd
from config import settings

class OBDService:
    def __init__(self) -> None:
        self.connection = obd.OBD(settings.OBD_PORT)
        obd.logger.setLevel(obd.logging.DEBUG)
        obd.logger.info(f"Connecting to {settings.OBD_PORT} - Status: {self.connection.status()}")

    def is_car_connected(self):
        return self.connection.is_connected()

    def get_speed(self):
        response = self.connection.query(obd.commands.SPEED)
        return response.value if not response.is_null() else 0
    
    def get_rpm(self):
        response = self.connection.query(obd.commands.RPM)
        return response.value if not response.is_null() else 0



