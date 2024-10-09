# README

This document will walk you through the steps necessary to configure and run the application using Docker, as well as how to make API requests using Postman. We will use the example we just developed to illustrate each step.

## Prerequisites

Before you begin, make sure you have the following components installed on your system:

- **Docker**: You can download and install it from the [official Docker site](https://www.docker.com).
- Git (optional)**: To clone the repository if necessary.
- Postman**: To make API requests. Download it from [Postman](https://www.postman.com/downloads/).

## Project Configuration

### 1. Clone or Download the Project

If you have Git installed, you can clone the repository:

```bash
git clone https://github.com/your_username/your_repository.git
cd your_repository
```
### 2. Build the container

At the root of the project, run the following command to build the image:

```bash
docker-compose build
```
After building the image, run the following command to start the container:

```bash
docker-compose up
```
### 3. When it is ready to use?
You must see in your terminal this result:
```bash
app-1  | 2024-10-03 15:38:42,520 - INFO - Model 'qwen2:1.5b' downloaded successfully.
app-1  | 2024-10-03 15:38:51,173 - INFO - Load pretrained SentenceTransformer: BAAI/bge-small-en-v1.5
app-1  | 2024-10-03 15:39:16,494 - INFO - 2 prompts are loaded, with the keys: ['query', 'text']
app-1  | 2024-10-03 15:39:16,624 - INFO - Model and settings configured successfully.
app-1  | INFO:     Started server process [24]
app-1  | INFO:     Waiting for application startup.
app-1  | INFO:     Application startup complete.
app-1  | INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```
## Using the API

Once the container is running and the API is available, you can interact with it using tools such as Postman or curl.

### 1. Upload Documents

Before starting a conversation, you need to load the documents and create the index.

Endpoint:

- Method: GET
- URL: http://localhost:8000/load_documents

Expected Response:
```bash
{
    "status": "Documents loaded and index created"
}
```
### 2. Start a Conversation
With the documents loaded, you can start a conversation between the doctor and the salesperson.

#### Endpoint:
- Method: POST
- URL: http://localhost:8000/start_conversation
- Headers:
    - Content-Type: application/json
    - Body (JSON):

```bash
{
  "company": "PharmaCorp",
  "mood": "Friendly",
  "product": "MedicinaX"
}
```
#### Parameters:
- company: pharmaceutical company name.
- mood: Doctor's mood (“Neutral”, “Friendly”, “In a hurry”, “Closed”).
- product: Name of the product to be presented.

#### Example result:
```bash
{
  "conversation": [
    {
      "role": "Doctor",
      "message": "Hello, I'm Dr. William, a general practitioner. What will you be presenting today?"
    },
    {
      "role": "Salesperson",
      "message": "Hello, Dr. William, I'm Mario from PharmaCorp. Today, I'll be discussing MedicinaX and how it could benefit your patients."
    },
    {
      "role": "Doctor",
      "message": "Could you tell me more about how MedicinaX compares to similar products on the market?"
    },
    {
      "role": "Salesperson",
      "message": "Certainly! MedicinaX has a unique formula that provides 30% greater efficacy compared to similar products due to its unique composition..."
    },
    {
      "role": "Doctor",
      "message": "Thank you for the information, Mario. I will definitely consider MedicinaX for my patients. Have a great day!"
    },
    {
      "role": "Salesperson",
      "message": "Thank you for your time, Dr. William. If you have any more questions, feel free to contact me. Have an excellent day!"
    }
  ],
  "total_time": 5.4321
}
```