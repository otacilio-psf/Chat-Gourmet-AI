# Vector Database

## Qdrant

Qdrant is a high-performance vector search engine designed for efficient similarity search in large-scale datasets. It provides advanced indexing and search capabilities, making it ideal for applications like recommendation systems, image search, and natural language processing. Qdrant supports a variety of similarity metrics and offers real-time search capabilities.

You can start using Qdrant with their free tier cloud service, which provides a generous allocation for development and testing purposes. This allows you to explore its features without incurring costs.

## Deployment

### Local Deployment

To deploy Qdrant locally using Docker, run the following command:

```bash
docker run -d \
    -p 6333:6333 \
    -v $(pwd)/qdrant_storage:/qdrant/storage \
    --ulimit nofile=10000:10000 \
    qdrant/qdrant:v1.11.3
```

This command will start a Qdrant container, mapping port 6333 for communication and mounting a local directory for persistent storage.

### Cloud Deployment

To deploy Qdrant in the cloud, you can use their managed cloud service. Sign up for an account on the [Qdrant Cloud](https://qdrant.tech/) platform. Once you have your account set up, you can create and configure a new Qdrant instance through the web interface.

After setting up your instance, you'll receive a URL and API key that you can use to interact with your Qdrant deployment.

## Load data

- Have [uv installed](https://docs.astral.sh/uv/getting-started/installation/)

Solve python dependencies:

```bash
uv sync --frozen
```

### Local Load

To load data into your local Qdrant instance, use the following command:

```bash
uv run load_data_pre_embedded.py
```

This command will load a dataset of size 350,000 into your local instance.

### Cloud Load

For loading data into a Qdrant cloud instance, use the following enviromental variables `QDRANT_URL` and `QDRANT_API_KEY`, replacing `<paste-your-url-here>` and `<paste-your-api-key-here>` with your actual URL and API key:

```bash
export QDRANT_URL=<paste-your-url-here>
export QDRANT_API_KEY=<paste-your-api-key-here>
uv run load_data_pre_embedded.py
```

This will upload the dataset to the cloud service, allowing you to work with it in a hosted environment.

## Pre-Embedded Dataset

Locally, embedding the data and loading it into the vector database (Qdrant) was taking too much time.

To address this, I pre-processed the embeddings using Kaggle with GPU support. The embeddings were then uploaded to Hugging Face using the notebook `recipe-short-embeddings-gpu.ipynb`.

To generate the embedding locally you can run

```bash
uv run load_data_batch.py
```

While `load_data_batch.py` works correctly, it was time-consuming to run locally without a GPU.

You can find the processed data set at [otacilio-psf/recipe_short_dense_and_sparse_embeddings](https://huggingface.co/datasets/otacilio-psf/recipe_short_dense_and_sparse_embeddings)

## Embedding models

- Dense Embeddings: Created using the sentence-transformers/all-MiniLM-L6-v2 model with fastembed library.
- Sparse Embeddings: Generated using the Qdrant/bm25-all-minilm-l6-v2-attentions model with fastembed library.

Sparse vector embedding model focuses on capturing the most important tokens from the text. It provides attention-based scores to highlight key terms, which can be beneficial for keyword-based search and sparse retrieval tasks.

## Hybrid Search

For the Hybrid search we are using the combination of Dense Vector search (Tradicional Vector search) and Sparse Vector search using [Reciprocal Rank Fusion*](https://plg.uwaterloo.ca/~gvcormac/cormacksigir09-rrf.pdf) to get the best of semantics, plus the best of matching specific words.

*Considers the positions of results within each query, and boosts the ones that appear closer to the top in multiple of them.