from openai import OpenAI
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


def get_openai_client(OPENAI_API_URL, OPENAI_API_KEY):
    if OPENAI_API_URL == "ngrok":
        OPENAI_API_URL = ngrok_url()

        timer = 0
        while True:
            if timer <= 3 * 60:
                r = requests.get(f"{OPENAI_API_URL}/health")
                if r.status_code == 200:
                    break
                time.sleep(1)
                timer += 1
            else:
                raise Exception("LLM model via Ngrok timed out")

        client = OpenAI(base_url=f"{OPENAI_API_URL}/v1", api_key=OPENAI_API_KEY)

        return client

    elif OPENAI_API_URL == "openai":
        client = OpenAI()
        return client

    else:
        client = OpenAI(base_url=f"{OPENAI_API_URL}/v1", api_key=OPENAI_API_KEY)

        return client


def return_completion_stream(completion):
    for chunk in completion:
        yield chunk.choices[0].delta.content or ""


class LLM:
    def __init__(self):
        OPENAI_API_URL = os.environ["OPENAI_API_URL"]
        OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]

        self._client = get_openai_client(OPENAI_API_URL, OPENAI_API_KEY)

        if os.environ["OPENAI_MODEL_NAME"] == "ngrok":
            self._model_name = self._client.models.list().model_dump()["data"][0][
                "id"
            ]
        else:
            self._model_name = os.environ["OPENAI_MODEL_NAME"]


    def chat(self, messages, stream=False):
        completion = self._client.chat.completions.create(
            model=self._model_name,
            messages=messages,
            stream=stream,
        )

        if stream:
            return return_completion_stream(completion)
        else:
            return completion.choices[0].message.content


if __name__ == "__main__":
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
    content = llm.chat(messages=messages, stream=stream)

    if stream:
        for chunk in content:
            print(chunk, end="")
    else:
        print(content)
