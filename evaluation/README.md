# Evaluation module

In this module we will evaluate the knowledge base retrival and the RAG flow responses

For all cases we will use a set of 450 synthetic questions, generated on `chatgpt-4o` web interface and can be found in `synthetic-questions.csv`, as for a generic questions as "What I can do with chiken and tomates" could bring relevant but unespected documents/recipes

## Retrival

For retrival we will evaluate the direct question and the rewrite query function used in our rag workflow

### Steps

As we don't have a proper Ground-thruth (one question can have multiple relevant recipes) we will:

1. Generate the answers for each retrival case
2. Use LLM-as-Judge to evaluate if the recipe is RELEVANT, PARTLY_RELEVANT or NON_RELEVANT for the question
3. Evaluate

### Metrics
- Precision@k (P@k): The proportion of relevant recipes retrieved in the top-k results
    - Since P@5 is a binary metric, we will treat RELEVANT as 1 and both PARTLY_RELEVANT and NON_RELEVANT as 0.
- Cumulative Weighted Relevance Normalized Score (CWRNS): Measures the relevance average score that reflects both the quantity and quality of relevant documents
    - In CWRNS we will treat RELEVANT as 1, PARTLY_RELEVANT  as 0.5 and NON_RELEVANT as 0.

### Results

#### VectorSearcher

- P@5: ``

- CWRNS: ``

#### HybridSearcher

- P@5: ``

- CWRNS: ``

### Query rewrite + HybridSearcher

- P@5: ``

- CWRNS: ``

## RAG Flow

For the RAG flow we will evaluate two different models

### Steps

1. Generate the answers for each retrival case
2. Use LLM-as-Judge to evaluate if the recipe is RELEVANT, PARTLY_RELEVANT or NON_RELEVANT for the question
3. Evaluate

### Metrics
- Relevance Distribution: Distribution of how relevant the answers are across the three categories
- Weighted Relevance Score: Provides a single value to summarize the overall performance

### meta-llama/Meta-Llama-3.1-8B-Instruct

- Relevance Distribution
    - x (y%) RELEVANT
    - x (y%) PARTLY_RELEVANT
    - x (y%) NON_RELEVANT

- Weighted Relevance Score: ``

### microsoft/Phi-3.5-mini-instruct

- Relevance Distribution
    - x (y%) RELEVANT
    - x (y%) PARTLY_RELEVANT
    - x (y%) NON_RELEVANT

- Weighted Relevance Score: ``

### Groq llama-3.1-70b-versatile

Groq rate limit we will run only 100 questions

- Relevance Distribution
    - x (y%) RELEVANT
    - x (y%) PARTLY_RELEVANT
    - x (y%) NON_RELEVANT

- Weighted Relevance Score: ``