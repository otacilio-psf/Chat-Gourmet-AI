#https://towardsdatascience.com/how-to-build-an-openai-compatible-api-87c8edea2f06
import asyncio
import json
import time
import uvicorn

from typing import Optional, List

from pydantic import BaseModel
from starlette.responses import StreamingResponse
from fastapi import FastAPI

app = FastAPI(title="OpenAI-compatible API")


# Data models
class Message(BaseModel):
    role: str
    content: str


class ChatCompletionRequest(BaseModel):
    model: Optional[str] = "mock-gpt-model"
    messages: List[Message]
    max_tokens: Optional[int] = 512
    temperature: Optional[float] = 0.1
    stream: Optional[bool] = False


async def _resp_async_generator(request: ChatCompletionRequest, text_resp: str):
    tokens = text_resp.split(" ")

    for i, token in enumerate(tokens):
        chunk = {
            "id": i,
            "object": "chat.completion.chunk",
            "created": time.time(),
            "model": request.model,
            "choices": [{"delta": {"content": token + " "}}],
        }
        yield f"data: {json.dumps(chunk)}\n\n"
        await asyncio.sleep(1)
    yield "data: [DONE]\n\n"


@app.post("/chat/completions")
async def chat_completions(request: ChatCompletionRequest):
    if request.messages:
        resp_content = (
            "As a mock AI Assistant, I can only echo your last message: "
            + request.messages[-1].content
        )
    else:
        resp_content = "As a mock AI Assistant, I can only echo your last message, but there wasn't one!"

    if request.stream:
        return StreamingResponse(
            _resp_async_generator(request, resp_content), media_type="application/x-ndjson"
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
