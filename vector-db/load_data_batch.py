from qdrant_client import QdrantClient
import polars as pl
import argparse
import ast
import gc

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

def load_data(client, collection_name, df):

    num_chunks = 3500
    chunk_size = len(df) // num_chunks

    for i in range(num_chunks):
        start_idx = i * chunk_size
        end_idx = (i + 1) * chunk_size if i != num_chunks - 1 else len(df)
        data = df[start_idx:end_idx].to_dict(as_series=False)
        client.add(
            collection_name=collection_name,
            documents=data['document'],
            metadata=data['metadata'],
            parallel=0
        )
    
        del data
        gc.collect()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Qdrant connection")

    parser.add_argument('--url', type=str, required=False, help='Qdrant Cloud url')
    parser.add_argument('--api_key', type=str, required=False, help='Qdrant Cloud api_key')

    args = parser.parse_args()

    client, collection_name = init(args)

    df = clean_350k_dataset()

    load_data(client, collection_name, df)
    