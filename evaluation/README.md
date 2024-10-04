# Evaluation module

In this module we will evaluate the knowledge base retrival and the RAG flow responses

For all cases we will use a set of 450 synthetic questions, generated on `chatgpt-4o` web interface and can be found in `synthetic-questions.csv`.

As we don't have a proper Ground-thruth (one question can have multiple relevant recipes) we will use LLM-as-a-Judge to evaluate our questions and retrivals/answers.

As we have a lot data to judge (7650 records) we will use `microsoft/Phi-3.5-mini-instruct` to judge as it provides a two times `meta-llama/Meta-Llama-3.1-8B-Instruct` throughput

## Retrival

For retrival we will evaluate the direct question and the rewrite query function used in our rag workflow

### Steps

1. Generate the answers for each retrival case
2. Use LLM-as-a-Judge to evaluate if the recipe is RELEVANT, PARTLY_RELEVANT or NON_RELEVANT for the question
3. Evaluate

### Metrics
- Precision@k (P@K): The proportion of RELEVANT recipes retrieved in the top-k results
- Hit Rate (Hit@K): measures whether at least one RELEVANT document appears
- Cumulative Weighted Relevance Normalized Score (CWRNS@K): Measures the relevance average score that reflects both the quantity and quality of relevant documents
    - In CWRNS we will treat RELEVANT as 1, PARTLY_RELEVANT as 0.5 and NON_RELEVANT as 0.

### Results

#### VectorSearcher

K=3
- P@3: `47.04%`
- Hit@3: `77.33%`
- CWRNS@3: `66.59%`

K=5
- P@5: `45.87%`
- Hit@5: `77.33%`
- CWRNS@5: `65.42%`

#### HybridSearcher

K=3
- P@3: `44.59%`
- Hit@3: `76.00%`
- CWRNS@3: `64.00%`

K=5
- P@5: `41.87%`
- Hit@5: `76.00%`
- CWRNS@5: `61.67%`

### Query rewrite + HybridSearcher

K=3
- P@3: `41.56%`
- Hit@3: `73.78%`
- CWRNS@3: `62.44%`

K=5
- P@5: `40.13%`
- Hit@5: `73.78%`
- CWRNS@5: `61.42%`

## RAG Flow

For the RAG flow we will evaluate two different models

### Steps

1. Generate the answers for each retrival case
2. Use LLM-as-a-Judge to evaluate if the answer is RELEVANT, PARTLY_RELEVANT or NON_RELEVANT for the question
3. Evaluate

### Metrics
- Relevance Distribution: Distribution of how relevant the answers are across the three categories
- Weighted Relevance Score: Provides a single value to summarize the overall performance

### meta-llama/Meta-Llama-3.1-8B-Instruct

- RELEVANT: `99.33%`
- PARTLY_RELEVANT: `0.44%`
- NON_RELEVANT: `0.22%`
- Weighted Relevance Score: `99.56%`

### microsoft/Phi-3.5-mini-instruct

- RELEVANT: `99.78%`
- PARTLY_RELEVANT: `0.22%`
- NON_RELEVANT: `0.00%`
- Weighted Relevance Score: `99.89%`
