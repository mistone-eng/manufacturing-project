import time
from external.pydobotplus import auto_connect_dobot
import struct

# Connect to DOBOT
device = auto_connect_dobot()
print("[INFO] Connected to DOBOT.")

# Ports used
COLOR_PORT = device.PORT_GP2
IR_PORT = device.PORT_GP4

def read_color_sensor(version):
    try:
        device.set_color(enable=True, port=COLOR_PORT, version=version)
        response = device.get_color(port=COLOR_PORT, version=version)

        # Read raw byte values
        r = struct.unpack_from('B', response.params, 0)[0]
        g = struct.unpack_from('B', response.params, 1)[0]
        b = struct.unpack_from('B', response.params, 2)[0]
        print(f"[COLOR V{version}] R: {r}, G: {g}, B: {b}")
    except Exception as e:
        print(f"[ERROR] Color Sensor V{version}: {e}")

def read_ir_sensor():
    try:
        state = device.get_ir(port=IR_PORT)
        print(f"[IR SENSOR] Detected: {bool(state)} (Raw: {state})")
    except Exception as e:
        print(f"[ERROR] IR Sensor: {e}")

print("[INFO] Starting sensor debug loop. Press Ctrl+C to stop.")

try:
    while True:
        read_color_sensor(version=0x0)
        read_color_sensor(version=0x1)
        read_ir_sensor()
        print("-" * 40)
        time.sleep(1)

except KeyboardInterrupt:
    print("\n[INFO] Exiting sensor debug program.")

finally:
    device.close()
    print("[INFO] Disconnected from DOBOT.")
