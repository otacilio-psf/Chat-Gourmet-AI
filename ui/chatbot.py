# chatbot.py
from openai import OpenAI
import streamlit as st
import requests
import time
import os

def stream_response():
    request_msg = system_init_msg + st.session_state.messages[1:]

    response = client.chat.completions.create(model=OPENAI_API_MODEL, messages=request_msg, stream=True)
    
    st.session_state["full_response"] = ""

    for chunk in response:
        content = chunk.choices[0].delta.content or ""
        st.session_state["full_response"] += content
        yield content


OPENAI_API_URL = os.getenv("OPENAI_API_URL")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_API_MODEL = os.getenv("OPENAI_API_MODEL")

client = OpenAI(
    base_url=f'{OPENAI_API_URL}/v1',
    api_key=OPENAI_API_KEY
)

st.set_page_config(page_title="Chat Gourmet AI", page_icon="🍔", layout="centered")

st.title("💬🍔🤖 Chat Gourmet AI")
st.caption("🚀 A RAG application to help you cook")

system_init_msg = [
    {
        "role": "system",
        "content": "You are a helpful recipe assistant. Your primary task is to provide one cooking suggestions and instructions based only in the ingredients provided by the user. Focus solely on culinary-related topics, such as recipe ideas, ingredient substitutions, or cooking techniques. If the user asks about topics unrelated to food or cooking, politely inform them that it is beyond your expertise, and redirect them to ask about recipes or cooking."
    }
]

if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {
        "role": "assistant",
        "content": "I can help you create meals with your ingredients. Share what you have, and I’ll suggest recipes. For cooking tips or substitutions, just ask!"
        }
    ]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():

    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    st.chat_message("assistant").write_stream(stream_response)

    st.session_state.messages.append({"role": "assistant", "content": st.session_state["full_response"]})