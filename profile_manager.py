import json
import os

PROFILE_PATH = "user_profile.json"

DEFAULT_PROFILE = {
    "name": "Kahan",
    "tone": "friendly",
    "hobbies": [],
    "interests": [],
    "expertise": [],
    "language": "en"
}

def load_profile():
    if not os.path.exists(PROFILE_PATH):
        save_profile(DEFAULT_PROFILE)
    with open(PROFILE_PATH, "r") as f:
        return json.load(f)

def save_profile(profile):
    with open(PROFILE_PATH, "w") as f:
        json.dump(profile, f, indent=2)

def analyze_and_update_profile(profile, user_message, model):
    prompt = f"""
You are a user profiler AI. Analyze the following message and update the user's tone, hobbies, interests, and areas of expertise if possible.

Return a JSON like:
{{
  "tone": "sarcastic",
  "hobbies": ["coding", "chess"],
  "interests": ["AI", "security"],
  "expertise": ["Python", "Ethical Hacking"]
}}

Only include fields that are clearly mentioned or implied by the message.
If nothing is relevant, return an empty JSON: {{}}

User Message:
\"\"\"{user_message}\"\"\"
JSON:"""

    try:
        response = model.create_completion(prompt=prompt, max_tokens=256)["choices"][0]["text"]
        json_start = response.find('{')
        json_end = response.rfind('}') + 1
        response_json = response[json_start:json_end]
        updates = json.loads(response_json)
    except Exception as e:
        print(f"[⚠️ Could not parse profile update]: {e}")
        return profile

    updated = False

    for key in ["tone", "hobbies", "interests", "expertise"]:
        if key in updates:
            if isinstance(updates[key], list):
                combined = list(set(profile.get(key, []) + updates[key]))
                if combined != profile.get(key, []):
                    profile[key] = combined
                    updated = True
            elif updates[key] != profile.get(key):
                profile[key] = updates[key]
                updated = True

    if updated:
        save_profile(profile)
        print("[✅ Profile updated]")
    else:
        print("[ℹ️ No meaningful profile updates found]")

    return profile
