from faster_whisper import WhisperModel
import time
import os
import glob

# ==========================================
# 1. CONFIGURACIÓN DEL MODELO LOCAL
# ==========================================
TAMAÑO_MODELO = "small" 

print(f"⚙️  Cargando modelo Whisper '{TAMAÑO_MODELO}' en memoria...")
# device="cpu" y compute_type="int8" evitan que tu RAM colapse
modelo = WhisperModel(TAMAÑO_MODELO, device="cpu", compute_type="int8")

# ==========================================
# 2. LECTURA DINÁMICA DE CARPETA
# ==========================================
CARPETA_AUDIOS = "Audios"

# Buscamos automáticamente todos los archivos .wav dentro de la subcarpeta
ruta_busqueda = os.path.join(CARPETA_AUDIOS, "*.wav")
audios = glob.glob(ruta_busqueda)

# Ordenamos la lista alfabéticamente para que procese de audio1 a audio13
audios.sort()

if not audios:
    print(f"❌ No se encontraron archivos .wav en la carpeta '{CARPETA_AUDIOS}'.")
    exit()

print(f"📂 Se detectaron {len(audios)} audios en cola. Iniciando procesamiento en lote...\n")

# ==========================================
# 3. PIPELINE DE PROCESAMIENTO MÚLTIPLE
# ==========================================
for archivo in audios:
    print(f"🎙️ Analizando archivo: {archivo}")
    print("-" * 40)
    tiempo_inicio = time.time()
    
    # Ejecutamos la inferencia con Whisper
    segmentos, info = modelo.transcribe(archivo, beam_size=5, language="es")
    
    transcripcion_completa = ""
    
    # Iteramos sobre cada fragmento de audio detectado
    for segmento in segmentos:
        marca_tiempo = f"[{segmento.start:.2f}s - {segmento.end:.2f}s]"
        texto = segmento.text.strip()
        
        # Imprimimos en pantalla para ver el progreso en tiempo real
        print(f"{marca_tiempo} {texto}")
        transcripcion_completa += texto + " "
        
    tiempo_fin = time.time()
    print("-" * 40)
    print(f"✅ Procesado en {tiempo_fin - tiempo_inicio:.2f} segundos.")
    
    # ==========================================
    # 4. GUARDADO EN LA CARPETA 'Audios'
    # ==========================================
    nombre_txt = archivo.replace(".wav", ".txt")
    with open(nombre_txt, "w", encoding="utf-8") as f:
        f.write(transcripcion_completa.strip())
    
    print(f"💾 Texto guardado en: {nombre_txt}\n")

print("🎉 ¡Pipeline de transcripción masiva finalizado con éxito!")