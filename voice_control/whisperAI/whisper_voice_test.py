import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import os
import tempfile
from faster_whisper import WhisperModel
from fuzzywuzzy import process, fuzz
import signal
import sys

# --- Setup ---
MIC_INDEX = 0  # Change this to your TONOR/YETI mic index
COMMANDS = [
    "up", "down", "left", "right",
    "forward", "backward", "home",
    "grip", "ungrip", "release",
    "quit", "exit", "stop"
]
RECORD_DURATION = 2  # seconds
SAMPLE_RATE = 16000

model = WhisperModel("base.en", compute_type="auto")  # Can change to 'tiny.en' for speed

# --- Signal handler for Ctrl+C ---
def signal_handler(sig, frame):
    print("\n[INFO] Ctrl+C detected. Exiting.")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

# --- Function to record and transcribe ---
def record_audio(duration=RECORD_DURATION, samplerate=SAMPLE_RATE):
    print(">> Speak now...")
    recording = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1, dtype='int16', device=MIC_INDEX)
    sd.wait()
    return recording.squeeze()

def save_temp_wav(audio, samplerate=SAMPLE_RATE):
    temp_path = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    wav.write(temp_path.name, samplerate, audio)
    return temp_path.name

def transcribe_with_whisper(wav_path):
    segments, _ = model.transcribe(wav_path, language="en")
    for segment in segments:
        return segment.text.strip().lower()
    return ""

def fuzzy_match(command):
    match, score = process.extractOne(command, COMMANDS, scorer=fuzz.ratio)
    return (match, score) if score > 70 else (None, score)

# --- Main loop ---
if __name__ == "__main__":
    print("[VOICE] Listening for:", ", ".join(COMMANDS))

    while True:
        try:
            audio = record_audio()
            wav_path = save_temp_wav(audio)
            transcription = transcribe_with_whisper(wav_path)
            os.remove(wav_path)

            if not transcription:
                print("[WARN] No speech detected.")
                continue

            print(f"[VOICE] You said: '{transcription}'")
            match, score = fuzzy_match(transcription)

            if match:
                print(f"[✓] Recognized as '{match}' (confidence: {score}%)")
                if match in ["quit", "exit", "stop"]:
                    print("[INFO] Exit command received. Shutting down.")
                    break
            else:
                print(f"[✗] No valid match found (confidence: {score}%)")

        except Exception as e:
            print(f"[ERROR] {e}")
