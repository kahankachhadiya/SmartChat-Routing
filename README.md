# SmartChat-Routing

A local chatbot application powered by **LLaMA models** and **ChromaDB** for memory.  
It features a **Tkinter-based UI**, multimodel routing, and persistent user profiles.  

---

## 🚀 Features
- Tkinter UI for easy interaction  
- Local LLaMA model inference via [llama-cpp-python](https://github.com/abetlen/llama-cpp-python)  
- ChromaDB vector memory for context retrieval  
- User profile management stored in JSON  
- Chat logging for tracking conversation history  
- Modular structure (router, loader, memory, etc.)  
- Multimodel routing for specialized handling of different tasks  

---

## ⚙️ Installation

### 1. Clone the Repository
git clone https://github.com/yourusername/CHAT_BOT.git
cd CHAT_BOT

### 2. Create a Virtual Environment (Recommended)

python -m venv venv
source venv/bin/activate   # On Linux/Mac
venv\Scripts\activate      # On Windows

### 3. Install Dependencies

pip install -r requirements.txt

### 4. Download Models

Inside the Models/ folder, you’ll find model download links.txt.
Follow the instructions to download the required .gguf model files and place them in the Models/ directory.

---

## ▶️ Usage

python main.py


This will launch the Tkinter-based GUI where you can start chatting with the bot.

---

## 🛠️ Requirements

Python 3.9+

At least 8 GB RAM recommended (more for larger LLaMA models)

A CPU/GPU supported by llama-cpp-python

---

## 📖 How It Works

1. Model Loading
      - loader.py initializes the LLaMA model from the Models/ directory.

2. Memory
      - memory.py uses ChromaDB to store embeddings of conversations, allowing the bot to “remember” past chats.

3. Routing & Multimodel Support
      - router.py decides how to process user input.
      - The bot can use multiple models simultaneously, each optimized for a different task:
      - A smaller, faster model can handle casual or short interactions.
      - A larger, more capable model is used for reasoning, summarization, or complex queries.
      - The routing logic determines which model to call based on the type of user request.

4. Logging
      - chat_logger.py saves all conversations for later review.

5. Profiles
      - profile_manager.py loads and saves settings in user_profile.json.

6. UI
      - ui.py provides a simple Tkinter window for chatting.

---

## 🤝 Contributing

1. Fork this repository
2. Create a new branch (git checkout -b feature-xyz)
3. Make your changes
4. Commit (git commit -m 'Add new feature')
5. Push (git push origin feature-xyz)
6. Open a Pull Request

---

## 📂 Project Structure

```plaintext
CHAT_BOT/
│── chat_logger.py          # Handles logging of chats
│── loader.py               # Loads models and embeddings
│── main.py                 # Entry point for running the chatbot
│── memory.py               # Manages memory storage and retrieval with ChromaDB
│── profile_manager.py      # Handles user profiles
│── router.py               # Routes user inputs to appropriate handlers or models
│── ui.py                   # Tkinter-based user interface
│── user_profile.json       # Stores user preferences/profile data
│
├── Models/
│   └── model download links.txt   # Instructions/links for downloading models
│
└── requirements.txt        # Python dependencies
