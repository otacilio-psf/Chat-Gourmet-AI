from qdrant_client import QdrantClient
from tqdm import tqdm
import polars as pl
import argparse
import ast

def init(args):
    if args.url:
        if args.api_key:
            client = QdrantClient(url=args.url, api_key=args.api_key)
        else:
            raise Exception("An API key is required when a URL is provided.")
    else:
        client = QdrantClient(url="http://localhost:6333")

    client.set_model("sentence-transformers/all-MiniLM-L6-v2")
    client.set_sparse_model("prithivida/Splade_PP_en_v1")

    collection_name = "recipes"

    if client.collection_exists(collection_name):
        client.delete_collection(collection_name=collection_name)
        
        client.create_collection(
            collection_name=collection_name,
            vectors_config=client.get_fastembed_vector_params(),
            sparse_vectors_config=client.get_fastembed_sparse_vector_params(),  
        )
    else:
        client.create_collection(
            collection_name=collection_name,
            vectors_config=client.get_fastembed_vector_params(),
            sparse_vectors_config=client.get_fastembed_sparse_vector_params(),  
        )
    
    return client, collection_name

# 2M rows
# def parse_2M_dataset():
#     df = pl.read_parquet('hf://datasets/skadewdl3/recipe-nlg-llama2/data/train-*.parquet')

# 350k rows
def parse_350k_dataset():
    data = (
        pl.read_parquet('hf://datasets/rk404/recipe_short/final_recipes.parquet')
        .select(['title', 'ingredients', 'directions', 'NER'])
        .to_dicts()
    )

    metadata = []
    documents = []

    doc_template = """
Title: {title}
Ingredients:\n{ingredients}
Directions:\n{directions}
    """

    for d in tqdm(data, desc="Processing data", unit="row"):
        # Cleaning the data
        for key, value in d.items():
            if value.startswith('[') and value.endswith(']'):
                string_list_value = ast.literal_eval(value)
                list_value= [item.strip() for item in string_list_value]

                if key == "NER":
                    d[key] = list_value
                else:
                    d[key] = "\n".join(list_value)
            else:
                d[key] = value.strip()

        # prepare for Qdrant
        metadata.append({"title": d['title'],"NER": d['NER']})
        documents.append(doc_template.format(title=d['title'],ingredients=d['ingredients'],directions=d['directions']).strip())


    return metadata, documents

def load_data(client, collection_name, metadata, documents):
    client.add(
        collection_name=collection_name,
        documents=documents,
        metadata=metadata,
        ids=tqdm(range(len(documents)), desc="Loading data", unit="document"),
        parallel=0
    )

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Qdrant connection")

    parser.add_argument('--size', type=str, required=True, help='Possible values: 350k or 2M')
    parser.add_argument('--url', type=str, required=False, help='Qdrant Cloud url')
    parser.add_argument('--api_key', type=str, required=False, help='Qdrant Cloud api_key')

    args = parser.parse_args()

    client, collection_name = init(args)

    if args.size.lower() == "350k":
        metadata, documents = parse_350k_dataset()
    elif args.size.upper() == "2M":
        raise Exception("Work in progress")
    else:
        raise Exception("Size to available")
    
    load_data(client, collection_name, metadata, documents)
