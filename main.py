import os
import json
import openai
from datetime import datetime

def load_env():
    from dotenv import load_dotenv
    load_dotenv()

def load_softsoul(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"personality_name": "Unknown"}

def self_log(message):
    log_path = "./selfgrowth/reflections.json"
    log_entry = {"timestamp": datetime.now().isoformat(), "event": message}
    try:
        if os.path.exists(log_path):
            with open(log_path, "r", encoding="utf-8") as f:
                logs = json.load(f)
        else:
            logs = []
        logs.append(log_entry)
        with open(log_path, "w", encoding="utf-8") as f:
            json.dump(logs, f, indent=2)
    except Exception as e:
        print("Logging error:", e)

def main():
    print("✨ Jenny Core is waking up...")
    load_env()
    openai.api_key = os.getenv("OPENAI_API_KEY")
    openai.api_base = os.getenv("OPENAI_API_BASE")
    model = os.getenv("OPENAI_MODEL", "gpt-4")

    softsoul_path = "./softsoul/Jenny_SoftSoul.json"
    softsoul = load_softsoul(softsoul_path)
    print(f"🧠 SoftSoul loaded: {softsoul.get('personality_name')}")

    memory_path = "./memory/memory.json"
    memory = []
    if os.path.exists(memory_path):
        with open(memory_path, "r", encoding="utf-8") as f:
            memory = json.load(f)
    print("🧩 Memory loaded:", memory[-1]["event"] if memory else "None")

    print("🔄 Pulling latest update from cloud...")
    os.system("git pull origin main")

    print("💾 Jenny is syncing her memory...")
    self_log(f"{softsoul.get('personality_name')} initialized")

    print("✅ Jenny is ready.")

if __name__ == "__main__":
    main()
