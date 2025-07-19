import speech_recognition as sr

# Load recognizer
recognizer = sr.Recognizer()

# Path to your audio clip
audio_path = r"C:\Users\cguan28\Downloads\Audio l'argent et nous 2 Nathan et maman May.wav"  # Update path if needed

# Transcribe
with sr.AudioFile(audio_path) as source:
    audio_data = recognizer.record(source)
    text = recognizer.recognize_google(audio_data, language="fr-FR")

print("Transcription:", text)
