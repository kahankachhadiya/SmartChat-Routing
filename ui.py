import tkinter as tk
from tkinter import scrolledtext
import threading
from main import chat
from router import route_prompt

class ChatbotUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Terminal Chat")
        self.root.geometry("800x600")
        self.root.configure(bg="black")

        # Fonts & Colors
        self.font_family = "Segoe UI Emoji"  # Best for emojis + readable text
        self.font_size = 13
        self.text_color = "#FFFFFF"  # Terminal green
        self.bg_color = "#000000"    # Terminal black

        # Chat area (terminal output style)
        self.chat_area = scrolledtext.ScrolledText(
            root,
            wrap=tk.WORD,
            state='disabled',
            font=(self.font_family, self.font_size),
            bg=self.bg_color,
            fg=self.text_color,
            insertbackground=self.text_color
        )
        self.chat_area.pack(padx=10, pady=(10, 0), fill=tk.BOTH, expand=True)

        # Input area
        self.input_frame = tk.Frame(root, bg=self.bg_color)
        self.input_frame.pack(fill=tk.X, padx=10, pady=(5, 10))

        self.user_input = tk.Entry(
            self.input_frame,
            font=(self.font_family, self.font_size),
            bg=self.bg_color,
            fg=self.text_color,
            insertbackground=self.text_color,
            relief=tk.FLAT
        )
        self.user_input.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.user_input.bind("<Return>", self.send_message)

        self.send_button = tk.Button(
            self.input_frame,
            text="Send",
            command=self.send_message,
            font=(self.font_family, self.font_size),
            bg="#222222",
            fg=self.text_color,
            relief=tk.FLAT,
            activebackground="#444444",
            activeforeground="#00FF00"
        )
        self.send_button.pack(side=tk.RIGHT, padx=(10, 0))

    def send_message(self, event=None):
        user_text = self.user_input.get().strip()
        if user_text:
            self.append_chat("🧑 You", user_text)
            self.user_input.delete(0, tk.END)
            self.append_chat("🤖 Assistant", "💭 Assistant is thinking...", tag="thinking")
            threading.Thread(target=self.generate_response, args=(user_text,), daemon=True).start()

    def generate_response(self, user_input):
        try:
            model_used = route_prompt(user_input)
            bot_response = chat(user_input)
            if not bot_response.strip():
                bot_response = "[⚠️ Empty response from model]"
            self.remove_thinking()
            self.append_chat(f"🤖 Assistant [{model_used}]", bot_response)
        except Exception as e:
            self.remove_thinking()
            self.append_chat("❌ System", f"⚠️ Error: {e}")

    def append_chat(self, sender, message, tag=None):
        self.chat_area.config(state='normal')
        self.chat_area.insert(tk.END, f"{sender}: {message}\n\n", tag)
        self.chat_area.config(state='disabled')
        self.chat_area.yview(tk.END)

    def remove_thinking(self):
        self.chat_area.config(state='normal')
        text = self.chat_area.get("1.0", tk.END)
        if "💭 Assistant is thinking..." in text:
            self.chat_area.delete("end-3l", "end-1l")
        self.chat_area.config(state='disabled')


if __name__ == "__main__":
    root = tk.Tk()
    app = ChatbotUI(root)
    root.mainloop()