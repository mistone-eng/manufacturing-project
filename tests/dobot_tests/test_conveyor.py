from pydobotplus import auto_connect_dobot
import time

device = auto_connect_dobot()
print("[INFO] Connected to DOBOT")

# Try enabling STP2 motor at moderate speed
print("[TEST] Running conveyor on STP2 forward for 5s")
device.conveyor_belt(speed=0.5, direction=1, interface=0)
time.sleep(5)

# Stop it
print("[TEST] Stopping conveyor for 2s")
device.conveyor_belt(speed=0.0, direction=1, interface=0)
time.sleep(2)

# Reverse
print("[TEST] Running conveyor on STP2 backward for 5s")
device.conveyor_belt(speed=0.5, direction=-1, interface=0)
time.sleep(5)

# Stop finally
print("[TEST] Final stop")
device.conveyor_belt(speed=0.0, direction=1, interface=0)

device.close()
print("[INFO] Test complete.")
