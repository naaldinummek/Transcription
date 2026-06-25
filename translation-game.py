import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import speech_recognition as sr
from deep_translator import GoogleTranslator
import random

# Diccionario de palabras por nivel
words_by_level = {
    "facil": ["gato", "perro", "manzana", "leche", "sol"],
    "medio": ["banana", "escuela", "amigo", "ventana", "amarillo"],
    "dificil": ["tecnologia", "universidad", "informacion", "pronunciacion", "imaginacion"]
}

def grabar_audio(duracion=5):
    """Graba audio del micrófono y lo guarda en un archivo"""
    sample_rate = 44100
    print("🎤 Habla ahora...")
    
    recording = sd.rec(
        int(duracion * sample_rate),
        samplerate=sample_rate,
        channels=1,
        dtype="int16"
    )
    sd.wait()
    
    wav.write("output.wav", sample_rate, recording)
    print("✓ Grabación completada\n")

def reconocer_audio():
    """Reconoce el audio grabado en inglés"""
    recognizer = sr.Recognizer()
    
    try:
        with sr.AudioFile("output.wav") as source:
            audio = recognizer.record(source)
        
        # Reconocer en inglés
        text = recognizer.recognize_google(audio, language="en-US")
        return text.lower()
    
    except sr.UnknownValueError:
        print("❌ No se pudo reconocer el audio.")
        return None
    except sr.RequestError as e:
        print(f"⚠️ Error de servicio: {e}")
        return None

def obtener_traduccion(palabra):
    """Obtiene la traducción correcta de una palabra"""
    try:
        traduccion = GoogleTranslator(source='es', target='en').translate(palabra)
        return traduccion.lower()
    except:
        return None

def comparar_respuestas(respuesta_usuario, respuesta_correcta):
    """Compara la respuesta del usuario con la correcta"""
    # Eliminar espacios y convertir a minúsculas
    respuesta_usuario = respuesta_usuario.strip().lower()
    respuesta_correcta = respuesta_correcta.strip().lower()
    
    # Coincidencia exacta o casi exacta
    if respuesta_usuario == respuesta_correcta:
        return True
    
    # Permitir pequeñas variaciones (plurales, etc)
    if respuesta_usuario.replace('s', '') == respuesta_correcta.replace('s', ''):
        return True
    
    return False

def mostrar_menu():
    """Muestra el menú de selección de nivel"""
    print("\n" + "="*50)
    print("      🎮 JUEGO DE TRADUCCIÓN ESPAÑOL-INGLÉS 🎮")
    print("="*50)
    print("\nSelecciona un nivel de dificultad:\n")
    print("  1. Fácil")
    print("  2. Medio")
    print("  3. Difícil")
    print()
    
    while True:
        opcion = input("Tu opción (1-3): ").strip()
        if opcion in ["1", "2", "3"]:
            niveles = {"1": "facil", "2": "medio", "3": "dificil"}
            return niveles[opcion]
        else:
            print("❌ Opción inválida. Intenta de nuevo.")

def jugar_ronda(palabra, numero_ronda, total_rondas, puntos, errores):
    """Ejecuta una ronda del juego"""
    print(f"\n{'─'*50}")
    print(f"Ronda {numero_ronda}/{total_rondas} | Puntos: {puntos} | Errores: {errores}")
    print(f"{'─'*50}")
    
    print(f"\n📝 Palabra en español: {palabra.upper()}\n")
    print("Tienes 5 segundos para pronunciar la traducción en inglés.")
    
    # Grabar audio
    grabar_audio(duracion=5)
    
    # Reconocer lo que dijo
    respuesta_usuario = reconocer_audio()
    
    if respuesta_usuario is None:
        print("⚠️ Intenta de nuevo...\n")
        return puntos, errores
    
    print(f"📢 Dijiste: '{respuesta_usuario}'")
    
    # Obtener traducción correcta
    respuesta_correcta = obtener_traduccion(palabra)
    
    if respuesta_correcta is None:
        print("⚠️ Error al obtener la traducción.\n")
        return puntos, errores
    
    print(f"✓ Traducción correcta: '{respuesta_correcta}'")
    
    # Comparar respuestas
    if comparar_respuestas(respuesta_usuario, respuesta_correcta):
        print("✅ ¡CORRECTO!\n")
        puntos += 10
    else:
        print("❌ INCORRECTO\n")
        errores += 1
    
    return puntos, errores

def mostrar_resultados(puntos, errores):
    """Muestra los resultados finales"""
    total_rondas = (puntos // 10) + errores
    
    print("\n" + "="*50)
    print("              🏁 JUEGO TERMINADO 🏁")
    print("="*50)
    print(f"\n  Puntos totales: {puntos}")
    print(f"  Errores: {errores}")
    
    if total_rondas > 0:
        porcentaje = (puntos / (puntos + errores * 10)) * 100
        print(f"  Porcentaje de acierto: {porcentaje:.1f}%")
    
    print("\n" + "="*50 + "\n")

def main():
    """Función principal"""
    # Seleccionar nivel
    nivel = mostrar_menu()
    print(f"\n✓ Nivel seleccionado: {nivel.upper()}")
    print("Obtener palabras...")
    
    # Obtener palabras del nivel
    palabras = words_by_level[nivel]
    palabras_juego = random.sample(palabras, min(3, len(palabras)))
    
    print(f"✓ Se seleccionaron 3 palabras\n")
    
    # Variables del juego
    puntos = 0
    errores = 0
    
    # Jugar rondas
    for i, palabra in enumerate(palabras_juego, 1):
        puntos, errores = jugar_ronda(palabra, i, len(palabras_juego), puntos, errores)
    
    # Mostrar resultados
    mostrar_resultados(puntos, errores)

if __name__ == "__main__":
    main()