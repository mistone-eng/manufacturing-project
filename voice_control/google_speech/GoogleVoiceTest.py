import os
import time
import threading
import speech_recognition as sr
from fuzzywuzzy import fuzz, process

# --- Suppress ALSA/JACK warnings ---
os.environ["SDL_AUDIODRIVER"] = "dummy"
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"

import ctypes
from ctypes.util import find_library
try:
    asound = ctypes.CDLL(find_library("asound"))
    asound.snd_lib_error_set_handler(None)
except Exception:
    pass

# --- Target commands ---
valid_commands = [
    "up", "down", "left", "right", "forward", "backward",
    "home", "grip", "ungrip", "release", "quit", "exit", "stop"
]

# --- Helper to find TONOR microphone ---
def find_mic_index(name_keyword="TONOR"):
    for i, name in enumerate(sr.Microphone.list_microphone_names()):
        if name_keyword.lower() in name.lower():
            return i
    raise ValueError("[ERROR] Microphone not found.")

# --- Fuzzy matching helper ---
def fuzzy_match_command(command):
    match, score = process.extractOne(command, valid_commands, scorer=fuzz.ratio)
    return (match, score) if score > 70 else (None, score)

# --- Voice recognition ---
def listen_for_commands():
    recognizer = sr.Recognizer()
    mic_index = find_mic_index()
    mic = sr.Microphone(device_index=mic_index)

    with mic as source:
        recognizer.adjust_for_ambient_noise(source)
        print("[VOICE] Speak one of the following:", ", ".join(valid_commands))

        while True:
            try:
                print(">> Speak now...")
                audio = recognizer.listen(source)
                command = recognizer.recognize_google(audio).lower()
                print(f"[VOICE] You said: '{command}'")

                match, score = fuzzy_match_command(command)

                if match:
                    print(f"[✓] Recognized as '{match}' (confidence: {score}%)")
                    if match in ["quit", "exit", "stop"]:
                        print("[INFO] Exit command received. Shutting down.")
                        break
                else:
                    print(f"[✗] No valid match found (confidence: {score}%)")

            except sr.UnknownValueError:
                print("[WARN] Could not understand audio.")
            except sr.RequestError:
                print("[ERROR] Google Speech Recognition unavailable.")
            except KeyboardInterrupt:
                print("\n[INFO] Ctrl+C detected. Exiting program.")
                break
            except Exception as e:
                print(f"[ERROR] {e}")

# --- Start main program ---
if __name__ == "__main__":
    listen_for_commands()
    print("[INFO] Program ended.")
