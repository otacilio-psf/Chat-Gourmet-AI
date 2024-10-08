from openai import AsyncOpenAI, OpenAI
import requests
import time
import os


def ngrok_url():
    NGROK_API_KEY = os.environ["NGROK_API_KEY"]

    headers = {"Authorization": f"Bearer {NGROK_API_KEY}", "Ngrok-Version": "2"}

    ngrok_response = requests.get("https://api.ngrok.com/tunnels", headers=headers)

    if ngrok_response.status_code == 200:
        if len(ngrok_response.json()["tunnels"]) == 1:
            return ngrok_response.json()["tunnels"][0]["public_url"]
        elif len(ngrok_response.json()["tunnels"]) == 0:
            raise Exception("No tunnels were found")
        else:
            raise Exception("More then one tunnels were found")
    else:
        raise Exception("Ngrok get tunnels error")


class LLM:
    OPENAI_API_URL = os.environ["OPENAI_API_URL"]
    OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]
    OPENAI_MODEL_NAME = os.environ["OPENAI_MODEL_NAME"]

    def __init__(self):
        self._get_openai_client()
        self._get_model()

    def _get_openai_client(self):
        if self.OPENAI_API_URL == "ngrok":
            self.OPENAI_API_URL = ngrok_url()

            timer = 0
            while True:
                if timer <= 3 * 60:
                    r = requests.get(f"{self.OPENAI_API_URL}/health")
                    if r.status_code == 200:
                        break
                    time.sleep(1)
                    timer += 1
                else:
                    raise Exception("LLM model via Ngrok timed out")

            self._client = AsyncOpenAI(
                base_url=f"{self.OPENAI_API_URL}/v1", api_key=self.OPENAI_API_KEY
            )

        elif self.OPENAI_API_URL == "openai":
            self._client = AsyncOpenAI()

        else:
            self._client = AsyncOpenAI(
                base_url=f"{self.OPENAI_API_URL}/v1", api_key=self.OPENAI_API_KEY
            )

    def _get_model(self):
        if self.OPENAI_MODEL_NAME == "ngrok":
            sync_client = OpenAI(
                base_url=f"{self.OPENAI_API_URL}/v1", api_key=self.OPENAI_API_KEY
            )
            model_list = sync_client.models.list()
            self._model_name = model_list.data[0].id
        else:
            self._model_name = self.OPENAI_MODEL_NAME

    async def _return_completion_stream(self, completion):
        async for chunk in completion:
            yield chunk.choices[0].delta.content or ""

    async def chat(self, messages, stream=False):
        completion = await self._client.chat.completions.create(
            model=self._model_name,
            messages=messages,
            stream=stream,
        )

        if stream:
            return self._return_completion_stream(completion)
        else:
            return completion.choices[0].message.content


if __name__ == "__main__":
    import asyncio

    messages = [
        {
            "role": "system",
            "content": "You are a helpful recipe assistant. Your primary task is to provide cooking one suggestions and instructions based only in the ingredients provided by the user. Focus solely on culinary-related topics, such as recipe ideas, ingredient substitutions, or cooking techniques. If the user asks about topics unrelated to food or cooking, politely inform them that it is beyond your expertise, and redirect them to ask about recipes or cooking.",
        },
        {
            "role": "user",
            "content": "I have chicken, garlic, and tomatoes. What can I make with these?",
        },
    ]

    llm = LLM()
    stream = True

    async def run_test():
        content = await llm.chat(messages=messages, stream=stream)

        if stream:
            async for chunk in content:
                print(chunk, end="")
        else:
            print(content)

    asyncio.run(run_test())
