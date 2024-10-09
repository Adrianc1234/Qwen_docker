# QwenClass.py

from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
import re
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core import Settings
from llama_index.core.postprocessor import SentenceTransformerRerank
from llama_index.core.memory import ChatMemoryBuffer
from Utils import *

class QwenClass:
    def __init__(self):
        self.companies = []
        self.products = []
        self.doc_meta = []
        self.documents = []
        self.index = None
        self.rerank = SentenceTransformerRerank(
            model="mixedbread-ai/mxbai-rerank-xsmall-v1", top_n=3
        )
        
        self.llm = Settings.llm  # Asegúrate de que Settings.llm esté configurado
        self.embed_model = Settings.embed_model  # Asegúrate de que Settings.embed_model esté configurado

    def simple_chat_engine(self):
        """
        Configura un chat engine simple para charlar sin contexto adicional.
        """
        # Crea un buffer de memoria para el chat
        chat_memory = ChatMemoryBuffer.from_defaults(token_limit=1000)

        # Devuelve un método que usa el LLM para completar el texto
        def chat(message):
            """
            Envía un mensaje al modelo y devuelve la respuesta.
            """
            # Procesa el mensaje y utiliza el LLM para obtener la respuesta
            response = self.llm.complete(prompt=message)  # Ajusta este método según tu LLM
            return response

        # Devuelve el método de chat, el cual se puede usar directamente
        return chat

    def load_documents(self, directory_path):
        reader = SimpleDirectoryReader(directory_path)
        self.documents = reader.load_data()

        pattern = re.compile(r"Product Sheet (.+?)-(.+)\.pdf")

        for docs in reader.iter_data():
            file_name = docs[0].metadata.get('file_name')

            if file_name.endswith('.pdf'):
                match = pattern.match(file_name)
                if match:
                    company_name = match.group(1)
                    drug_name = match.group(2)
                    self.companies.append(company_name)
                    self.products.append(drug_name)

            self.doc_meta.append(docs[0].metadata)
            print(f"Loaded {file_name}")

        print(self.companies)
        print(self.products)
        print(self.doc_meta)

    def create_index(self):
        node_parser = SentenceSplitter(chunk_size=1024)
        nodes = node_parser.get_nodes_from_documents(self.documents)
        self.index = VectorStoreIndex(nodes)

    # doctor chat_engine
    def doctor_setup_engine(self, company, mood, product):
        print(f"Setting up Doctor's chat engine for {company} - {product} with mood: {mood}")

        doctor_memory = ChatMemoryBuffer.from_defaults(token_limit=5000)

        print("Doctor's memory buffer initialized with token limit 5000")

        prompt = doctor_instruction_prompt(company, mood, product)

        doctor_chat_engine = self.index.as_chat_engine(
            llm=Settings.llm,
            memory=doctor_memory,
            context_prompt=prompt[0],
            node_postprocessors=[self.rerank],
            chat_mode="condense_plus_context",
            similarity_top_k=5,
        )
        print(f"Doctor's chat engine successfully set up with similarity_top_k = 5")

        return doctor_chat_engine, prompt[1]

    # sales chat_engine
    def salesperson_setup_engine(self, medic_type, company, product, interNum, mood, robinLang, robinName):
        print(f"Setting up Salesperson's chat engine for {company} - {product} with medic_type: {medic_type}, mood: {mood}")

        salesperson_memory = ChatMemoryBuffer.from_defaults(token_limit=5000)
        print("Salesperson's memory buffer initialized with token limit 5000")

        prompt = salesperson_instruction_prompt(medic_type, company, product, interNum, mood, robinLang, robinName)

        salesperson_chat_engine = self.index.as_chat_engine(
            llm=Settings.llm,
            memory=salesperson_memory,
            context_prompt=prompt,
            node_postprocessors=[self.rerank],
            chat_mode="condense_plus_context",
            similarity_top_k=5,
        )
        print(f"Salesperson's chat engine successfully set up with similarity_top_k = 5\n\n")

        return salesperson_chat_engine