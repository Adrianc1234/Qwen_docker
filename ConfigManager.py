# ConfigManager.py

import os
import subprocess
import logging
from huggingface_hub import login
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import Settings
from llama_index.core.node_parser import SentenceSplitter

# Configuración básica de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class ConfigManager:
    def __init__(self, install_deps=True, setup_env=True, download_model=True):
        """
        :param install_deps: Flag to control whether to install dependencies.
        :param setup_env: Flag to control whether to setup environment variables.
        :param download_model: Flag to control whether to download the model.
        """
        self.install_deps = install_deps
        self.setup_env = setup_env
        self.download_model = download_model

        logging.info(f"ConfigManager initialized with flags: install_deps={install_deps}, setup_env={setup_env}, download_model={download_model}")

        if self.setup_env:
            logging.info("Setting up environment variables.")
            self.setup_environment()
        else:
            logging.info("Environment setup skipped.")

        if self.install_deps:
            logging.info("Installing dependencies.")
            self.install_dependencies()
        else:
            logging.info("Dependency installation skipped.")

        self.setup_model()

    def setup_environment(self):
        """Setup environment variables required for the model."""
        os.environ['OLLAMA_HOST'] = '0.0.0.0:11434'
        os.environ['OLLAMA_ORIGINS'] = '*'
        os.environ["OLLAMA_NUM_THREADS"] = '2'
        os.environ["OLLAMA_CUDA"] = '1'
        os.environ["OLLAMA_MAX_LOADED"] = '2'
        os.environ["HUGGING_FACE_TOKEN"] = "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"

        login(os.environ["HUGGING_FACE_TOKEN"])
        logging.info("Environment variables set and Hugging Face login completed.")

    def install_dependencies(self):
        """Install required dependencies."""
        try:
            subprocess.run(["pip", "install", "llama-index-llms-ollama"], check=True)
            subprocess.run(["pip", "install", "llama-index"], check=True)
            subprocess.run(["pip", "install", "llama-index-embeddings-ollama"], check=True)
            subprocess.run(["pip", "install", "--upgrade", "llama-index"], check=True)
            subprocess.run(["pip", "install", "llama-index-embeddings-huggingface"], check=True)
            logging.info("Dependencies installed successfully.")
        except subprocess.CalledProcessError as e:
            logging.error(f"Error occurred during dependency installation: {e}")

        if self.download_model:
            try:
                subprocess.run(["ollama", "pull", "qwen2:1.5b"], check=True)
                logging.info("Model 'qwen2:1.5b' downloaded successfully.")
            except subprocess.CalledProcessError as e:
                logging.error(f"Error occurred while downloading model: {e}")
        else:
            logging.info("Model download skipped.")

    def setup_model(self):
        """Setup model and settings."""
        self.llm = Ollama(model="qwen2:1.5b", request_timeout=300.0)
        Settings.chunk_size = 512
        Settings.node_parser = SentenceSplitter(chunk_size=512, chunk_overlap=20)
        Settings.num_output = 512
        Settings.context_window = 3900
        Settings.llm = self.llm
        Settings.embed_model = HuggingFaceEmbedding(
            model_name="BAAI/bge-small-en-v1.5"
        )
        logging.info("Model and settings configured successfully.")