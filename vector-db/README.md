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
    qdrant/qdrant:v1.11.3
```

This command will start a Qdrant container, mapping port 6333 for communication and mounting a local directory for persistent storage.

### Cloud Deployment

To deploy Qdrant in the cloud, you can use their managed cloud service. Sign up for an account on the [Qdrant Cloud](https://qdrant.tech/) platform. Once you have your account set up, you can create and configure a new Qdrant instance through the web interface.

After setting up your instance, you'll receive a URL and API key that you can use to interact with your Qdrant deployment.

## Load data

### Local Load

To load data into your local Qdrant instance, use the following command:

```bash
python load_data_batch.py
```

This command will load a dataset of size 350,000 into your local instance.

### Cloud Load

For loading data into a Qdrant cloud instance, use the command below, replacing `<paste-your-url-here>` and `<paste-your-api-key-here>` with your actual URL and API key:

```bash
python load_data_batch.py --url <paste-your-url-here> --api_key <paste-your-api-key-here>
```

This will upload the dataset to the cloud service, allowing you to work with it in a hosted environment.

## Pre-Embedded Dataset

Locally, embedding the data and loading it into the vector database (Qdrant) was taking too much time.

To address this, I pre-processed the embeddings using Kaggle with GPU support. The embeddings were then uploaded to Hugging Face using the notebook `recipe-short-embeddings-gpu.ipynb`. After that, the data was loaded into Qdrant using the script `load_data_pre_embedded.py`.

While `load_data_batch.py` works correctly, it was time-consuming to run locally without a GPU.

You can find the processed data set at [otacilio-psf/recipe_short_embeddings](https://huggingface.co/datasets/otacilio-psf/recipe_short_embeddings)

## Full text index

To eneable full text filter (similar to full text search) we need to index the metadata columns after load it
