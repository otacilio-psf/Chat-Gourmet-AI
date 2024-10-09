import streamlit as st
import psycopg2
import os

@st.cache_resource
def get_conn():
    db_params = {
        "host": os.getenv("PGHOST"),
        "user": os.getenv("PGUSER"),
        "password": os.getenv("PGPASSWORD"),
        "dbname": os.getenv("PGDATABASE")
    }
    return psycopg2.connect(**db_params)


def insert_new_question(question_id, question, answer):
    insert_query = """
    INSERT INTO questions (question_id, question, answer)
    VALUES (%s, %s, %s);
    """
    with get_conn() as conn:
        with conn.cursor() as cur:        
            cur.execute(insert_query, (question_id, question, answer))
            conn.commit()

def update_thumbs(question_id, thumbs):
    update_query = """
    UPDATE questions
    SET thumbs = %s
    WHERE question_id = %s;
    """
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(update_query, (thumbs, question_id))
            conn.commit()