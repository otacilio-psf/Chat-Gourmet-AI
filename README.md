# Chat Gourmet AI

<p align="center"><img src=".github/assets/cooking-robot.jpg" alt="Project Logo" width="300"></p>


Be creative to prepare our daily basis meal can be exautive, especially when you have a limited selection of ingredients.

The Chat Gourmet AI is here to simplify the process by generating recipes based on the ingredients you have on hand.

This project uses Retrieval-Augmented Generation (RAG) to provide tailored recipe suggestions, making meal planning easier and more enjoyable.

## Table of Contents

- [Chat Gourmet AI](#chat-gourmet-ai)
  - [Table of Contents](#table-of-contents)
  - [Project Overview](#project-overview)
    - [Note](#note)
  - [Project struture](#project-struture)
  - [Dataset](#dataset)
  - [How to run this project](#how-to-run-this-project)
    - [With Docker](#with-docker)
    - [Without Docker](#without-docker)
    - [Query to the endpoint](#query-to-the-endpoint)
    - [Chat with UI](#chat-with-ui)
  - [Acknowledgements](#acknowledgements)

## Project Overview

The Chat Gourmet AI is designed to exclusively help the user to get food recipes and tips

Use cases:
  - Recipe generation based on available ingridients
  - Recipe generation based on dish name or cooking method
  - Cooking tips and advices

### Note

This repo is for [Data Talks LLM Zoomcamp](https://github.com/DataTalksClub/llm-zoomcamp) project submission

## Project struture

This project is splited in:
 - model-serve
 - vector-db
 - rag
 - ui

Each of them contains unit of work pieces (and some specifics README)

## Dataset

Dataset used for Retrival is a sample of: [RecipeNLG](https://recipenlg.cs.put.poznan.pl/)

- Original 2M+ recipes
- Sample 350k recipes

## How to run this project

### With Docker

- Serve llama 3.1 8b on Kaggle, for it please check README inside model-serve

- Start docker compose

```bash
docker compose up --build
```

- Prepare vector database, for it please check README inside vector-db

### Without Docker

- Start and prepare vector database, for it please check README inside vector-db

- Serve llama 3.1 8b on Kaggle, for it please check README inside model-serve

Install dependencies

```bash
pip install -r rag/requirements.txt
```

Define Enviroment Variables
```bash
export NGROK_API_KEY="<your-ngrok-api-key>"
export HF_TOKEN="<your-gh-token>"

export LLM_SYSTEM="OPENAI"
export OPENAI_API_KEY="open-source-model"
export OPENAI_API_URL="ngrok"
export OPENAI_MODEL_NAME="ngrok"
```

To start the Open Ai compatible server

```bash
python rag/server.py
```

### Query to the endpoint

```python
from openai import OpenAI

client = OpenAI(
    base_url=f'http://localhost:8000/v1',
    api_key="not-need"
)

# For stream
content = client.chat.completions.create(
    model="not-need",
    messages=[{
        "role": "user",
        "content": "I have chicken, garlic, and tomatoes. What can I make with these?"
    }],
    stream=True,
)

for chunk in content:
    print(chunk.choices[0].delta.content, end="")

# Single response
content = client.chat.completions.create(
    model="not-need",
    messages=[{
        "role": "user",
        "content": "I have chicken, garlic, and tomatoes. What can I make with these?"
    }],
    stream=False,
)    

print(content.choices[0].message.content)

```

### Chat with UI

If you are using docker compose, you can access the UI at [`http://localhost:8501`](http://localhost:8501) and have a chat!

## Acknowledgements

- Open AI Compatible server was based in this [Towards Data Science publication](https://towardsdatascience.com/how-to-build-an-openai-compatible-api-87c8edea2f06)
