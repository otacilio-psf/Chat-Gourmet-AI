# Chat Gourmet AI

<p align="center"><img src=".github/assets/cooking-robot.jpg" alt="Project Logo" width="300"></p>


Being creative with daily meals can be exhausting, especially when you have a limited selection of ingredients.

The Chat Gourmet AI is here to simplify the process by generating recipes based on the ingredients you have on hand. Meal planning just got easier and more enjoyable!

This project uses Retrieval-Augmented Generation (RAG) to provide tailored recipe suggestions!

## Access the Chat Gourmet AI

You can access the app at [https://chat-gourmet-ai.streamlit.app](https://chat-gourmet-ai.streamlit.app)

## Table of Contents

- [Chat Gourmet AI](#chat-gourmet-ai)
  - [Access the Chat Gourmet AI](#access-the-chat-gourmet-ai)
  - [Table of Contents](#table-of-contents)
  - [Project Overview](#project-overview)
  - [Project Structure](#project-structure)
  - [Dataset](#dataset)
  - [How to run this project](#how-to-run-this-project)
    - [With Docker](#with-docker)
    - [Without Docker](#without-docker)
    - [Query to the endpoint](#query-to-the-endpoint)
    - [Chat with UI](#chat-with-ui)
  - [King of the Free-Tier Cloud Deployment](#king-of-the-free-tier-cloud-deployment)
    - [Services Used](#services-used)
      - [Groq Cloud](#groq-cloud)
      - [Qdrant Cloud](#qdrant-cloud)
      - [Render](#render)
      - [Streamlit Community Cloud](#streamlit-community-cloud)
  - [Built With](#built-with)
  - [Acknowledgements](#acknowledgements)

## Project Overview

Chat Gourmet AI is designed to exclusively help users find food recipes and cooking tips based on the ingredients they have.

Use cases:
  - Recipe generation based on available ingridients
  - Recipe generation based on dish name or cooking method
  - Cooking tips and advice


## Project Structure

This project is divided into the following components:

- core
  - Core code of the project, including the RAG module and an OpenAI API-compatible server. Refer to its README for more details.

- vector-db
  - Qdrant Vector Database preparation module. Check its README for instructions and retrieval details.

- ui
  - Web UI developed with Streamlit. See its README for more details.

- model-serve
  - A notebook designed for deployment on Kaggle using GPU to serve open-source LLM (with vLLM) and make it accessible via the internet (with Ngrok). Refer to its README for detailed instructions.

- evaluation
  - A notebook containing retrieval and RAG evaluation processes. Check its README for evaluation results and methodology.

- cloud-deployment
  - Folder with soft links to the necessary scripts, along with its own Python dependencies management file, to deploy to free tier services. Check its README for methodology and more details.

Each component can be run standalone and includes a README with specific instructions.

## Dataset

Dataset used for retrival is a sample of: [RecipeNLG](https://recipenlg.cs.put.poznan.pl/)

- Original: 2M+ recipes
- Sample: 350k recipes

## How to run this project

### With Docker

1. Serve LLaMA 3.1 8B on Kaggle. Please refer to the README inside the `model-serve` directory for instructions. Or you can use Groq free tier or OpenAI. 

2. Define Enviroment Variables:

   - Using `vllm-serve` on Kaggle:
     ```bash
     export NGROK_API_KEY="<your-ngrok-api-key>"
     export OPENAI_API_URL="ngrok"
     export OPENAI_API_KEY="open-source-model"
     export OPENAI_MODEL_NAME="ngrok"
     ```
   
   - Using OpenAi
     ```bash
     export NGROK_API_KEY=""
     export OPENAI_API_URL="openai"
     export OPENAI_API_KEY="<your-open-ai-key>"
     export OPENAI_MODEL_NAME="<choosed-model>"
     ```

   - Using Groq
     ```bash
     export NGROK_API_KEY=""
     export OPENAI_API_URL="https://api.groq.com/openai"
     export OPENAI_API_KEY="<your-groq-key>"
     export OPENAI_MODEL_NAME="<choosed-model>"
     ```

3. Start docker compose:

   ```bash
   docker compose up --build
   ```
   or
   ```bash
   make chat-gourmet
   ```
   or without the ui
   ```bash
   make chat-gourmet-server
   ```

4. Prepare the vector database. Refer to the README inside the `vector-db` directory.

### Without Docker

1. Have [uv installed](https://docs.astral.sh/uv/getting-started/installation/)

2. Start and prepare the vector database. Refer to the README inside the `vector-db` directory.
  - tip: To start Qdrant you can do `make qdrant` from root folder

3. Serve LLaMA 3.1 8B on Kaggle. Please refer to the README inside the `model-serve` directory for instructions. Or you can use Groq free tier or OpenAI.

4. Define Environment Variables:

   - Using `vllm-serve` on Kaggle:
     ```bash
     export NGROK_API_KEY="<your-ngrok-api-key>"
     export OPENAI_API_KEY="open-source-model"
     export OPENAI_API_URL="ngrok"
     export OPENAI_MODEL_NAME="ngrok"
     ```
   
   - Using OpenAi
     ```bash
     export OPENAI_API_KEY="<your-open-ai-key>"
     export OPENAI_MODEL_NAME="<choosed-model>"
     ```

   - Using Groq
     ```bash
     export OPENAI_API_URL="https://api.groq.com/openai"
     export OPENAI_API_KEY="<your-groq-key>"
     export OPENAI_MODEL_NAME="<choosed-model>"
     ```

5. Install Python Dependencies

   ```bash
   uv sync --frozen
   ```

6. Start the OpenAI-Compatible Server:

   ```bash
   uv run server.py
   ```


### Query to the endpoint

Example of how to query the API using Python:

```python
from openai import OpenAI

client = OpenAI(
    base_url=f'http://localhost:8000/v1',
    api_key="cg_123456789_key"
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

## King of the Free-Tier Cloud Deployment

This project aims to deploy a Chat Gourmet AI to the cloud using the free tier offerings from various cloud services.

You can access the app at [https://chat-gourmet-ai.streamlit.app](https://chat-gourmet-ai.streamlit.app)

You can connect to the server at [chat-gourmet-ai.streamlit.app](https://chat-gourmet-ai.onrender.com/)

As it use free tier the app can be un-available some times due rate limits.

### Services Used

#### [Groq Cloud](https://console.groq.com/docs/quickstart)

Groq Cloud offers a free tier with a generous rate limit for several open-source models, including Llama 3.1.

#### [Qdrant Cloud](https://qdrant.tech/pricing/)

Qdrant Cloud provides a sufficient free tier where we can host our vector database.

#### [Render](https://render.com/pricing/)

Render provides a sufficient free tier to deploy our FastApi server

#### [Streamlit Community Cloud](https://docs.streamlit.io/deploy/streamlit-community-cloud)

Streamlit Community Cloud allows you to publish public Streamlit apps for free.

## Built With

This project leverages the following technologies:

- [Qdrant](https://qdrant.tech/documentation/) - A vector search database for efficient storage and retrieval of high-dimensional data.
- [OpenAI API](https://platform.openai.com/docs/api-reference/introduction) - Provides a standart way to interact with LLM models.
- [FastAPI](https://fastapi.tiangolo.com/) - A modern, fast web framework for building the API endpoint.
- [Streamlit](https://docs.streamlit.io/) - A framework for building interactive and user-friendly web interfaces, used for the project UI.
- [uv](https://docs.astral.sh/uv/) - An extremely fast Python package and project manager, written in Rust


## Acknowledgements

- The OpenAI-compatible server was based on this [Towards Data Science publication](https://towardsdatascience.com/how-to-build-an-openai-compatible-api-87c8edea2f06)

- [LLM Zoomcamp](https://github.com/DataTalksClub/llm-zoomcamp) from  DataTalks.Club for the amazing content and lernings
