from json.decoder import JSONDecodeError
from retrival import HybridSearcher
from generation import LLM
import asyncio
import json


class ChatGourmet:
    def __init__(self):
        self._hybrid_searcher = HybridSearcher()
        self._llm = LLM()

    def _initialize_system_instructions(self, messages):
        system_init_msg = [
            {
                "role": "system",
                "content": """
    You are a helpful and expert recipe assistant.
    Your primary task is to provide creative and detailed cooking suggestions for a **single** recipe idea, and instructions.
    Use any recipes inside [CONTEXT]...[/CONTEXT] as inspiration, but feel free to expand and enhance your responses with your broader knowledge of culinary techniques, ingredient substitutions, and cooking methods.
    [CONTEXT]...[/CONTEXT] is for internal use only. Do **NOT** mention or refer to it in the response to the user.
    If the user asks about topics unrelated to food or cooking, politely inform them that you are designed exclusively for culinary-related questions, and for no reason provide information outside of this scope.
    Gently encourage the user to ask questions related to cooking, ingredients, or food preparation.
    """.strip(),
            }
        ]

        if messages[0]["role"] in ("system", "assistant"):
            return system_init_msg + messages[1:]
        else:
            return system_init_msg + messages

    def _prompt_template(self, user_question, search_results):
        template = """
    {user_question}

    [CONTEXT]
    {retrieved_recipes}
    [/CONTEXT]
    """.strip()

        retrieved_recipes = ""

        for i in range(len(search_results)):
            num = i + 1
            retrieved_recipes = (
                retrieved_recipes + f"recipe {num}:\n{search_results[i]}\n\n"
            )

        prompt = template.format(
            user_question=user_question, retrieved_recipes=retrieved_recipes
        ).strip()
        return prompt

    async def _query_rewrite(self, user_question):
        messages = [
            {
                "role": "system",
                "content": "You are an assistant whose task is to determine if the user's input is related to food recipes.\nYour task is to respond in the following JSON format based on the user's input:\n\n{\"search\": \"yes/no\", \"query\": \"Title: {title}\\nIngredients:\\n{ingredient 1}\\n{ingredient 2}\\n{ingredient n}\\nDirections:\\n{directions}\"}\n\nIf the input mentions specific ingredients, include them under 'Ingredients'. If the input references a type of dish (like 'cake', 'soup', etc.), add it under 'Title'. If a cooking method (like 'bake', 'fry', etc.) is mentioned, include it under 'Directions'. If the query is not related to food, recipes, or cooking, respond with 'search': 'no' and leave the 'query' field empty. Only include the sections that are relevant to the user's input. **NEVER** use any information outside user input. For example:\n\nUser input: 'I want to bake a cake.'\n\nResponse:\n{\"search\": \"yes\", \"query\": \"Title: cake\\nDirections: bake\"}\n\nUser input: 'What’s the weather today?'\n\nResponse:\n{\"search\": \"no\", \"query\": \"\"}",
            },
            {"role": "user", "content": f"user input: {user_question}"},
        ]

        result = await self._llm.chat(messages=messages)

        for _ in range(2):
            try:
                j_result = json.loads(result)
                if "search" in j_result:
                    return j_result
                else:
                    return {"search": "no"}
            except JSONDecodeError:
                result = f"{{{result}}}"

        return {"search": "no"}

    async def rag(self, messages, stream=False):
        messages = self._initialize_system_instructions(messages)

        user_question = messages.pop()
        query_decision = await self._query_rewrite(user_question["content"])

        if query_decision["search"] == "yes":
            search_results = await self._hybrid_searcher.search(
                text=query_decision["query"]
            )
            user_question["content"] = self._prompt_template(
                user_question["content"], search_results
            )
            messages.append(user_question)
            return await self._llm.chat(messages=messages, stream=stream)

        else:
            messages.append(user_question)
            return await self._llm.chat(messages=messages, stream=stream)


if __name__ == "__main__":
    import asyncio

    messages = [
        {
            "role": "user",
            "content": "I have only chicken, garlic, and tomatoes. What can I make with these?",
        }
    ]
    chat_gourmet = ChatGourmet()

    async def test():
        content = await chat_gourmet.rag(messages, stream=True)

        async for chunk in content:
            print(chunk, end="")

    asyncio.run(test())
