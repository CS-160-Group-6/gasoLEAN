# from services.obd_service import *
# from models.trip_data import TripData
# from utils.logger import get_logger

import services
import models
import utils
import obd as OBD

log = utils.logger.get_logger('obd_backend')

def main():
    obd = services.OBDService()
    OBD.logger.setLevel(OBD.logging.INFO)
    if not obd.is_car_connected():
        OBD.logger.info(f"Failed to connect to OBD device.")
        return

    trip = models.trip_data.TripData()

    OBD.logger.info(f"Collecting data ...")
    for _ in range(5):
        trip.record_sample(obd.get_speed(), obd.get_rpm())
       
    OBD.logger.info(trip.rpms)
    OBD.logger.info(trip.speeds)
    # TODO: Call the scorer and give the score

if __name__ == "__main__":
    main()
