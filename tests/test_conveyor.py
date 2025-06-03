import time
from pydobotplus import auto_connect_dobot

# --- Connect DOBOT ---
device = auto_connect_dobot()
print("[INFO] Connected to DOBOT.")

try:
    print("Starting converyor...")
    device.conveyor_belt(speed=0.5, direction=1)
    device.conveyor_belt_distance(speed_mm_per_sec=50, distance_mm=200, direction=1)
    time.sleep(2)
    
    # --- Stop ---
    print("[TEST] Stopping conveyor...")
    device.conveyor_belt(speed=0.0, interface=0)

finally:
    device.close()
    print("[INFO] Conveyor test complete. Device disconnected.")
