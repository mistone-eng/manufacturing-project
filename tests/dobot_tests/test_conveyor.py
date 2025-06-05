import time
import sys
from external.pydobotplus import auto_connect_dobot

# --- Connect DOBOT ---
device = auto_connect_dobot()

try:
    # --- Optional: Reset/initialize state ---
    device.speed(velocity=100, acceleration=100)
    device.home()
    print("[INFO] Homed and ready.")

    # --- Run conveyor forward (STP2) ---
    print("\n[TEST] Running conveyor forward (STP2)...")
    device.conveyor_belt(speed=0.5, direction=1, interface=0)
    time.sleep(5)

    # --- Stop ---
    print("[TEST] Stopping conveyor...")
    device.conveyor_belt(speed=0.0, interface=0)
    time.sleep(2)

    # --- Run conveyor backward (STP2) ---
    print("[TEST] Running conveyor backward (STP2)...")
    device.conveyor_belt(speed=0.5, direction=-1, interface=0)
    time.sleep(5)

    # --- Stop ---
    print("[TEST] Stopping conveyor...")
    device.conveyor_belt(speed=0.0, interface=0)

finally:
    device.close()
    print("[INFO] Conveyor test complete. Device disconnected.")
