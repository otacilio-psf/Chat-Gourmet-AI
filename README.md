# Chat Gourmet AI

<p align="center"><img src=".github/assets/cooking-robot.jpg" alt="Project Logo" width="300"></p>


Being creative with daily meals can be exhausting, especially when you have a limited selection of ingredients.

The Chat Gourmet AI is here to simplify the process by generating recipes based on the ingredients you have on hand. Meal planning just got easier and more enjoyable!

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
  - [Built With](#built-with)
  - [Acknowledgements](#acknowledgements)

## Project Overview

Chat Gourmet AI is designed to exclusively help users find food recipes and cooking tips based on the ingredients they have.

Use cases:
  - Recipe generation based on available ingridients
  - Recipe generation based on dish name or cooking method
  - Cooking tips and advice

### Note

This repo is a project submission for the [Data Talks LLM Zoomcamp](https://github.com/DataTalksClub/llm-zoomcamp)

## Project struture

This project is divided into the following components:

 - model-serve
 - vector-db
 - core
 - ui

Each component can be runned standalone and can have its own README with specific instructions.

## Dataset

Dataset used for retrival is a sample of: [RecipeNLG](https://recipenlg.cs.put.poznan.pl/)

- Original: 2M+ recipes
- Sample: 350k recipes

## How to run this project

### With Docker

- Serve LLaMA 3.1 8B on Kaggle. Please refer to the README inside the `model-serve` directory for instructions.

- Define Enviroment Variables:

```bash
export NGROK_API_KEY="<your-ngrok-api-key>"
export HF_TOKEN="<your-gh-token>"
```

- Start docker compose:

```bash
docker compose up --build
```

- Prepare the vector database. Refer to the README inside the `vector-db` directory.

### Without Docker

- Have [uv installed](https://docs.astral.sh/uv/getting-started/installation/)

- Start and prepare the vector database. Refer to the README inside the `vector-db` directory.

- Serve LLaMA 3.1 8B on Kaggle. Please refer to the README inside the `model-serve` directory for instructions.

- Define Enviroment Variables:

```bash
export NGROK_API_KEY="<your-ngrok-api-key>"
export HF_TOKEN="<your-gh-token>"

export LLM_SYSTEM="OPENAI"
export OPENAI_API_KEY="open-source-model"
export OPENAI_API_URL="ngrok"
export OPENAI_MODEL_NAME="ngrok"
```

- Start the OpenAI-compatible server:

```bash
cd core

uv sync --frozen

uv run server.py
```

### Query to the endpoint

Example of how to query the API using Python:

```python
from openai import OpenAI

client = OpenAI(
    base_url=f'http://localhost:8000/v1',
    api_key="not-need"
)

# Streamed response
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

If using Docker Compose, you can access the UI at [`http://localhost:8501`](http://localhost:8501) and have a chat!

## Built With

This project leverages the following technologies:

- [Qdrant](https://qdrant.tech/documentation/) - A vector search database for efficient storage and retrieval of high-dimensional data.
- [OpenAI API](https://platform.openai.com/docs/api-reference/introduction) - Provides a standart way to interact with LLM models.
- [FastAPI](https://fastapi.tiangolo.com/) - A modern, fast web framework for building the API endpoint.
- [Streamlit](https://docs.streamlit.io/) - A framework for building interactive and user-friendly web interfaces, used for the project UI.
- [uv](https://docs.astral.sh/uv/) - An extremely fast Python package and project manager, written in Rust


## Acknowledgements

- The OpenAI-compatible server was based on this [Towards Data Science publication](https://towardsdatascience.com/how-to-build-an-openai-compatible-api-87c8edea2f06)
