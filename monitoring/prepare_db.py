from datetime import datetime, timedelta, timezone
from psycopg2 import sql
import polars as pl
import numpy as np
import psycopg2
import random
import os


db_params = {
    "host": os.getenv("PGHOST"),
    "user": os.getenv("PGUSER"),
    "password": os.getenv("PGPASSWORD"),
    "dbname": os.getenv("PGDATABASE"),
    "port": os.getenv("PGPORT", 5432),
}

conn = psycopg2.connect(**db_params)
cur = conn.cursor()


def check_table_exists(table_name):
    query = sql.SQL(
        "SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = %s);"
    )
    cur.execute(query, (table_name,))
    return cur.fetchone()[0]


def drop_table_if_exists(table_name):
    if check_table_exists(table_name):
        drop_query = sql.SQL("DROP TABLE IF EXISTS {} CASCADE;").format(
            sql.Identifier(table_name)
        )
        cur.execute(drop_query)
        conn.commit()
        print(f"Table '{table_name}' dropped.")


def create_table():
    cur.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp";')

    create_table_query = """
    CREATE TABLE questions (
        question_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
        question TEXT NOT NULL,
        answer TEXT NOT NULL,
        thumbs INT DEFAULT 0,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """
    cur.execute(create_table_query)
    conn.commit()
    print("Table 'questions' created.")


# Function to insert initial data
def insert_initial_data():
    df = pl.read_csv("../evaluation/dataset/Llama-3.1-8B-veredict.csv")

    timestamp_list = [
        datetime.now(timezone.utc)
        - timedelta(days=random.randint(0, 5), seconds=random.randint(0, 86400))
        for i in range(df.height)
    ]
    random_choices = np.random.choice([1, 1, 0], size=df.height)

    df = (
        df.with_columns(
            pl.when(pl.col("relevance") == "RELEVANT")
            .then(random_choices)
            .otherwise(-1)
            .alias("thumbs"),
            pl.Series(name="timestamp", values=timestamp_list),
        )
        .sort("timestamp")
        .select(["question", "answer", "thumbs", "timestamp"])
    )

    initial_data = df.to_dicts()
    initial_data = [tuple(d.values()) for d in initial_data]

    insert_query = """
    INSERT INTO questions (question, answer, thumbs, timestamp)
    VALUES (%s, %s, %s, %s);
    """

    cur.executemany(insert_query, initial_data)
    conn.commit()
    print("Initial data inserted into 'questions' table.")


try:
    drop_table_if_exists("questions")
    create_table()
    insert_initial_data()

finally:
    cur.close()
    conn.close()
