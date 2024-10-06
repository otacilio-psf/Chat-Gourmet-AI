from openai import OpenAI
import streamlit as st
import asyncio
import sys
import os

sys.path.append(os.path.abspath('../core'))

CONNECTION_MODE = os.getenv("CONNECTION_MODE", "OpenAIapi")
OPENAI_API_URL = os.getenv("OPENAI_API_URL")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_API_MODEL = os.getenv("OPENAI_API_MODEL")


if CONNECTION_MODE=="OpenAIapi":
    client = OpenAI(base_url=f"{OPENAI_API_URL}/v1", api_key=OPENAI_API_KEY)
elif CONNECTION_MODE=="direct":
    from rag import ChatGourmet
    chat_gourmet = ChatGourmet()
else:
    raise Exception("Missing or wrong connection mode")

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

async def get_async_response(messages):
    content = await chat_gourmet.rag(messages=messages, stream=True)

    async for chunk in content:
        yield chunk

def stream_response():
    st.session_state["full_response"] = ""
    request_msg = initialize_system_instructions(st.session_state.messages)
    
    if CONNECTION_MODE=="OpenAIapi":

        response = client.chat.completions.create(
            model=OPENAI_API_MODEL, messages=request_msg, stream=True
        )

        st.session_state["full_response"] = ""

        for chunk in response:
            content = chunk.choices[0].delta.content or ""
            st.session_state["full_response"] += content
            yield content

    elif CONNECTION_MODE=="direct":
        async_response = get_async_response(request_msg)
        while True:
            try:
                content = asyncio.run(async_response.__anext__())
                st.session_state["full_response"] += content
                yield content
            except StopAsyncIteration:
                break 
    