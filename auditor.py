import os
import requests
import json
import pandas as pd
from datetime import datetime

# ==========================================
# 1. MOTOR DE IA (QWEN 2.5 LOCAL)
# ==========================================
def auditar_con_qwen(transcripcion):
    print("   🧠 Consultando a Qwen 2.5...")
    OLLAMA_URL = "http://localhost:11434/api/generate"
    
    prompt = f"""
    Eres un auditor de calidad QA para un Call Center.
    Analiza esta transcripción y responde ÚNICAMENTE en formato JSON válido con estas tres claves:
    - "alerta_churn": true o false (Si el cliente amenaza con quejarse, cancelar, o está furioso).
    - "cumplimiento": true o false (Si el operador ofreció promociones o cumplió un protocolo de venta).
    - "sentimiento": "Positivo", "Neutral" o "Negativo".

    Transcripción:
    {transcripcion}
    """
    
    payload = {
        "model": "qwen2.5", # Usamos el modelo que demostró ser superior
        "prompt": prompt,
        "stream": False,
        "format": "json", 
        "temperature": 0.0
    }
    
    try:
        respuesta = requests.post(OLLAMA_URL, json=payload)
        datos = json.loads(respuesta.json()["response"])
        return datos.get("alerta_churn", False), datos.get("cumplimiento", False), datos.get("sentimiento", "Neutral")
    except Exception as e:
        print(f"   ❌ Error en IA: {e}")
        return False, False, "Error"

# ==========================================
# 2. PIPELINE DE AUDITORÍA
# ==========================================
def procesar_y_reportar():
    CARPETA_AUDIOS = "Audios"
    
    # Ahora buscamos los JSON generados
    archivos_json = sorted([f for f in os.listdir(CARPETA_AUDIOS) if f.endswith('.json')])
    
    if not archivos_json:
        print("❌ No se encontraron archivos .json. Ejecuta transcriptor.py primero.")
        return

    print(f"📊 Iniciando Auditoría con Qwen de {len(archivos_json)} llamadas...\n")
    resultados = []
    
    for archivo in archivos_json:
        ruta_completa = os.path.join(CARPETA_AUDIOS, archivo)
        print(f"🔍 Leyendo metadata de: {archivo}")
        
        # Leemos el JSON de forma estructurada
        with open(ruta_completa, 'r', encoding='utf-8') as f:
            datos_llamada = json.load(f)
            
        transcripcion = datos_llamada["transcripcion_texto"]
        duracion = datos_llamada["metadatos"]["duracion_segundos"]
            
        if duracion < 2.0 or len(transcripcion.strip()) < 10:
            print("   ⚠️ Audio demasiado corto. Saltando.")
            continue
            
        # Ejecutar auditoría
        alerta_churn, cumplimiento, sentimiento = auditar_con_qwen(transcripcion)
        
        resultados.append({
            "Archivo": datos_llamada["metadatos"]["archivo_original"],
            "Duración (s)": duracion,
            "Riesgo Fuga (Churn)": "🔴 ALTO" if alerta_churn else "🟢 Bajo",
            "Cumplió Venta": "✅ Sí" if cumplimiento else "❌ No",
            "Sentimiento": sentimiento,
        })
        
        print(f"   -> Churn: {alerta_churn} | Venta: {cumplimiento} | Humor: {sentimiento}\n")

    # ==========================================
    # 3. EXPORTACIÓN DEL REPORTE
    # ==========================================
    print("💾 Generando reportes ejecutivos...")
    df = pd.DataFrame(resultados)
    
    df.to_csv("Reporte_QA_CallCenter.csv", index=False, encoding='utf-8')
    
    with open("Reporte_QA_CallCenter.md", "w", encoding='utf-8') as f:
        f.write("# 📊 Reporte Ejecutivo de Calidad (QA) - Auditoría Automatizada\n\n")
        f.write(f"**Fecha:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(df.to_markdown(index=False))
        
    print("✅ ¡Éxito! Revisa los archivos 'Reporte_QA_CallCenter.csv' y '.md' en tu carpeta.")

if __name__ == "__main__":
    procesar_y_reportar()