import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import os
import tempfile
import signal
import sys
import threading
import queue
from faster_whisper import WhisperModel
from fuzzywuzzy import process, fuzz

from external.pydobotplus import auto_connect_dobot

# ---------------- CONFIGURATION ----------------
MIC_INDEX = 1  # Adjust this to your mic index
RECORD_DURATION = 2.5
SAMPLE_RATE = 44100
COMMANDS = [
    "up", "down", "left", "right", "forward", "backward", "home",
    "grip", "ungrip", "release",
    "magic pick from tray", "magic place on table",
    "robo assemble gear", "robo disassemble gear",
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

# ---------------- CTRL+C HANDLER ----------------
def signal_handler(sig, frame):
    print("\n[INFO] Ctrl+C detected. Exiting.")
    transcription_queue.put(None)
    if device:
        device.close()
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
                spoken = result_queue.get(timeout=10)  # 10s timeout
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

                # --- Command Actions ---
                if match == "up":
                    dobot_move_relative(dz=20)
                elif match == "down":
                    dobot_move_relative(dz=-20)
                elif match == "left":
                    dobot_move_relative(dy=-20)
                elif match == "right":
                    dobot_move_relative(dy=20)
                elif match == "forward":
                    dobot_move_relative(dx=20)
                elif match == "backward":
                    dobot_move_relative(dx=-20)
                elif match == "home":
                    dobot_home()
                elif match == "grip":
                    device.grip(True)
                elif match in ["release", "ungrip"]:
                    device.grip(False)
                elif match == "magic pick from tray":
                    dobot_pick()
                elif match == "magic place on table":
                    dobot_place()
                elif match.startswith("robo"):
                    print(f"[ROBO] Command recognized: '{match}'.")
                    print("→ [TODO] Implement UR5e control here.")
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
