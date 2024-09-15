from qdrant_client import QdrantClient, models
from fastembed import TextEmbedding
import argparse

def init(url=None, api_key=None):
    if url:
        if api_key:
            client = QdrantClient(url=url, api_key=api_key)
        else:
            raise Exception("An API key is required when a URL is provided.")
    else:
        client = QdrantClient(url="http://localhost:6333")

    collection_name = "recipes"
    
    return client, collection_name


class VectorSearcher:
    DENSE_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
    def __init__(self, client, collection_name):
        self.collection_name = collection_name
        self.qdrant_client = client
        self.model = TextEmbedding(model_name=self.DENSE_MODEL)

    def search(self, text: str, limit=5, score_threshold=0.7):
        vector = next(self.model.embed(text)).tolist()
        search_result = self.qdrant_client.search(
            collection_name=self.collection_name,
            query_vector=vector,
            query_filter=None,
            limit=limit,
            score_threshold=score_threshold
        )
        document = [hit.payload['document'] for hit in search_result]
        return document


class HybridSearcher:
    DENSE_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
    def __init__(self, client, collection_name):
        self.collection_name = collection_name
        self.qdrant_client = client
        self.model = TextEmbedding(model_name=self.DENSE_MODEL)

    def search(self, text: str, limit=5, score_threshold=0.7):
        vector = next(self.model.embed(text)).tolist()
        search_result = self.qdrant_client.search(
            collection_name=self.collection_name,
            query_vector=vector,
            query_filter=models.Filter(
                must=models.FieldCondition(
                    key="document",
                    match=models.MatchText(text=text),
                )
            ),
            limit=limit,
            score_threshold=score_threshold
        )
        document = [hit.payload['document'] for hit in search_result]
        return document


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Qdrant connection")

    parser.add_argument('--url', type=str, required=False, help='Qdrant Cloud url')
    parser.add_argument('--api_key', type=str, required=False, help='Qdrant Cloud api_key')

    args = parser.parse_args()

    client, collection_name = init(url=args.url, api_key=args.api_key)

    test_cases = ["""
Ingredients:
chicken
tomato
onion
""".strip(),
"""
Title: Pizza
""".strip(),
"""
Directions:
make in the oven
""".strip(),
"""
Ingredients:
chicken
tomato
Directions:
make in the oven
""".strip()
    ]

    vector_searcher = VectorSearcher(client, collection_name=collection_name)
    v_result = vector_searcher.search(text=test_cases[3], limit=3)

    hybrid_searcher = HybridSearcher(client, collection_name=collection_name)
    h_result = hybrid_searcher.search(text=test_cases[3], limit=3)

    for i in range(3):
        print(v_result[i])
        print(10*"=")
        print(h_result[i])
        print("\n\n")
