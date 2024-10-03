from qdrant_client import QdrantClient, models
from fastembed import TextEmbedding, SparseTextEmbedding
import os


def init():
    url = os.getenv("QDRANT_URL", "http://localhost:6333")
    api_key = os.getenv("QDRANT_API_KEY", None)
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

    def search(self, text: str, limit=5, score_threshold=None):
        vector = next(self.model.embed(text)).tolist()
        search_result = self.qdrant_client.query_points(
            collection_name=self.collection_name,
            query=vector,
            using="all-MiniLM-L6-v2",
            limit=limit,
            score_threshold=score_threshold,
        )
        documents = [hit.payload["document"] for hit in search_result.points]
        return documents


class HybridSearcher:
    DENSE_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
    SPARSE_MODEL = "Qdrant/bm42-all-minilm-l6-v2-attentions"

    def __init__(self):
        client, collection_name = init()
        self.collection_name = collection_name
        self.qdrant_client = client
        self.model = TextEmbedding(model_name=self.DENSE_MODEL)
        self.sparse_model = SparseTextEmbedding(model_name=self.SPARSE_MODEL)

    def search(self, text: str, limit=5, score_threshold=None):
        vector = next(self.model.query_embed(text))
        sparse_vector = next(self.sparse_model.query_embed(text))
        search_result = self.qdrant_client.query_points(
            collection_name=self.collection_name,
            prefetch=[
                models.Prefetch(
                    query=vector.tolist(), using="all-MiniLM-L6-v2", limit=2 * limit
                ),
                models.Prefetch(
                    query=sparse_vector.as_object(),
                    using="bm42-all-minilm-l6-v2-attentions",
                    limit=2 * limit,
                ),
            ],
            query=models.FusionQuery(fusion=models.Fusion.RRF),
            limit=limit,
            score_threshold=score_threshold,
        )
        documents = [hit.payload["document"] for hit in search_result.points]
        return documents


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
        "No-Bake Nut Cookies",
        "Chicken",
    ]
    vector_searcher = VectorSearcher()
    hybrid_searcher = HybridSearcher()
    for case in test_cases:
        print("\n\n", 8 * "=", "CASE", 8 * "=")
        print(case)

        v_result = vector_searcher.search(text=case, limit=3)
        h_result = hybrid_searcher.search(text=case, limit=3)

        for v in v_result:
            print(5 * "=", "Vector", 5 * "=")
            print(v)

        for h in h_result:
            print(5 * "=", "Hybrid", 5 * "=")
            print(h)
