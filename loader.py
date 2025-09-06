import os
import time
from llama_cpp import Llama

# 🛠️ Patch to suppress buggy __del__ cleanup error
def safe_del(self):
    try:
        self.close()
    except Exception:
        pass
Llama.__del__ = safe_del

MODELS = {
    "router": "./Models/tinyllama/tinyllama-1.1b-chat-v1.0.Q4_0.gguf",
    "general": "./Models/nemotron/llama-3.1-nemotron-nano-8b-v1-q4_k_m.gguf",
    "code": "./Models/deepseek/deepseek-coder-6.7b-instruct.Q6_K.gguf",
    "creative": "./Models/mythomax/mythomax-l2-13b.Q5_K_M.gguf",
    "multilingual": "./Models/openchat/openchat-3.5-0106.Q5_K_M.gguf",
    "fast_facts": "./Models/openhermes/openhermes-2.5-mistral-7b.Q6_K.gguf",
    "summarizer": "./Models/tinyllama/tinyllama-1.1b-chat-v1.0.Q4_0.gguf",
    "doc_qa": "./Models/mistralinstruct/mistral-7b-instruct-v0.2.Q6_K.gguf",
    "tools": "./Models/gemma/gemma-1.1-2b-it.Q4_K_M.gguf",
    "uncensored": "./Models/neuralbeagle/neuralbeagle14-7b.Q4_K_M.gguf",
    "security": "./Models/security/Foundation-Sec-8B.Q5_K_M.gguf",
    "data_analysis": "./Models/deepseek/deepseek-coder-6.7b-instruct.Q6_K.gguf",
    "data_summary": "./Models/openhermes/openhermes-2.5-mistral-7b.Q6_K.gguf",
}

loaded_models = {}
active_model_name = None  # Tracks the currently loaded non-router model

def unload_model(name):
    if name in loaded_models:
        try:
            print(f"[Unloading model: {name}]")
            del loaded_models[name]
        except Exception as e:
            print(f"[⚠️ Error unloading model '{name}']: {e}")
    else:
        print(f"[Model {name} not loaded]")

def load_model(name):
    global active_model_name

    # Check model file exists
    if name not in MODELS or not os.path.exists(MODELS[name]):
        raise FileNotFoundError(f"❌ Model path for '{name}' is missing or incorrect: {MODELS.get(name)}")

    # Load router model
    if name == "router":
        if "router" not in loaded_models:
            print("[Preloading router model]")
            try:
                loaded_models["router"] = Llama(
                    model_path=MODELS["router"],
                    n_ctx=8192,
                    n_threads=os.cpu_count(),
                    n_gpu_layers=1000
                )
            except Exception as e:
                raise RuntimeError(f"❌ Failed to load router model: {e}")
        return loaded_models["router"]

    # Use cached model if already active
    if name == active_model_name:
        print(f"[Using cached model: {name}]")
        return loaded_models[name]

    # Unload previous model
    if active_model_name and active_model_name in loaded_models:
        unload_model(active_model_name)
        active_model_name = None

    # Load new model safely
    print(f"[Loading model: {name}]")
    try:
        model = Llama(
            model_path=MODELS[name],
            n_ctx=8192,
            n_threads=os.cpu_count(),
            n_gpu_layers=1000
        )
        loaded_models[name] = model
        active_model_name = name
        return model
    except Exception as e:
        raise RuntimeError(f"❌ Failed to load model '{name}': {e}")
