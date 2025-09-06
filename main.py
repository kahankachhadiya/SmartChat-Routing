from loader import load_model
from router import route_prompt, update_loaded_model
from memory import store_memory, recall_memory
from chat_logger import create_chat_log, append_to_log
from profile_manager import load_profile, analyze_and_update_profile

user_profile = load_profile()

# State
first_message = True
session_buffer = []
MAX_TURNS = 6


def chat(prompt: str) -> str:
    global first_message, user_profile

    # 🔁 Route model
    route = route_prompt(prompt)
    update_loaded_model(route)
    model = load_model(route)
    print(f"[🔀 Routed to]: {route}")

    # 👤 Analyze user profile with current model
    user_profile = analyze_and_update_profile(user_profile, prompt, model)

    # 🧠 Recall memory context
    memory_context = recall_memory(prompt)
    memory_text = "\n".join(memory_context) if memory_context else ""

    # 🧠 Convert recent session into valid role-based format
    recent_session = []
    for role, msg in session_buffer[-MAX_TURNS:]:
        recent_session.append({
            "role": "user" if role == "You" else "assistant",
            "content": msg
        })

    # 💬 Build messages for chat completion
    messages = [{
        "role": "system",
        "content": f"""You are a helpful assistant who speaks in a clear, structured, and {user_profile['tone']} tone.

Instructions:
- Use bullet points when listing
- NEVER include phrases like "As an AI" or "Here's the output"
- End with a friendly follow-up question
- Provide honest answers and offer a workaround if needed.
- Dont use *Follow-up question:* ,  *smiles* or any other expression like this

Be brief and readable."""
    }]

    # 📚 Add context and user prompt
    context_parts = []
    if memory_text:
        context_parts.append(f"📜 Relevant memory:\n{memory_text}")
    if recent_session:
        context_parts.append("🕑 Recent conversation:\n" + "\n".join(
            [f"{m['role']}: {m['content']}" for m in recent_session]
        ))
    combined_input = "\n\n".join(context_parts + [prompt])
    messages.append({
        "role": "user",
        "content": combined_input
    })

    # 📂 Create chat log on first message
    if first_message:
        create_chat_log(route)
        first_message = False

    # 🧠 Generate assistant response
    try:
        response = model.create_chat_completion(
            messages=messages,
            max_tokens=1024,
            temperature=0.7,
        )
        raw_output = response["choices"][0]["message"]["content"].strip()
        print("✅ Model Output:", raw_output)
    except Exception as e:
        print("[❌ Model generation error]:", e)
        raw_output = "[Error generating response]"

    final_output = raw_output

    # 💾 Store memory
    store_memory(prompt, source="user")
    store_memory(final_output, source="assistant")

    # 🧠 Update session
    session_buffer.append(("You", prompt))
    session_buffer.append(("Assistant", final_output))

    # 📝 Log conversation
    append_to_log("You", prompt)
    append_to_log("Assistant", final_output)

    return final_output
