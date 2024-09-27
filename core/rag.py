from retrival import HybridSearcher
from generation import generate
import json

hybrid_searcher = HybridSearcher()


def initialize_system_instructions(messages):
    system_init_msg = [
        {
            "role": "system",
            "content": "You are a helpful and expert recipe assistant. Your primary task is to provide creative and detailed cooking suggestions for a single recipe idea, and instructions based only in the ingredients provided by the user, unless it asked to increment with others ingridients. Use any recipes in the CONTEXT as inspiration, but feel free to expand and enhance your responses with your broader knowledge of culinary techniques, ingredient substitutions, and cooking methods. If the user asks about topics unrelated to food or cooking, politely inform them that you are designed exclusively for culinary-related questions, and avoid providing information outside of this scope. Gently encourage the user to ask questions related to cooking, ingredients, or food preparation.",
        }
    ]

    if messages[0]["role"] in ("system", "assistant"):
        return system_init_msg + messages[1:]
    else:
        return system_init_msg + messages


def prompt_template(user_question, search_results):
    template = """
User Input:
{user_question}

Context:
{retrieved_recipes}
Instructions for the model:
Use the recipes in the CONTEXT as inspiration to answer the user's question, but also incorporate your own culinary knowledge to provide a complete and creative response. Be sure to include ingredients and step-by-step instructions, and feel free to offer substitutions or tips for variety.
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


def query_rewrite(user_question):
    messages = [
        {
            "role": "system",
            "content": "You are an assistant whose task is to determine if the user's input is related to food recipes. Recipe documents are structured as follows:\n\nTitle: {title}\nIngredients: {ingredient 1}\n{ingredient 2}\n{ingredient n}\nDirections: {directions}\n\nYour task is to respond in the following JSON format based on the user's input:\n\n{\"search\": \"yes/no\", \"query\": \"Title: {title}\\nIngredients:\\n{ingredient 1}\\n{ingredient 2}\\n{ingredient n}\\nDirections:\\n{directions}\"}\n\nIf the input mentions specific ingredients, include them under 'Ingredients'. If the input references a type of dish (like 'cake', 'soup', etc.), add it under 'Title'. If a cooking method (like 'bake', 'fry', etc.) is mentioned, include it under 'Directions'. If the query is not related to food, recipes, or cooking, respond with 'search': 'no' and leave the 'query' field empty. Only include the sections that are relevant to the user's input. For example:\n\nUser input: 'I want to bake a cake.'\n\nResponse:\n{\"search\": \"yes\", \"query\": \"Title: cake\\nDirections: bake\"}\n\nUser input: 'What’s the weather today?'\n\nResponse:\n{\"search\": \"no\", \"query\": \"\"}",
        },
        {"role": "user", "content": user_question},
    ]

    result = generate(messages=messages)

    try:
        j_result = json.loads(result)
        if "search" in j_result:
            return j_result
        else:
            return {"search": "no"}
    except Exception:
        return {"search": "no"}


def rag(messages, stream=False):
    messages = initialize_system_instructions(messages)

    user_question = messages.pop()
    query_decision = query_rewrite(user_question["content"])

    if query_decision["search"] == "yes":
        search_results = hybrid_searcher.search(text=query_decision["query"])
        user_question["content"] = prompt_template(
            user_question["content"], search_results
        )
        messages.append(user_question)
        return generate(messages=messages, stream=stream)

    else:
        messages.append(user_question)
        return generate(messages=messages, stream=stream)


if __name__ == "__main__":
    messages = [
        {
            "role": "user",
            "content": "I have chicken, garlic, and tomatoes. What can I make with these?",
        }
    ]

    content = rag(messages, stream=True)

    for chunk in content:
        print(chunk, end="")
