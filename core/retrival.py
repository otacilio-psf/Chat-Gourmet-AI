from qdrant_client import QdrantClient, models
from fastembed import TextEmbedding
import os


def init():
    url = os.getenv("QDRANT_URL")
    api_key = os.getenv("QDRANT_API_KEY")
    client = QdrantClient(url=url, api_key=api_key)

    collection_name = "recipes"

    return client, collection_name


class VectorSearcher:
    DENSE_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

    def __init__(self):
        client, collection_name = init()
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
            score_threshold=score_threshold,
        )
        document = [hit.payload["document"] for hit in search_result]
        return document


class HybridSearcher:
    DENSE_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

    def __init__(self):
        client, collection_name = init()
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
            score_threshold=score_threshold,
        )
        document = [hit.payload["document"] for hit in search_result]
        return document


if __name__ == "__main__":
    test_cases = [
        """
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
""".strip(),
    ]

    vector_searcher = VectorSearcher()
    v_result = vector_searcher.search(text=test_cases[3], limit=3)

    hybrid_searcher = HybridSearcher()
    h_result = hybrid_searcher.search(text=test_cases[3], limit=3)

    for i in range(3):
        print(v_result[i])
        print(10 * "=")
        print(h_result[i])
        print("\n\n")
