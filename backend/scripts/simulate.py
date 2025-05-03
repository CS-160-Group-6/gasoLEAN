import time
import obd
import logging
from elm import Elm
from elm.interpreter import Edit

emulator = None
pty_path = None

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')

def start_emulator():
    '''Sets up and starts the emulator'''
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
    logging.info(f"Emulator started on {pty_path}")
    
def edit_values(emulator: Elm, position:int, new_value: str,  field: str) -> bool:
    '''
    Edit the emulator's values for speed and RPM.
    
    :param emulator: The Elm emulator instance.
    :param position: The position in the data structure to edit.
    :param new_value: The new value to set (as a hex string).
    :param field: The field to edit ('SPEED' or 'RPM', etc.).
    '''
    edit_speed = Edit(emulator, pid=field)
    return edit_speed.answer(position=position, replace_bytes=new_value, pid=field)

def stop_emulator():
    '''Stops the emulator'''
    global emulator
    if emulator:
        emulator.terminate()
        emulator = None
        logging.info("Emulator stopped")

def run_simulation():
    global pty_path

    try:
        start_emulator()
        time.sleep(0.5)

        logging.info(f"Connecting to emulator at {pty_path}")
        conn = obd.OBD(pty_path, fast=False)

		# Ensure connectivity
        while conn.status() != obd.OBDStatus.CAR_CONNECTED:
            time.sleep(0.05)
        
        fields_to_change = ['SPEED', 'RPM']
        values_to_change = ['3C', '1F40']  # Hexadecimal values for 60 kph and 2000 RPM
        position = 2  # Position in the data structure to edit
        
        for field, new_value in zip(fields_to_change, values_to_change):
            logging.info(f"Editing {field} at position {position} to {new_value}")
            
            if edit_values(emulator, position, new_value, field):
                logging.info(f"Edited {field} at position {position} to {new_value}")
            else:
                logging.error(f"Failed to edit {field} at position {position} to {new_value}")
                stop_emulator()
        
        speed_response = conn.query(obd.commands.SPEED)
        rpm_response = conn.query(obd.commands.RPM)
        
        if speed_response.is_null() or rpm_response.is_null():
            logging.error("Failed to retrieve speed or RPM from the emulator")
            stop_emulator()
        else:
            logging.info(f"Speed: {speed_response.value}, RPM: {rpm_response.value}")
        
    finally:
        stop_emulator()

if __name__ == "__main__":
    run_simulation()
