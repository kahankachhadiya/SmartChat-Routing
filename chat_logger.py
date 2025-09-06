import os
from datetime import datetime
import re

chat_dir = "history"
os.makedirs(chat_dir, exist_ok=True)

# Global variable for file path (set after first message)
chat_log_path = None

def create_chat_log(route: str):
    global chat_log_path
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Sanitize route to safe filename: only allow alphanumeric, dash, underscore
    safe_route = re.sub(r'[^a-zA-Z0-9_\-]', '_', route)

    filename = f"{safe_route}_chat_{timestamp}.txt"
    chat_log_path = os.path.join(chat_dir, filename)
    print(f"[📂 Chat log created: {chat_log_path}]")

def append_to_log(role: str, message: str):
    if not chat_log_path:
        raise RuntimeError("Chat log path not set. Call create_chat_log(route) first.")
    
    with open(chat_log_path, "a", encoding="utf-8") as f:
        f.write(f"{role}: {message}\n\n")