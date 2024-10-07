import streamlit as st
from connection import stream_response

st.set_page_config(page_title="Chat Gourmet AI", page_icon="🍔", layout="centered")

st.title("💬🍔🤖 Chat Gourmet AI")
st.caption("🚀 A RAG application to help you cook")

if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {
            "role": "assistant",
            "content": "I can help you create meals with your ingredients. Share what you have, and I’ll suggest recipes. For cooking tips or substitutions, just ask!",
        }
    ]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    st.chat_message("assistant").write_stream(stream_response)

    st.session_state.messages.append(
        {"role": "assistant", "content": st.session_state["full_response"]}
    )
