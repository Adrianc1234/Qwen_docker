#!/bin/bash

# Iniciar el servidor de Ollama en segundo plano
ollama serve &

# Esperar unos segundos para asegurarse de que Ollama está listo
sleep 5

# Iniciar la aplicación
uvicorn Api:app --host 0.0.0.0 --port 8000