import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import speech_recognition as sr
from deep_translator import GoogleTranslator

duration = 5  # segundos de grabación
sample_rate = 44100

print("Speak now...")
recording = sd.rec(
  int(duration * sample_rate), # el número de muestras a grabar
  samplerate=sample_rate,      # tasa de muestreo
  channels=1,                  # 1 significa grabación mono
  dtype="int16")               # tipo de datos para las muestras grabadas
sd.wait()  # esperando a que termine la grabación

wav.write("output.wav", sample_rate, recording)
print("Recording completed, now recognising...")

recognizer = sr.Recognizer()
with sr.AudioFile("output.wav") as source:
    audio = recognizer.record(source)

try:
    text = recognizer.recognize_google(audio, language="es")
    print("You said:", text)
    result = GoogleTranslator(source='es', target='en').translate(text)
    print("Translation:", result)

except sr.UnknownValueError:             # - si Google no pudo entender el habla debido a ruido o silencio
    print("Speech could not be recognised.")
except sr.RequestError as e:             # - si no hay conexión a Internet o la API no está disponible
    print(f"Service Error: {e}")