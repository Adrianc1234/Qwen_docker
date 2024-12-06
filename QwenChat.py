# QwenClass.py

import json
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core import Settings
from llama_index.core.postprocessor import SentenceTransformerRerank
from llama_index.core.memory import ChatMemoryBuffer
from Utils import *

class QwenClassChat:
    def __init__(self):
        """
        Inicializa la clase QwenClass.
        """
        self.llm = Settings.llm  # Asegúrate de que Settings.llm esté configurado
        self.background = ""  # Aquí se almacenará el contexto global

    def set_background(self, background_json):
        """
        Establece el contexto global desde un string JSON.
        """
        try:
            background_data = json.loads(background_json)
            self.background = background_data.get("context", "")
            print("Background establecido exitosamente.")
        except json.JSONDecodeError as e:
            print(f"Error al cargar el background: {e}")
            self.background = ""

    def chat_engine(self):
        """
        Configura un chat engine simple que use el contexto global para responder.
        """
        # Crea un buffer de memoria para el chat
        chat_memory = ChatMemoryBuffer.from_defaults(token_limit=5000)

        def chat(message):
            """
            Envía un mensaje al modelo y devuelve la respuesta usando el contexto global.
            """
            # Combina el background con el mensaje del usuario
            prompt = f"Contexto: {self.background}\nPregunta: {message}\nRespuesta:"
            response = self.llm.complete(prompt=prompt)  # Ajusta este método según tu LLM
            return response

        # Devuelve el método de chat, el cual se puede usar directamente
        return chat