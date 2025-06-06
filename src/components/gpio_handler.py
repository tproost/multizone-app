import serial
import time
import threading
from typing import Dict, List, Optional
import streamlit as st


class GPIOHandler:
    def __init__(self, port: str = "COM3", baudrate: int = 9600):
        """Initialize GPIO handler for Arduino communication."""
        self.port = port
        self.baudrate = baudrate
        self.serial_conn: Optional[serial.Serial] = None
        self.is_connected = False
        self.zone_talker_status = [False, False, False, False]  # 4 zones
        self.processing_status = False
        self.read_thread = None
        self.running = False

    def connect(self) -> bool:
        """Connect to Arduino via Serial."""
        try:
            self.serial_conn = serial.Serial(self.port, self.baudrate, timeout=1)
            time.sleep(2)  # Wait for Arduino to initialize
            self.is_connected = True
            self.running = True
            self.start_reading()
            return True
        except Exception as e:
            st.error(f"Failed to connect to Arduino: {e}")
            return False

    def disconnect(self):
        """Disconnect from Arduino."""
        self.running = False
        if self.read_thread and self.read_thread.is_alive():
            self.read_thread.join(timeout=1)
        if self.serial_conn and self.serial_conn.is_open:
            self.serial_conn.close()
        self.is_connected = False

    def start_reading(self):
        """Start reading from Arduino in a separate thread."""
        if not self.read_thread or not self.read_thread.is_alive():
            self.read_thread = threading.Thread(
                target=self._read_from_arduino, daemon=True
            )
            self.read_thread.start()

    def _read_from_arduino(self):
        """Read GPIO status from Arduino continuously."""
        while self.running and self.is_connected:
            try:
                if self.serial_conn and self.serial_conn.in_waiting > 0:
                    line = self.serial_conn.readline().decode("utf-8").strip()
                    self._parse_arduino_data(line)
                time.sleep(0.1)  # Small delay to prevent excessive CPU usage
            except Exception as e:
                print(f"Error reading from Arduino: {e}")
                time.sleep(1)

    def _parse_arduino_data(self, data: str):
        """Parse incoming data from Arduino.
        Expected format: "TALKER:0,1,0,1" where 1=active, 0=inactive for each zone
        """
        try:
            if data.startswith("TALKER:"):
                status_str = data.replace("TALKER:", "")
                status_values = status_str.split(",")
                if len(status_values) == 4:
                    self.zone_talker_status = [bool(int(val)) for val in status_values]
        except Exception as e:
            print(f"Error parsing Arduino data: {e}")

    def send_processing_command(self, enable: bool):
        """Send processing on/off command to Arduino."""
        if not self.is_connected or not self.serial_conn:
            return False

        try:
            command = f"PROCESS:{'1' if enable else '0'}\n"
            self.serial_conn.write(command.encode("utf-8"))
            self.processing_status = enable
            return True
        except Exception as e:
            st.error(f"Failed to send command to Arduino: {e}")
            return False

    def get_zone_talker_status(self) -> List[bool]:
        """Get current talker status for all zones."""
        return self.zone_talker_status.copy()

    def get_processing_status(self) -> bool:
        """Get current processing status."""
        return self.processing_status


# Global GPIO handler instance
_gpio_handler = None


def get_gpio_handler() -> GPIOHandler:
    """Get or create the global GPIO handler instance."""
    global _gpio_handler
    if _gpio_handler is None:
        _gpio_handler = GPIOHandler()
    return _gpio_handler
