from rtde_control import RTDEControlInterface as RTDEControl
from rtde_receive import RTDEReceiveInterface as RTDEReceive
import os
import psutil
import time
import ctypes
import GoSdk_MsgHandler
from Gocator import GoSdk, kApi, RecieveData, get_measurement_decision, kObject_Destroy, kIpAddress,  GoDataSet, GoDataMsg, kNULL
import epick_gripper as gripper
import camera as cam

# Set environment variables to limit thread usage
os.environ["OPENBLAS_NUM_THREADS"] = "1"

# Parameters
vel = 0.5  
acc = 0.5 
rtde_frequency = 500
ur_cap_port = 50002
robot_ip = "192.168.1.5"
scanner_ip = b"192.168.1.10" 
RECEIVE_TIMEOUT = 10000

# Home positions
scanning_pose =  [0.18460770962661585, -0.4198238765759319, 0.2576206095505704, -0.5978738392574462, 3.075728673810618, -0.018057268513576502]
default_pick_pose = [0.15567489275284674, -0.35162644504319374, 0.06095980226567002, -0.6893993925036952, 3.040759202994412, -0.011438164988687225]
place_station_1 = [0.15963730635112894, -0.3456811802676046, 0.21723580955386407, -0.6377238906506748, 3.0132023314691896, -0.02128345945811506]
place_station_2 = [-0.0206788728166898, -0.6761322298817805, 0.18534997433085124, 0.4231507248294163, 3.073900294001708, -0.03824977839387938]
default_place_pose = [-0.015024415995209551, -0.7056774883003915, 0.06581146968886833, 0.4186433764466406, 3.111196418160659, -0.023448896225652473]

process = psutil.Process(os.getpid())
# Set application high priority
try:
    process.nice(-10)
except psutil.AccessDenied:
    print("[WARNING] Insufficient permissions to set high priority. Running with normal priority.")
    process.nice(0)
# process.nice(psutil.HIGH_PRIORITY_CLASS) for Windows

# Connect to UR5e
print("Connecting to UR5e...")
rtde_r = RTDEReceive(robot_ip, rtde_frequency)
rtde_c = RTDEControl(robot_ip, rtde_frequency, RTDEControl.FLAG_VERBOSE | RTDEControl.FLAG_UPLOAD_SCRIPT) #ur_cap_port


#Live camera feed
#cam.camera_feed()

while True:
    try:
        # Move UR5e to home position before scanning
        print(20*"*")
        print(f"Moving UR5e to scanning position : {scanning_pose}")
        rtde_c.moveL(scanning_pose, vel, acc)
        #data_collector.collect_data(OperationLabels.MOVING_TO_SCAN)
        time.sleep(1)
        
        # Initialize scanner
        api = ctypes.c_void_p()
        system = ctypes.c_void_p()
        sensor = ctypes.c_void_p()
        dataset = GoDataSet()   
        dataObj = GoDataMsg()
        
        # Initialize SDK
        GoSdk.GoSdk_Construct(ctypes.byref(api))
        GoSdk.GoSystem_Construct(ctypes.byref(system), None)
        
        # Connect to sensor
        ipAddr_ref = kIpAddress()
        kApi.kIpAddress_Parse(ctypes.byref(ipAddr_ref), scanner_ip)
        GoSdk.GoSystem_FindSensorByIpAddress(system, ctypes.byref(ipAddr_ref), ctypes.byref(sensor))
        GoSdk.GoSensor_Connect(sensor)
        GoSdk.GoSystem_EnableData(system, True)
        
        Mgr = GoSdk_MsgHandler.MsgManager(GoSdk, system, dataset)
        Mgr.SetDataHandler(RECEIVE_TIMEOUT, RecieveData)

        # Start scanning
        print(20*"*")
        print("Scanning the object...")
        print()
        GoSdk.GoSensor_Stop(sensor)
        GoSdk.GoSensor_Snapshot(sensor)
        time.sleep(1)
        print("Scan Completed!")
        print()

        #Get Measurement Decision
        measurement_decision = get_measurement_decision()
        
        # Disconnect scanner
        Mgr.SetDataHandler(RECEIVE_TIMEOUT, kNULL)
        Mgr.thread.join()

        kObject_Destroy(system)
        kObject_Destroy(api)

        if measurement_decision != 1:   #fault object
            print("Fault object detected ! Placing it away...")
            print()
            
            # Move to pick position
            print(20*"*")
            print(f"Moving to pick position : {default_pick_pose}")
            rtde_c.moveL(default_pick_pose, vel, acc)
            time.sleep(1)
            print("Picking Object...")
            gripper.start_suction()

            # Move to place position
            print(f"Moving to place position : {default_place_pose}")
            
            rtde_c.moveL(place_station_1, vel, acc)
            rtde_c.moveL(place_station_2, vel, acc)

            rtde_c.moveL(default_place_pose, vel, acc)
            print("Dropping object...")
            gripper.stop_suction()
            time.sleep(1)
            
        else:
            print("Detected object is acceptable !")
            time.sleep(1)

    except KeyboardInterrupt:
        print("Control Interrupted! Stopping loop.")
        rtde_c.stopScript()
        break
    
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        time.sleep(1)

print("UR5e connection closed.")
