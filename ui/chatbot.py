import streamlit as st
from streamlit import session_state as ss
from uuid import uuid4

st.set_page_config(page_title="Chat Gourmet AI", page_icon="🍝", layout="centered")

from connection import stream_response
from db import insert_new_question, update_thumbs


st.title("💬🍝🤖 Chat Gourmet AI")
st.caption("🚀 A RAG application to help you cook")

ss["is_chat_input_disabled"] = ss.get("is_chat_input_disabled", False)
ss.commited_msg = ss.get("commited_msg", dict())
ss.feedback = ss.get("feedback", dict())

if "messages" not in ss:
    ss.messages = [
        {
            "role": "assistant",
            "content": "I can help you create meals with your ingredients. Share what you have, and I’ll suggest recipes. For cooking tips or substitutions, just ask!",
        }
    ]

def insert_msg_database(idx, msg):
    if msg["role"] == "assistant" and str(idx) not in ss.commited_msg:
        if idx != 0:
            question_id = str(uuid4())
            question = ss.messages[idx-1]["content"]
            answer = msg["content"]
            insert_new_question(question_id, question, answer)
            ss.commited_msg[str(idx)] = question_id

def user_feedback(idx, role):
    _, col1, col2 = st.columns([10, 1, 1])
    if role == "assistant" and str(idx) not in ss.feedback:
        if idx != 0:
            show_thanks = False
            question_id = ss.commited_msg[str(idx)]

            with col1:
                if st.button("👍", key=f"thumbs_up_{idx}"):
                    ss.feedback[str(idx)] = 1
                    with st.spinner("Registering feedback..."):
                        update_thumbs(question_id, 1)
                    show_thanks = True

            with col2:
                if st.button("👎", key=f"thumbs_down_{idx}"):
                    ss.feedback[str(idx)] = -1
                    with st.spinner("Registering feedback..."):
                        update_thumbs(question_id, -1)
                    show_thanks = True

            if show_thanks:
                st.success("Thank you for your feedback!")


for idx, msg in enumerate(ss.messages):
    st.chat_message(msg["role"]).write(msg["content"])
    insert_msg_database(idx, msg)
    user_feedback(idx, msg["role"])



if prompt := st.chat_input(disabled=ss.is_chat_input_disabled) or ss.is_chat_input_disabled:
    if not ss.is_chat_input_disabled:
        ss.messages.append({"role": "user", "content": prompt})
        ss.is_chat_input_disabled = True
        st.rerun()

    st.chat_message("assistant").write_stream(stream_response)

    ss.is_chat_input_disabled = False

    ss.messages.append({"role": "assistant", "content": ss["full_response"]})

    st.rerun()
