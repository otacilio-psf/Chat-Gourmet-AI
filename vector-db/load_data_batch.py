from qdrant_client import QdrantClient
from itertools import islice
import polars as pl
import argparse
import ast
import gc
import os

def init(args):
    if args.url:
        if args.api_key:
            client = QdrantClient(url=args.url, api_key=args.api_key)
        else:
            raise Exception("An API key is required when a URL is provided.")
    else:
        client = QdrantClient(url="http://localhost:6333")

    client.set_model("sentence-transformers/all-MiniLM-L6-v2")

    collection_name = "recipes"

    if client.collection_exists(collection_name):
        client.delete_collection(collection_name=collection_name)
        
        client.create_collection(
            collection_name=collection_name,
            vectors_config=client.get_fastembed_vector_params()
        )
    else:
        client.create_collection(
            collection_name=collection_name,
            vectors_config=client.get_fastembed_vector_params()  
        )
    
    return client, collection_name

# 350k rows
def clean_350k_dataset():
    
    def clean_data_structure(row):
        doc_template = """
Title: {title}
Ingredients:\n{ingredients}
Directions:\n{directions}
"""

        temp_data = list()
        new_row = list()

        for value in row:
            if value.startswith('[') and value.endswith(']'):
                string_list_value = ast.literal_eval(value)
                list_value= [item.strip() for item in string_list_value]
                temp_data.append(list_value)
            else:
                temp_data.append(value.strip())

        temp_data[1] = "\n".join(temp_data[1])
        temp_data[2] = "\n".join(temp_data[2])

        new_row.append({"title": temp_data[0],"NER": temp_data[3]})
        new_row.append(doc_template.format(title=temp_data[0],ingredients=temp_data[1],directions=temp_data[2]).strip())
        
        return tuple(new_row)
    
    return (
        pl.read_parquet('hf://datasets/rk404/recipe_short/final_recipes.parquet')
        .select(['title', 'ingredients', 'directions', 'NER'])
        .map_rows(clean_data_structure)
        .rename({"column_0": "metadata", "column_1": "document"})
    )

def batched(iterable, n):
    iterator = iter(iterable)
    while batch := list(islice(iterator, n)):
        yield batch

def load_data(client, collection_name, df):

    batch_size = 100

    for batch in batched(df.iter_rows(named=True), batch_size):
        documents = [point.pop("document") for point in batch]
        metadata = [point.pop("metadata") for point in batch]

        client.add(
            collection_name=collection_name,
            documents=documents,
            metadata=metadata,
            parallel=0
        )

        del documents
        del metadata
        gc.collect()



if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Qdrant connection")

    parser.add_argument('--url', type=str, required=False, help='Qdrant Cloud url')
    parser.add_argument('--api_key', type=str, required=False, help='Qdrant Cloud api_key')

    args = parser.parse_args()

    client, collection_name = init(args)

    df = clean_350k_dataset()

    load_data(client, collection_name, df)
