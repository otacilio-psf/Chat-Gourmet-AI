# Evaluation module

In this module we will evaluate the knowledge base retrival and the RAG flow responses

For both cases we will use a set of 450 synthetic questions, generated on `chatgpt-4o` web interface and can be found in `synthetic-questions.csv`, as for a generic questions as "What I can do with chiken and tomates" could bring relevant but unespected documents/recipes

## Retrival

For retrival we will evaluate the direct question and the rewrite query function used in our rag workflow

### Direct question

- x (y%) RELEVANT
- x (y%) PARTLY_RELEVANT
- x (y%) NON_RELEVANT

### Query rewrite

- x (y%) RELEVANT
- x (y%) PARTLY_RELEVANT
- x (y%) NON_RELEVANT

## RAG Flow

For the RAG flow we will evaluate with different models

### meta-llama/Meta-Llama-3.1-8B-Instruct

- x (y%) RELEVANT
- x (y%) PARTLY_RELEVANT
- x (y%) NON_RELEVANT

### microsoft/Phi-3.5-mini-instruct

- x (y%) RELEVANT
- x (y%) PARTLY_RELEVANT
- x (y%) NON_RELEVANT

### microsoft/Phi-3-medium-4k-instruct

- x (y%) RELEVANT
- x (y%) PARTLY_RELEVANT
- x (y%) NON_RELEVANT

### bartowski/Phi-3-medium-128k-instruct-GGUF - Q8_0

- x (y%) RELEVANT
- x (y%) PARTLY_RELEVANT
- x (y%) NON_RELEVANT

### Groq llama-3.1-70b-versatile

Groq rate limit we will run only 100 questions

- x (y%) RELEVANT
- x (y%) PARTLY_RELEVANT
- x (y%) NON_RELEVANT
