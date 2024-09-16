# Chat Gourmet AI

<p align="center"><img src=".github/assets/cooking-robot.jpg" alt="Project Logo" width="300"></p>


Be creative to prepare our daily basis meal can be exautive, especially when you have a limited selection of ingredients.

The Chat Gourmet AI is here to simplify the process by generating recipes based on the ingredients you have on hand.

This project uses Retrieval-Augmented Generation (RAG) to provide tailored recipe suggestions, making meal planning easier and more enjoyable.


## Project Overview

Dataset used for Retrival is a sample of: [RecipeNLG](https://recipenlg.cs.put.poznan.pl/)

This project is splited in:
 - model-serve
 - vector-db
 - rag
 - ui

 Each of them contains unit of work pieces (and some specifics README)

### Note

This repo is for [Data Talks LLM Zoomcamp](https://github.com/DataTalksClub/llm-zoomcamp) project submission

## How to run this project

Prepare vector database, for it please check README inside vector-db

Serve llama 3.1 8b on Kaggle, for it please check README inside model-serve

Install dependencies

```bash
pip install -r rag/requirements.txt
```

To start the Open Ai compatible server

```bash
python rag/server.py
```

Query

```python
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

## Acknowledgements

- Open AI Compatible server was based in this [Towards Data Science publication](https://towardsdatascience.com/how-to-build-an-openai-compatible-api-87c8edea2f06)
