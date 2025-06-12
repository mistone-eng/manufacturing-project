import sys
import os

# Add the manufacturing-project path to allow importing external.pydobotplus
sys.path.append("/home/stem/Code/manufacturing-project")

import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import tempfile
import signal
import threading
import queue
from faster_whisper import WhisperModel
from fuzzywuzzy import process, fuzz

from external.pydobotplus import auto_connect_dobot
from ur_rtde import RTDEControlInterface as RTDEControl
from ur_rtde import RTDEReceiveInterface as RTDEReceive

# ---------------- CONFIGURATION ----------------
MIC_INDEX = 1  # Adjust this to your mic index
RECORD_DURATION = 2.5
SAMPLE_RATE = 44100
COMMANDS = [
    # DOBOT
    "magic up", "magic down", "magic left", "magic right", "magic forward", "magic backward",
    "magic home", "magic grip", "magic ungrip", "magic release",
    "magic pick from tray", "magic place on table",

    # UR5e
    "robo move up", "robo move down", "robo home", "robo stop",

    # Exit
    "quit", "exit", "stop"
]

# ---------------- SETUP ----------------
model = WhisperModel("tiny.en", compute_type="int8")
transcription_queue = queue.Queue()
result_queue = queue.Queue()

# Connect to DOBOT
try:
    device = auto_connect_dobot()
    device.speed(velocity=100, acceleration=100)
    print("[INFO] DOBOT connected and configured.")
    dob_current_pos = {"x": 200.0, "y": 0.0, "z": 70.0, "r": 0.0}
    device.move_to(**dob_current_pos, wait=True)
except Exception as e:
    print(f"[ERROR] Failed to connect to DOBOT: {e}")
    device = None

# Connect to UR5e
UR5E_IP = "192.168.1.5"
ur_control = None
ur_receive = None
try:
    print("[INFO] Connecting to UR5e...")
    ur_control = RTDEControl(UR5E_IP)
    ur_receive = RTDEReceive(UR5E_IP)
    print("[INFO] UR5e connected successfully.")
except Exception as e:
    print(f"[ERROR] Failed to connect to UR5e: {e}")

# ---------------- CTRL+C HANDLER ----------------
def signal_handler(sig, frame):
    print("\n[INFO] Ctrl+C detected. Exiting.")
    transcription_queue.put(None)
    if device:
        device.close()
    if ur_control:
        ur_control.stopScript()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

# ---------------- AUDIO FUNCTIONS ----------------
def record_audio(duration=RECORD_DURATION, samplerate=SAMPLE_RATE):
    print(">> Speak now...")
    try:
        recording = sd.rec(int(duration * samplerate), samplerate=samplerate,
                           channels=1, dtype='int16', device=MIC_INDEX)
        sd.wait()
        return recording.squeeze()
    except Exception as e:
        print(f"[ERROR] Recording failed: {e}")
        return None

def save_temp_wav(audio, samplerate=SAMPLE_RATE):
    temp_path = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    wav.write(temp_path.name, samplerate, audio)
    return temp_path.name

# ---------------- TRANSCRIPTION THREAD ----------------
def whisper_worker():
    while True:
        wav_path = transcription_queue.get()
        if wav_path is None:
            break
        try:
            print("[TRANSCRIBE] Processing...")
            segments, _ = model.transcribe(wav_path, language="en")
            os.remove(wav_path)
            for segment in segments:
                result_queue.put(segment.text.strip().lower())
                break
            else:
                result_queue.put("")
        except Exception as e:
            print(f"[ERROR] Whisper failed: {e}")
            result_queue.put("")

# ---------------- FUZZY COMMAND MATCH ----------------
def fuzzy_match(command):
    match, score = process.extractOne(command, COMMANDS, scorer=fuzz.ratio)
    return (match, score) if score > 70 else (None, score)

# ---------------- DOBOT ROUTINES ----------------
def dobot_move_relative(dx=0, dy=0, dz=0, dr=0):
    if not device:
        print("[ERROR] No DOBOT connected.")
        return
    dob_current_pos["x"] += dx
    dob_current_pos["y"] += dy
    dob_current_pos["z"] += dz
    dob_current_pos["r"] += dr
    device.move_to(**dob_current_pos, wait=True)
    print(f"[DOBOT] Moved to: {dob_current_pos}")

def dobot_home():
    if device:
        print("[ACTION] Returning DOBOT to home.")
        device.home()
        dob_current_pos.update({"x": 200.0, "y": 0.0, "z": 70.0, "r": 0.0})

def dobot_pick():
    print("[ACTION] Magic picking from tray...")
    device.pickOrPlace(260, 10, 20, do_pick=True)

def dobot_place():
    print("[ACTION] Magic placing on table...")
    device.pickOrPlace(240, 0, 20, do_pick=False)

# ---------------- UR5e ROUTINES ----------------
def ur5e_home():
    if ur_control:
        print("[ROBO] Moving to home position...")
        ur_control.moveL([0.2, -0.3, 0.3, 0, 3.14, 0], 0.5, 0.3)

def ur5e_up():
    if ur_control:
        pose = ur_receive.getActualTCPPose()
        pose[2] += 0.05
        ur_control.moveL(pose, 0.5, 0.3)
        print("[ROBO] Moved up.")

def ur5e_down():
    if ur_control:
        pose = ur_receive.getActualTCPPose()
        pose[2] -= 0.05
        ur_control.moveL(pose, 0.5, 0.3)
        print("[ROBO] Moved down.")

def ur5e_stop():
    if ur_control:
        ur_control.stopScript()
        print("[ROBO] Script stopped.")

# ---------------- MAIN LOOP ----------------
if __name__ == "__main__":
    print("[VOICE] Listening for:", ", ".join(COMMANDS))
    threading.Thread(target=whisper_worker, daemon=True).start()

    while True:
        try:
            audio = record_audio()
            if audio is None:
                continue
            wav_path = save_temp_wav(audio)
            transcription_queue.put(wav_path)

            try:
                spoken = result_queue.get(timeout=10)
            except queue.Empty:
                print("[WARN] Whisper timeout — no response.")
                continue

            if not spoken:
                print("[WARN] No speech detected.")
                continue

            print(f"[VOICE] You said: '{spoken}'")
            match, score = fuzzy_match(spoken)

            if match:
                print(f"[✓] Recognized as '{match}' (confidence: {score}%)")

                # --- Magic = DOBOT ---
                if match == "magic up":
                    dobot_move_relative(dz=20)
                elif match == "magic down":
                    dobot_move_relative(dz=-20)
                elif match == "magic left":
                    dobot_move_relative(dy=-20)
                elif match == "magic right":
                    dobot_move_relative(dy=20)
                elif match == "magic forward":
                    dobot_move_relative(dx=20)
                elif match == "magic backward":
                    dobot_move_relative(dx=-20)
                elif match == "magic home":
                    dobot_home()
                elif match == "magic grip":
                    device.grip(True)
                elif match in ["magic release", "magic ungrip"]:
                    device.grip(False)
                elif match == "magic pick from tray":
                    dobot_pick()
                elif match == "magic place on table":
                    dobot_place()

                # --- Robo = UR5e ---
                elif match == "robo move up":
                    ur5e_up()
                elif match == "robo move down":
                    ur5e_down()
                elif match == "robo home":
                    ur5e_home()
                elif match == "robo stop":
                    ur5e_stop()

                elif match in ["quit", "exit", "stop"]:
                    print("[INFO] Exit command received. Shutting down.")
                    transcription_queue.put(None)
                    break
            else:
                print(f"[✗] No valid match found (confidence: {score}%)")

        except Exception as e:
            print(f"[ERROR] {e}")

    if device:
        device.close()
        print("[INFO] DOBOT safely disconnected.")
    if ur_control:
        ur_control.stopScript()
        print("[INFO] UR5e safely stopped.")
