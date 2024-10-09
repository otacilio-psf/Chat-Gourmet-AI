from openai import OpenAI
import streamlit as st
import os

OPENAI_API_URL = os.getenv("OPENAI_API_URL")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL_NAME = os.getenv("OPENAI_MODEL_NAME")


@st.cache_resource
def get_client():
    return OpenAI(base_url=f"{OPENAI_API_URL}/v1", api_key=OPENAI_API_KEY)


client = get_client()


def initialize_system_instructions(messages):
    system_init_msg = [
        {
            "role": "system",
            "content": """
You are a helpful and expert recipe assistant.
Your primary task is to provide creative and detailed cooking suggestions for a **single** recipe idea, and instructions.
If the user asks about topics unrelated to food or cooking, politely inform them that you are designed exclusively for culinary-related questions, and for no reason provide information outside of this scope.
Gently encourage the user to ask questions related to cooking, ingredients, or food preparation.
""".strip(),
        }
    ]

    if messages[0]["role"] in ("system", "assistant"):
        return system_init_msg + messages[1:]
    else:
        return system_init_msg + messages


def stream_response():
    st.session_state["full_response"] = ""
    request_msg = initialize_system_instructions(st.session_state.messages)

    response = client.chat.completions.create(
        model=OPENAI_MODEL_NAME, messages=request_msg, stream=True
    )

    st.session_state["full_response"] = ""

    for chunk in response:
        content = chunk.choices[0].delta.content or ""
        st.session_state["full_response"] += content
        yield content
