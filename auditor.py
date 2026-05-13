import os
import requests
import json
import pandas as pd
from datetime import datetime

# ==========================================
# 1. MOTOR DE IA (DEEPSEEK LOCAL)
# ==========================================
def auditar_con_ia_local(transcripcion):
    print("   🧠 Consultando a Qwen...")
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
        "model": "qwen2.5",
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
# 2. PIPELINE DE AUDITORÍA Y REPORTE
# ==========================================
def procesar_y_reportar():
    CARPETA_AUDIOS = "Audios"
    
    # Buscar todos los archivos .txt generados por Whisper
    archivos_txt = sorted([f for f in os.listdir(CARPETA_AUDIOS) if f.endswith('.txt')])
    
    if not archivos_txt:
        print("❌ No se encontraron archivos .txt. Ejecuta transcriptor.py primero.")
        return

    print(f"📊 Iniciando Auditoría con IA de {len(archivos_txt)} llamadas...\n")
    
    # Lista para guardar los resultados
    resultados = []
    
    for archivo in archivos_txt:
        ruta_completa = os.path.join(CARPETA_AUDIOS, archivo)
        print(f"🔍 Auditando: {archivo}")
        
        with open(ruta_completa, 'r', encoding='utf-8') as f:
            transcripcion = f.read()
            
        # Si el audio estaba vacío o era muy corto, lo saltamos
        if len(transcripcion.strip()) < 10:
            print("   ⚠️ Transcripción muy corta. Saltando.")
            continue
            
        # Ejecutar la auditoría con Inteligencia Artificial
        alerta_churn, cumplimiento, sentimiento = auditar_con_ia_local(transcripcion)
        
        # Guardar en nuestro "diccionario" de datos
        resultados.append({
            "Archivo": archivo.replace('.txt', '.wav'),
            "Riesgo_Fuga_Churn": "ALTO" if alerta_churn else "Bajo",
            "Cumplimiento_Venta": "Sí" if cumplimiento else "No",
            "Sentimiento": sentimiento,
            "Snippet": transcripcion[:100] + "..." # Guardamos un pedacito del texto para contexto
        })
        
        print(f"   -> Churn: {alerta_churn} | Venta: {cumplimiento} | Humor: {sentimiento}\n")

    # ==========================================
    # 3. EXPORTACIÓN DE DATOS (PANDAS)
    # ==========================================
    print("💾 Generando reportes ejecutivos...")
    
    # Convertimos la lista de resultados a una Tabla de Pandas (DataFrame)
    df = pd.DataFrame(resultados)
    
    # 1. Exportar a CSV (Para abrir en Excel)
    df.to_csv("Reporte_QA_CallCenter.csv", index=False, encoding='utf-8')
    
    # 2. Exportar a Markdown (Para que se vea bonito en GitHub)
    with open("Reporte_QA_CallCenter.md", "w", encoding='utf-8') as f:
        f.write("# 📊 Reporte Ejecutivo de Calidad (QA) - Auditoría Automatizada\n\n")
        f.write(f"**Fecha:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(df.to_markdown(index=False))
        
    print("✅ ¡Éxito! Revisa los archivos 'Reporte_QA_CallCenter.csv' y '.md' en tu carpeta.")

if __name__ == "__main__":
    procesar_y_reportar()