from faster_whisper import WhisperModel
import time
import os
import glob
import json

# ==========================================
# 1. CONFIGURACIÓN DEL MODELO LOCAL
# ==========================================
TAMAÑO_MODELO = "small" 
print(f"⚙️  Cargando modelo Whisper '{TAMAÑO_MODELO}' en memoria...")
modelo = WhisperModel(TAMAÑO_MODELO, device="cpu", compute_type="int8")

# ==========================================
# 2. LECTURA DINÁMICA DE CARPETA
# ==========================================
CARPETA_AUDIOS = "Audios"
ruta_busqueda = os.path.join(CARPETA_AUDIOS, "*.wav")
audios = sorted(glob.glob(ruta_busqueda))

if not audios:
    print(f"❌ No se encontraron archivos .wav en la carpeta '{CARPETA_AUDIOS}'.")
    exit()

print(f"📂 Se detectaron {len(audios)} audios en cola. Iniciando extracción a JSON...\n")

# ==========================================
# 3. PIPELINE DE EXTRACCIÓN ESTRUCTURADA
# ==========================================
for archivo in audios:
    print(f"🎙️ Transcribiendo archivo: {archivo}")
    tiempo_inicio = time.time()
    
    segmentos, info = modelo.transcribe(archivo, beam_size=5, language="es")
    
    transcripcion_completa = ""
    lista_segmentos = []
    duracion_final = 0.0
    
    # Recorremos los segmentos para armar nuestra estructura de datos
    for segmento in segmentos:
        texto = segmento.text.strip()
        transcripcion_completa += texto + " "
        duracion_final = segmento.end # El final del último segmento será la duración
        
        lista_segmentos.append({
            "inicio": round(segmento.start, 2),
            "fin": round(segmento.end, 2),
            "texto": texto
        })
        
    # Armamos el Objeto JSON (El Payload)
    datos_audio = {
        "metadatos": {
            "archivo_original": os.path.basename(archivo),
            "idioma_detectado": info.language,
            "confianza_idioma": round(info.language_probability, 2),
            "duracion_segundos": duracion_final
        },
        "transcripcion_texto": transcripcion_completa.strip(),
        "timeline": lista_segmentos
    }
    
    tiempo_fin = time.time()
    print(f"✅ Extracción completada en {tiempo_fin - tiempo_inicio:.2f} segundos.")
    
    # ==========================================
    # 4. GUARDADO EN FORMATO JSON
    # ==========================================
    nombre_json = archivo.replace(".wav", ".json")
    with open(nombre_json, "w", encoding="utf-8") as f:
        # dump guarda el diccionario como JSON bonito (indent=4)
        json.dump(datos_audio, f, ensure_ascii=False, indent=4)
    
    print(f"💾 JSON guardado en: {nombre_json}\n")

print("🎉 ¡Ingesta a JSON finalizada con éxito!")