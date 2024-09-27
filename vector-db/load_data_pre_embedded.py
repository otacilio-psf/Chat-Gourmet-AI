from qdrant_client import QdrantClient, models
from datasets import load_dataset
from itertools import islice
import argparse


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
            ),
        )
    else:
        client.create_collection(
            collection_name=collection_name,
            vectors_config=models.VectorParams(
                size=384,
                distance=models.Distance.COSINE,
            ),
        )

    if args.url:
        client.update_collection(
            collection_name=collection_name,
            vectors_config={"": models.VectorParamsDiff(on_disk=True)},
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
        for point in batch:
            point["ingredients_list"] = " ".join(point["NER"])
            del point["NER"]

        client.upsert(
            collection_name=collection_name,
            points=models.Batch(
                ids=ids,
                vectors=vectors,
                payloads=batch,
            ),
        )


def full_text_index(client, collection_name):
    client.create_payload_index(
        collection_name=collection_name,
        field_name="ingredients_list",
        field_schema=models.TextIndexParams(
            type="text",
            tokenizer=models.TokenizerType.WORD,
            min_token_len=2,
            max_token_len=15,
            lowercase=True,
        ),
    )

    client.create_payload_index(
        collection_name=collection_name,
        field_name="document",
        field_schema=models.TextIndexParams(
            type="text",
            tokenizer=models.TokenizerType.WORD,
            min_token_len=2,
            max_token_len=15,
            lowercase=True,
        ),
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Qdrant connection")

    parser.add_argument("--url", type=str, required=False, help="Qdrant Cloud url")
    parser.add_argument(
        "--api_key", type=str, required=False, help="Qdrant Cloud api_key"
    )

    args = parser.parse_args()

    client, collection_name = init(args)

    load_data(client, collection_name)

    full_text_index(client, collection_name)
