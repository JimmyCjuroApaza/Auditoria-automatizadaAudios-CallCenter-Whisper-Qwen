# 🎙️ QA-Whisper-CallCenters: Auditoría Inteligente de Calidad (Local AI)

![Pipeline Status](https://img.shields.io/badge/Status-Production--Ready-green)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![AI](https://img.shields.io/badge/Model-Faster--Whisper%20%2B%20Qwen2.5-orange)

Este proyecto es una solución de **Ingeniería de Datos e Inteligencia Artificial** diseñada para automatizar la auditoría de calidad en Call Centers. Permite procesar miles de horas de audio de forma local, garantizando la privacidad de los datos y reduciendo drásticamente los costos operativos asociados a APIs de nube.

##  Problema de Negocio
En el sector de Call Centers (especialmente en Perú y Latinoamérica), auditar llamadas para control de calidad es un proceso manual y costoso. Las empresas suelen auditar menos del 1% de sus llamadas. Este sistema permite una **cobertura del 100%** mediante:
- Detección automática de **Riesgo de Fuga (Churn)**.
- Verificación de **Cumplimiento Comercial** (ofrecimiento de promociones).
- Análisis de **Sentimiento y Tono** del cliente.

##  Arquitectura del Sistema

El pipeline se divide en tres etapas críticas:

1.  **Procesamiento Multimedia:** Conversión de video/audio a formato optimizado (WAV 16kHz Mono) usando **FFmpeg**.
2.  **Transcripción Sensorial:** Uso de `faster-whisper` (basado en CTranslate2) para una conversión de voz a texto 4x más rápida que el modelo original.
3.  **Auditoría Cognitiva (LLM):** Inferencia local mediante **Ollama** utilizando el modelo **Qwen 2.5**, especializado en razonamiento semántico y detección de intención en español.

##  A/B Testing: Qwen 2.5 vs. DeepSeek-Coder
Durante el desarrollo, se realizó una comparativa de modelos para la tarea de auditoría:

| Métrica | DeepSeek-Coder 6.7B | Qwen 2.5 (7B) |
| :--- | :--- | :--- |
| **Comprensión Semántica** | Media (Falsos positivos en Churn) | **Alta (Consistente)** |
| **Precisión JSON** | Alta | Alta |
| **Detección de Sarcasmo** | Baja | **Media-Alta** |
| **Resultado** | Tiende a alucinar riesgos | **Recomendado para Producción** |

##  Instalación

### Requisitos
- Python 3.10+
- FFmpeg
- Ollama (con el modelo `qwen2.5` descargado)

### Setup
```bash
pip install faster-whisper pandas requests

Ejecución:

Genera las transcripciones:
Bash
python3 transcriptor.py

Ejecuta la auditoría inteligente:
Bash
python3 auditor.py

---
> **Autor:** Jimmy Cristhian Cjuro Apaza
> *Estudiante de Ingeniería de Software | UNMSM*
> *Desarrollador enfocado en Data Engineering y Soluciones de IA aplicadas a la Industria.*