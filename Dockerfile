# Dockerfile
FROM python:3.9-slim

# Instala dependencias del sistema necesarias
RUN apt-get update && apt-get install -y curl ca-certificates

# Instala Ollama
RUN curl -o /tmp/ollama-install.sh https://ollama.ai/install.sh && \
    bash /tmp/ollama-install.sh && \
    rm /tmp/ollama-install.sh

# Agrega Ollama al PATH
ENV PATH="/root/.ollama/bin:${PATH}"

# Establece el directorio de trabajo
WORKDIR /app

# Copia los archivos de requerimientos
COPY requirements.txt .

# Instala las dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto del código
COPY . .

# Copia el script de entrada y dale permisos de ejecución
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Exponer el puerto
EXPOSE 8000

# Comando para ejecutar la API a través del script de entrada
CMD ["/entrypoint.sh"]