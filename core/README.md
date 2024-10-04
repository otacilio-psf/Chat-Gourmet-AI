# Core Module for Chat Gourmet AI

This module contains the RAG (Retrieval-Augmented Generation) logic for the Chat Gourmet AI project.

Since this module is integrated with a FastAPI web server, it uses asynchronous calls to ensure non-blocking operations.

## Modules

### `retrieval.py`

This module includes the **Vector** and **Hybrid** search classes, implemented asynchronously for efficient search retrieval.

### `generation.py`

This module defines the asynchronous **LLM** class, which automatically discovers how to connect to the LLM (Large Language Model) and parses the responses accordingly.

### `rag.py`

This is where the magic happens! The **ChatGourmet** class brings everything together, utilizing RAG to provide intelligent responses ✨🪄.

## To Run It Standalone

1. Install [uv](https://docs.astral.sh/uv/getting-started/installation/)

2. Define Environment Variables:

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
     export OPENAI_API_KEY="<your-groq-key>"
     export OPENAI_API_URL="https://api.groq.com/openai"
     export OPENAI_MODEL_NAME="<choosed-model>"
     ```

3. Install Python Dependencies

   ```bash
   uv sync --frozen
   ```

4. Start the OpenAI-Compatible Server:

   ```bash
   uv run server.py
   ```
