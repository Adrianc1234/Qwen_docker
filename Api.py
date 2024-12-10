# Api.py
from fastapi import FastAPI, HTTPException, Body
from ConfigManager import ConfigManager
from QwenChat import QwenClassChat
from Utils import clean_response
from pydantic import BaseModel
import uvicorn
import time

app = FastAPI()

# Inicializa las clases
config_manager = ConfigManager()
qwen = QwenClassChat()


@app.put("/chat")
def chat(
    context: str = Body(..., embed=True, description="Contexto global para el chat"),
    message: str = Body(..., embed=True, description="Mensaje que se desea responder")
):
    """
    Endpoint para chatear con el modelo usando un contexto dinámico.
    
    Args:
        context (str): Contexto global en formato string.
        message (str): Mensaje para enviar al modelo.

    Returns:
        dict: Respuesta generada por el modelo.
    """
    try:

        # Establece el contexto global
        background_json = f'{{"context": "{context}"}}'
        qwen.set_background(background_json)

        # Obtén el chat engine
        chat = qwen.chat_engine()

        # Usa el chat engine para responder el mensaje
        respuesta = chat(message)

        return {"response": respuesta}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error procesando la solicitud: {e}")

if __name__ == "__main__":
    uvicorn.run("Api:app", host="0.0.0.0", port=8000)