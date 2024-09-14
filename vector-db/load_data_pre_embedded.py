from qdrant_client import QdrantClient, models
from datasets import load_dataset
from itertools import islice
import threading
import argparse
import os

def init(args):
    if args.url:
        if args.api_key:
            client = QdrantClient(url=args.url, api_key=args.api_key)
        else:
            raise Exception("An API key is required when a URL is provided.")
    else:
        client = QdrantClient(url="http://localhost:6333")

    collection_name = "recipes"

    if client.collection_exists(collection_name):
        client.delete_collection(collection_name=collection_name)
        
        client.create_collection(
            collection_name=collection_name,
            vectors_config=models.VectorParams(
                size=384,
                distance=models.Distance.COSINE,
            )
        )
    else:
        client.create_collection(
            collection_name=collection_name,
            vectors_config=models.VectorParams(
                size=384,
                distance=models.Distance.COSINE,
            )
        )
    
    return client, collection_name

def batched(iterable, n):
    iterator = iter(iterable)
    while batch := list(islice(iterator, n)):
        yield batch

def load_data(client, collection_name):

    dataset = load_dataset(
        "otacilio-psf/recipe_short_embeddings", split="train", streaming=True
    ).select_columns(["id", "title", "NER", "document", "all-MiniLM-L6-v2"])

    batch_size = 100

    for batch in batched(dataset, batch_size):
        ids = [point.pop("id") for point in batch]
        vectors = [point.pop("all-MiniLM-L6-v2") for point in batch]

        client.upsert(
            collection_name=collection_name,
            points=models.Batch(
                ids=ids,
                vectors=vectors,
                payloads=batch,
            ),
        )



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Qdrant connection")

    parser.add_argument('--url', type=str, required=False, help='Qdrant Cloud url')
    parser.add_argument('--api_key', type=str, required=False, help='Qdrant Cloud api_key')

    args = parser.parse_args()
    
    class MockArgs:
        def __init__(self):
            self.url = False

    mock_args = MockArgs()
    mock_args.url = False

    client_local, collection_name = init(mock_args)
    client_cloud, _ = init(args)

    local_thread = threading.Thread(target=load_data, args=(client_local, collection_name,))
    local_thread.start()

    cloud_thread = threading.Thread(target=load_data, args=(client_cloud, collection_name,))
    cloud_thread.start()

    local_thread.join()
    cloud_thread.join()
