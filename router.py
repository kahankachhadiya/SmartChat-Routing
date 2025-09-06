from loader import load_model, MODELS

VALID_ROUTES = {
    "general", "code", "creative", "multilingual", "fast_facts",
    "tools", "doc_qa", "uncensored", "summarizer",
    "security", "data_analysis", "data_summary"
}

current_model_name = "general"
loaded_model = load_model(current_model_name)  # preload general

def route_prompt(prompt: str) -> str:
    global loaded_model, current_model_name

    router_model = load_model("general")  # always use general model for routing

    routing_prompt = f"""
You are a smart routing agent.

Your job is to read the user's message and classify it into exactly one of the following categories:
- general
- code
- creative
- multilingual
- fast_facts
- tools
- doc_qa
- uncensored
- summarizer
- security
- data_analysis
- data_summary

Respond with ONLY one word, the category name. No quotes, no punctuation, no explanation.

Message:
\"\"\"{prompt}\"\"\"
Response:"""

    try:
        result = router_model.create_completion(
            prompt=routing_prompt,
            max_tokens=8,
            temperature=0.2,
        )
        raw_route = result["choices"][0]["text"].strip()
        route = raw_route.lower().replace('"', '').replace("'", "").split()[0]
    except Exception as e:
        print(f"[❌ Routing error: {e}]")
        return "general"

    if route not in VALID_ROUTES:
        print(f"[⚠️ Invalid route '{raw_route}' — defaulting to 'general']")
        return "general"

    return route

def update_loaded_model(route: str):
    global current_model_name, loaded_model

    if route != current_model_name:
        loaded_model = load_model(route)
        current_model_name = route
