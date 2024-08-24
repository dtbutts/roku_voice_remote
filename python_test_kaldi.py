import sounddevice as sd
import vosk
import sys
import numpy as np
import threading
import time
import json
import requests

# Path to the Vosk model
model_path = "../kaldiTry/vosk-model-small-en-us-0.15"

# You need to find your roku device's IP address and set it here
IP_ADDRESS_OF_TV = "TV_IP_ADDRESS_HERE"

# Load the Vosk modelf
model = vosk.Model(model_path)

# Create a Vosk recognizer
rec = vosk.KaldiRecognizer(model, 16000)

# Define the audio callback function
def audio_callback(indata, frames, time, status):
    if status:
        print("Error:", status)
        return

    # Convert the audio data to bytes
    audio_data = (indata * 32767).astype(np.int16).tobytes()

    # Perform speech recognition on the audio data
    rec.AcceptWaveform(audio_data)

def communicate_with_tv(keyword):
    try:
        url = "http://" + IP_ADDRESS_OF_TV + ":8060/keypress/" + keyword
        response = requests.post(url, data='')
    except requests.exceptions.RequestException as e:
        print("Request failed:", e)

def parse_out_keyword(result):
    testingString = json.loads(result)
    actualString = testingString.get("partial")  # Use .get() method to avoid KeyError
    print(actualString)

    if actualString and actualString.strip():  # Check if the recognized text is not empty
        if actualString == "okay" or actualString == "stop" or actualString == "go" or actualString == "play":
            keyword = "select"
        elif actualString == "pause":
            keyword = "select"
        elif actualString == "back":
            keyword = "back"
        elif actualString == "left":
            keyword = "left"
        elif actualString == "right":
            keyword = "right"
        elif actualString == "up" or actualString == "hi" or actualString == "high":
            keyword = "up"
        elif actualString == "down" or actualString == "low":
            keyword = "down"
        elif actualString == "off":
            keyword = "PowerOff"
        elif actualString == "on":
            keyword = "PowerOn"
        elif actualString == "turn it up" or actualString == "volume up" or actualString == "louder":
            keyword = "VolumeUp"
        elif actualString == "turn it down" or actualString == "volume down" or actualString == "quieter":
            keyword = "VolumeDown"
        elif actualString == "mute":
            keyword = "VolumeMute"
        else:
            keyword = "nothing"

        if keyword != "nothing":
            communicate_with_tv(keyword)
    else:
        print("No recognizable text found.")

# Function to continuously listen and process audio
def listen_and_process():
    with sd.InputStream(callback=audio_callback, channels=1, samplerate=16000):
        while True:
            try:
                sd.sleep(100)
            except KeyboardInterrupt:
                print("\nStopped by user.")
                break

# Function to parse partial results every two seconds
def parse_partial_results():
    global rec  # Declare rec as a global variable

    while True:
        # Get partial recognition result
        result = rec.PartialResult()
        if result:
            # Print the recognized text
            parse_out_keyword(result)

            # Reset the recognizer after each partial result
            rec = vosk.KaldiRecognizer(model, 16000)

        # Sleep for two seconds
        time.sleep(3.0)

# Create and start the threads
listen_thread = threading.Thread(target=listen_and_process)
parse_thread = threading.Thread(target=parse_partial_results)

listen_thread.start()
parse_thread.start()

# Wait for the threads to complete
listen_thread.join()
parse_thread.join()
