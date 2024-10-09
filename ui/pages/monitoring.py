import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import psycopg2
import os

def load_data():
    db_params = {
        "host": os.getenv("PGHOST"),
        "user": os.getenv("PGUSER"),
        "password": os.getenv("PGPASSWORD"),
        "dbname": os.getenv("PGDATABASE"),
        "port": os.getenv("PGPORT", 5432),
    }
    conn = psycopg2.connect(**db_params)

    query = "SELECT question_id, question, answer, thumbs, timestamp FROM questions"
    data = pd.read_sql_query(query, conn)

    conn.close()

    data['date'] = pd.to_datetime(data['timestamp']).dt.date
    return data

data = load_data()

st.sidebar.header("Filter Options")
start_date = st.sidebar.date_input("Start Date", value=data['date'].min())
end_date = st.sidebar.date_input("End Date", value=data['date'].max())

filtered_data = data[(data['date'] >= start_date) & (data['date'] <= end_date)]

st.title("RAG System Feedback Dashboard")

# Metric 1: Total Number of Questions in Filtered Data
total_questions = filtered_data['question_id'].nunique()
st.subheader("Total Number of Questions")
st.metric("Total Number of Questions", total_questions, label_visibility="hidden")

# Metric 2: Feedback Distribution (Thumbs Up, Down, and No Feedback)
feedback_counts = (
    filtered_data['thumbs']
    .value_counts()
    .reindex([1, 0, -1], fill_value=0)
    .rename(index={1: 'Thumbs Up', 0: 'No Feedback', -1: 'Thumbs Down'})
)
st.subheader("Feedback Distribution")
st.bar_chart(feedback_counts)

# Metric 3: Average Feedback Score
average_feedback_score = filtered_data['thumbs'].replace(0, pd.NA).mean()
st.subheader("Average Feedback Score")
st.metric("Average Feedback Score", round(average_feedback_score, 2), label_visibility="hidden")
st.caption("""
The Average Feedback Score indicates general user satisfaction:
- **Closer to 1**: Mostly positive feedback (thumbs up)
- **Around 0**: Mixed or neutral feedback
- **Closer to -1**: Mostly negative feedback (thumbs down)
""")

# Metric 4: Feedback Over Time
st.subheader("Feedback Over Time")
feedback_over_time = (
    filtered_data.groupby(['date', 'thumbs'])
    .size()
    .unstack(fill_value=0)
)
feedback_over_time = feedback_over_time.rename(columns={1: 'Thumbs Up', 0: 'No Feedback', -1: 'Thumbs Down'})
st.line_chart(feedback_over_time)

# Metric 5: Word Cloud of Frequently Asked Words in Filtered Questions
st.subheader("Word Cloud of Common Words in Questions")
text = " ".join(filtered_data['question'].fillna("").tolist())
wordcloud = WordCloud(width=800, height=400, background_color="white").generate(text)
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
st.pyplot(plt)

# Additional Section: Most Recent Feedback (in the filtered data)
st.subheader("Most Recent Feedback")
recent_feedback = filtered_data[['timestamp', 'question', 'answer', 'thumbs']].sort_values(by='timestamp', ascending=False).head(5)
st.write(recent_feedback)