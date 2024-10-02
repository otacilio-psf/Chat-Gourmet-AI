from qdrant_client import QdrantClient, models
from datasets import load_dataset
from itertools import islice
from tqdm import tqdm
import os

QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY", None)

def init():

    client = QdrantClient(QDRANT_URL, api_key=QDRANT_API_KEY)

    collection_name = "recipes"

    if client.collection_exists(collection_name):
        client.delete_collection(collection_name=collection_name)

    client.create_collection(
        collection_name=collection_name,
        vectors_config={
            "all-MiniLM-L6-v2": models.VectorParams(
                size=384,
                distance=models.Distance.COSINE,
            )
        },
        sparse_vectors_config={
            "bm42-all-minilm-l6-v2-attentions": models.SparseVectorParams(
                modifier=models.Modifier.IDF,
            )
        },
    )

    if QDRANT_URL != "http://localhost:6333":
        client.update_collection(
            collection_name=collection_name,
            vectors_config={"all-MiniLM-L6-v2": models.VectorParamsDiff(on_disk=True)},
        )

    return client, collection_name


def batched(iterable, n):
    iterator = iter(iterable)
    while batch := list(islice(iterator, n)):
        yield batch


def load_data(client, collection_name):
    dataset = load_dataset(
        "otacilio-psf/recipe_short_dense_and_sparse_embeddings", split="train", streaming=True
    ).select_columns(["id", "title", "NER", "document", "all-MiniLM-L6-v2", "bm42-all-minilm-l6-v2-attentions"])

    batch_size = 100

    for batch in tqdm(batched(dataset, batch_size), total=int(350000/batch_size), desc="Loading data"):
        ids = [point.pop("id") for point in batch]
        vectors = [point.pop("all-MiniLM-L6-v2") for point in batch]
        sparse_vectors = []
        for point in batch:
            s_vector_dict = point.pop("bm42-all-minilm-l6-v2-attentions")
            s_vector = models.SparseVector(
                        values=s_vector_dict["values"],
                        indices=s_vector_dict["indices"]
                    )
            sparse_vectors.append(s_vector)
        for point in batch:
            point["ingredients_list"] = " ".join(point["NER"])
            del point["NER"]

        client.upsert(
            collection_name=collection_name,
            points=models.Batch(
                ids=ids,
                vectors={
                    "all-MiniLM-L6-v2": vectors,
                    "bm42-all-minilm-l6-v2-attentions": sparse_vectors
                },
                payloads=batch,
            ),
        )



if __name__ == "__main__":

    client, collection_name = init()

    load_data(client, collection_name)
