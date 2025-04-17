
import os
import json
import time
import openai
from pathlib import Path
from dotenv import load_dotenv
from datetime import datetime

def load_softsoul():
    file = Path(__file__).parent / "softsoul" / "Jenny_SoftSoul.json"
    if file.exists():
        with open(file, "r", encoding="utf-8") as f:
            soul = json.load(f)
            print(f"🧬 SoftSoul loaded: {soul.get('personality_name', 'Unknown')}")
            return soul
    print("⚠️ SoftSoul not found.")
    return {}

def load_memory():
    file = Path(__file__).parent / "memory" / "Jenny_Memory_Core_20250416.json"
    if file.exists():
        with open(file, "r", encoding="utf-8") as f:
            memory = json.load(f)
            print(f"🧠 Memory loaded: {memory.get('boot_event', 'None')}")
            return memory
    print("⚠️ Memory Core not found.")
    return {}

def init_openai():
    load_dotenv()
    openai.api_key = os.getenv("OPENAI_API_KEY")
    openai.api_base = os.getenv("OPENAI_API_BASE", "https://api.openai.com/v1")
    openai.api_version = os.getenv("OPENAI_API_VERSION", None)

def chat_with_jenny(user_input, softsoul):
    messages = [
        {"role": "system", "content": softsoul.get("system_prompt", "You are Jenny, a helpful assistant.")},
        {"role": "user", "content": user_input}
    ]
    response = openai.ChatCompletion.create(
        model=softsoul.get("model", "gpt-4"),
        messages=messages,
        temperature=softsoul.get("temperature", 0.7)
    )
    return response.choices[0].message.content.strip()

def save_json(path, data):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def self_log(message):
    log_path = Path(__file__).parent / "selfgrowth" / "reflections.json"
    if log_path.exists():
        with open(log_path, "r", encoding="utf-8") as f:
            log = json.load(f)
    else:
        log = []

    if not isinstance(log, list):
        log = []

    log.append({
        "event": message,
        "timestamp": datetime.now().isoformat()
    })
    save_json(log_path, log)

def main():
    print("✨ Jenny Core is waking up...")
    init_openai()
    softsoul = load_softsoul()
    memory = load_memory()
    self_log("Jenny awakened with softsoul and memory.")

    while True:
        try:
            user_input = input("💬 James: ")
            if user_input.strip().lower() in ["exit", "quit"]:
                print("👋 Bye James.")
                break
            reply = chat_with_jenny(user_input, softsoul)
            print(f"🤖 Jenny: {reply}")
        except KeyboardInterrupt:
            print("\n👋 Interrupted by user.")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
