# Api.py
from fastapi import FastAPI
from ConfigManager import ConfigManager
from QwenClass import QwenClass
from Utils import clean_response
from pydantic import BaseModel
import uvicorn
import time

app = FastAPI()

# Inicializa las clases
config_manager = ConfigManager()
qwen = QwenClass()

# Define el modelo de solicitud
class ConversationRequest(BaseModel):
    company: str
    mood: str
    product: str

@app.get("/load_documents")
def load_documents():
    qwen.load_documents('Product Sheets Pharmaceutics')
    qwen.create_index()
    return {"status": "Documents loaded and index created"}

@app.post("/start_conversation")
def start_conversation(request: ConversationRequest):
    company = request.company
    mood = request.mood
    product = request.product

    # Configura los motores de chat para el doctor y el vendedor
    doctor_engine, prompt_data = qwen.doctor_setup_engine(company, mood, product)
    medic_type, robinLang, robinName, interNum = prompt_data
    salesperson_engine = qwen.salesperson_setup_engine(
        medic_type, company, product, interNum, mood, robinLang, robinName
    )

    # Reinicia las memorias de chat
    doctor_engine.reset()
    salesperson_engine.reset()

    # Variables para almacenar la conversación
    conversation_history = []

    # Palabras clave para limpiar las respuestas
    keywords_to_remove = ["user:", "assistant:", "doctor:", "salesperson:",
                          "Assistant:", "User:", "Doctor:", "Salesperson:", "(Note:"]

    # Inicia la conversación
    # Medir el tiempo de inicio
    start_time = time.time()

    # Primera interacción
    doctor_response = doctor_engine.chat("Initiate conversation")
    cleaned_doctor_response = clean_response(doctor_response.response, keywords_to_remove)

    salesperson_response = salesperson_engine.chat(cleaned_doctor_response)
    cleaned_salesperson_response = clean_response(salesperson_response.response, keywords_to_remove)

    conversation_history.append({"role": "Doctor", "message": cleaned_doctor_response})
    conversation_history.append({"role": "Salesperson", "message": cleaned_salesperson_response})

    # Segunda interacción
    doctor_followup_response_1 = doctor_engine.chat(cleaned_salesperson_response)
    cleaned_doctor_followup_1 = clean_response(doctor_followup_response_1.response, keywords_to_remove)

    salesperson_followup_response_1 = salesperson_engine.chat(cleaned_doctor_followup_1)
    cleaned_salesperson_followup_1 = clean_response(salesperson_followup_response_1.response, keywords_to_remove)

    conversation_history.append({"role": "Doctor", "message": cleaned_doctor_followup_1})
    conversation_history.append({"role": "Salesperson", "message": cleaned_salesperson_followup_1})

    # Tercera interacción
    doctor_followup_response_2 = doctor_engine.chat(cleaned_salesperson_followup_1)
    cleaned_doctor_followup_2 = clean_response(doctor_followup_response_2.response, keywords_to_remove)

    salesperson_followup_response_2 = salesperson_engine.chat(cleaned_doctor_followup_2)
    cleaned_salesperson_followup_2 = clean_response(salesperson_followup_response_2.response, keywords_to_remove)

    conversation_history.append({"role": "Doctor", "message": cleaned_doctor_followup_2})
    conversation_history.append({"role": "Salesperson", "message": cleaned_salesperson_followup_2})

    # Medir el tiempo de fin
    end_time = time.time()
    total_time = end_time - start_time

    # Retornar la conversación y el tiempo total
    return {
        "conversation": conversation_history,
        "total_time": total_time
    }

if __name__ == "__main__":
    uvicorn.run("Api:app", host="0.0.0.0", port=8000)