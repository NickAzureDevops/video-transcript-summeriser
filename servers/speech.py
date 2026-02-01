# Combined script: Download transcript and audio, then (optionally) run Azure Speech diarization
import subprocess
import os
from dotenv import load_dotenv
import azure.cognitiveservices.speech as speechsdk
load_dotenv()

speech_key = os.environ.get('SPEECH_KEY')
endpoint = os.environ.get('ENDPOINT')
region = os.environ.get('REGION', 'uksouth')

VIDEO_ID = "4MUgq_rzjqo"
VIDEO_URL = f"https://www.youtube.com/watch?v={VIDEO_ID}"

TRANSCRIPT_DIR = "./transcript"
TRANSCRIPT_FILE = f"{TRANSCRIPT_DIR}/{VIDEO_ID}.txt"
AUDIO_FILE = f"{TRANSCRIPT_DIR}/audio.wav"

# Ensure transcript directory exists
os.makedirs(TRANSCRIPT_DIR, exist_ok=True)

# 1. Download transcript
print(f"Downloading transcript for {VIDEO_ID}...")
with open(TRANSCRIPT_FILE, "w") as tf:
    subprocess.run([
        "python3", "-m", "youtube_transcript_api", VIDEO_ID
    ], stdout=tf, check=True)
print(f"Transcript saved to {TRANSCRIPT_FILE}")

# 2. Download audio as WAV
print(f"Downloading audio for {VIDEO_ID}...")
subprocess.run([
    "yt-dlp", "-x", "--audio-format", "wav", "-o", AUDIO_FILE, VIDEO_URL
], check=True)
print(f"Audio saved to {AUDIO_FILE}")

audio_config = speechsdk.audio.AudioConfig(filename=AUDIO_FILE)

speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=region)
speech_config.speech_recognition_language = "en-US"
audio_config = speechsdk.audio.AudioConfig(filename=AUDIO_FILE)

# Create recognizer
speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

print("Transcribing (continuous)...")
all_results = []
done = False

def recognized(evt):
    if evt.result.reason == speechsdk.ResultReason.RecognizedSpeech:
        all_results.append(evt.result.text)

def stop_cb(evt):
    global done
    done = True

speech_recognizer.recognized.connect(recognized)
speech_recognizer.session_stopped.connect(stop_cb)
speech_recognizer.canceled.connect(stop_cb)

speech_recognizer.start_continuous_recognition()
while not done:
    pass
speech_recognizer.stop_continuous_recognition()

with open(f"{TRANSCRIPT_DIR}/agentcon.txt", "w") as f:
    for idx, line in enumerate(all_results, 1):
        line = line.strip()
        if line:
            f.write(f"{idx}: {line}\n")