import speech_recognition as sr
from datetime import date
from time import sleep
import os
import sys

# Suppress ALSA & JACK errors
def suppress_alsa_errors():
    sys.stderr = open(os.devnull, 'w')

# Restore original stderr (optional if needed for logging or debugging)
def restore_errors():
    sys.stderr = sys.__stderr__

r = sr.Recognizer()

# Apply suppression
suppress_alsa_errors()
mic = sr.Microphone()
restore_errors()

print("Voice recognition started. Say something!")

while True:
    try:
        with mic as source:
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source)

        words = r.recognize_google(audio).lower()
        print(f"You said: {words}")

        if "today" in words:
            print(date.today())

        if "stop" in words:
            print("Stopping...")
            sleep(1)
            break

    except sr.UnknownValueError:
        print("Sorry, I didn’t catch that.")
    except sr.RequestError:
        print("Speech recognition service is unavailable.")
