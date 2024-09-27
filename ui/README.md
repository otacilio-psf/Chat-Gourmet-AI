# Chat Gourmet AI

Chat Gourmet AI is a web-based chat application designed to assist users with cooking-related queries. Whether you're looking for recipe suggestions based on available ingredients, need tips on cooking techniques, or want to know about ingredient substitutions, this application is here to help!

## Features

- **Recipe Suggestions**: Provide ingredients and get recipe ideas based on what you have.
- **Cooking Tips**: Ask for cooking techniques or ingredient substitutions.
- **Real-time Responses**: Streamed responses for a more interactive experience.

## How to run

- Define Enviroment Variables:

```bash
export OPENAI_API_KEY="<your-key>"
export OPENAI_API_URL="<api-if-need>"
export OPENAI_MODEL_NAME="<model-name>"
```

- Start the server

```bash
uv sync --frozen

uv run streamlit run chatbot.py
```