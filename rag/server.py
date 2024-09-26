# https://towardsdatascience.com/how-to-build-an-openai-compatible-api-87c8edea2f06
import json
import time
import uvicorn

from typing import Optional, List

from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from fastapi import FastAPI

from rag import rag

app = FastAPI(title="OpenAI-compatible API")


# Data models
class Message(BaseModel):
    role: str
    content: str


class ChatCompletionRequest(BaseModel):
    model: Optional[str] = "unknow"
    messages: List[Message]
    stream: Optional[bool] = False
    # max_tokens: Optional[int] = 512
    # temperature: Optional[float] = 0.1


async def _resp_async_generator(request: ChatCompletionRequest, resp_content: str):
    for i, token in enumerate(resp_content):
        chunk = {
            "id": i,
            "object": "chat.completion.chunk",
            "created": time.time(),
            "model": request.model,
            "choices": [{"delta": {"content": token}}],
        }
        yield f"data: {json.dumps(chunk)}\n\n"
    yield "data: [DONE]\n\n"


@app.post("/v1/chat/completions")
async def chat_completions(request: ChatCompletionRequest):
    if not request.messages:
        resp_content = "No messages provided"

    messages = [
        {"role": message.role, "content": message.content}
        for message in request.messages
    ]
    resp_content = rag(messages, request.stream)

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


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
