from fastapi import FastAPI, Depends, HTTPException
from fastapi.security.api_key import APIKeyHeader
from fastapi.responses import StreamingResponse
from typing import Optional, List
from pydantic import BaseModel
from rag import ChatGourmet
import uvicorn
import json
import time

app = FastAPI(title="Chat Gourmet AI - OpenAI-compatible API")
chat_gourmet = ChatGourmet()
API_KEY = "cg_123456789_key"

api_key_header = APIKeyHeader(name="Authorization", auto_error=False)


class Message(BaseModel):
    role: str
    content: str


class ChatCompletionRequest(BaseModel):
    model: Optional[str] = "unknow"
    messages: List[Message]
    stream: Optional[bool] = False


def verify_api_key(api_key: str = Depends(api_key_header)):
    if api_key is None:
        print("API key is missing")
        raise HTTPException(status_code=403, detail="API key is missing")
    if api_key != f"Bearer {API_KEY}":
        print(f"Invalid API key: {api_key}")
        raise HTTPException(status_code=403, detail="Could not validate API key")
    print(f"API key validated: {api_key}")


async def _resp_async_generator(request: ChatCompletionRequest, resp_content: str):
    id = 0
    async for token in resp_content:
        id += 1
        chunk = {
            "id": id,
            "object": "chat.completion.chunk",
            "created": time.time(),
            "model": request.model,
            "choices": [{"delta": {"content": token}}],
        }
        yield f"data: {json.dumps(chunk)}\n\n"
    yield "data: [DONE]\n\n"


@app.post("/v1/chat/completions", dependencies=[Depends(verify_api_key)])
async def chat_completions(request: ChatCompletionRequest):
    if not request.messages:
        resp_content = "No messages provided"

    messages = [
        {"role": message.role, "content": message.content}
        for message in request.messages
    ]
    resp_content = await chat_gourmet.rag(messages, request.stream)

    if request.stream:
        return StreamingResponse(
            _resp_async_generator(request, resp_content),
            media_type="application/x-ndjson",
        )

    return {
        "id": "1337",
        "object": "chat.completion",
        "created": time.time(),
        "model": request.model,
        "choices": [{"message": Message(role="assistant", content=resp_content)}],
    }


@app.get("/health")
async def health_check():
    return {"message": "success"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
