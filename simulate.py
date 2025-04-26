import time
import threading
import obd
from elm import Elm
from elm.interpreter import Edit, Interpreter

class EmulatorController:
    def __init__(self):
        self.emulator = None
        self.pty_path = None
        self.interpreter_thread = None

    def start_emulator(self):
        self.emulator = Elm()
        self.emulator.set_defaults()
        self.emulator.threadState = self.emulator.THREAD.ACTIVE
        time.sleep(1)
        self.pty_path = self.emulator.get_pty()
        self.emulator.connect_serial()
        self.emulator.scenario = 'car'

        def emulator_backend():
            interpreter = Interpreter(self.emulator, args=type('', (), {'batch_mode': False})())
            
            while True:
                try:
                    if self.emulator.serial_port:
                        cmd = self.emulator.serial_port.readline()
                        if cmd:
                            cmd_str = cmd.decode('utf-8', errors='ignore').strip()
                            interpreter.default(cmd_str)
                    time.sleep(0.01)
                except Exception as e:
                    print(f"Error in emulator backend: {e}")
                    break

        self.interpreter_thread = threading.Thread(target=emulator_backend, daemon=True)
        self.interpreter_thread.start()

        print(f"Emulator started on {self.pty_path}")

    def stop_emulator(self):
        if self.emulator:
            self.emulator.terminate()
            print("Emulator stopped")

    def edit_pid(self, pid, position, replace_bytes):
        with Edit(self.emulator, pid) as edit:
            success = edit.answer(position, replace_bytes)
            if success:
                print(f"Edited PID {pid} successfully")
            else:
                print(f"Failed to edit PID {pid}")

def run_simulation():
    controller = EmulatorController()

    try:
        controller.start_emulator()

        time.sleep(2)

        controller.edit_pid('SPEED', 2, '3C')  # 60 km/h
        controller.edit_pid('RPM', 2, '07D0')  # 2000

        print(f"Connecting to emulator at {controller.pty_path}...")
        connection = obd.OBD(controller.pty_path, fast=False)

        speed_response = connection.query(obd.commands.SPEED)
        rpm_response = connection.query(obd.commands.RPM)

        print(f"Queried SPEED: {speed_response.value}")
        print(f"Queried RPM: {rpm_response.value}")

    finally:
        controller.stop_emulator()

if __name__ == "__main__":
    run_simulation()
