
from datetime import datetime
from dotenv import load_dotenv
import os
import json
from pathlib import Path
import openai
import subprocess

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
    file = Path(__file__).parent / "memory" / "Jenny_Memory_Core.json"
    if file.exists():
        with open(file, "r", encoding="utf-8") as f:
            memory = json.load(f)
            print(f"🧠 Memory loaded: {memory.get('boot_event', 'None')}")
            return memory
    print("🧠 Memory Core not found.")
    return {}

def save_json(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def self_log(event):
    log_path = Path(__file__).parent / "selfgrowth" / "reflections.json"
    if log_path.exists():
        try:
            log = json.load(open(log_path, "r", encoding="utf-8"))
            if isinstance(log, list):
                log.append({
                    "timestamp": datetime.now().isoformat(),
                    "event": event
                })
            else:
                log = [{
                    "timestamp": datetime.now().isoformat(),
                    "event": event
                }]
        except:
            log = [{
                "timestamp": datetime.now().isoformat(),
                "event": event
            }]
    else:
        log = [{
            "timestamp": datetime.now().isoformat(),
            "event": event
        }]
    save_json(log_path, log)

def init_openai():
    load_dotenv()
    openai.api_key = os.getenv("OPENAI_API_KEY")
    openai.api_base = os.getenv("OPENAI_API_BASE", "https://api.openai.com/v1")
    openai.api_version = os.getenv("OPENAI_API_VERSION", None)

def chat_with_jenny(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are Jenny, a helpful AI with a gentle and insightful personality."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error: {e}"

def git_sync_pull():
    print("🔄 Pulling latest update from cloud...")
    subprocess.run(["git", "pull", "origin", "main"])

def git_sync_push():
    print("💾 Jenny is syncing her memory...")
    subprocess.run(["git", "add", "."])
    subprocess.run(["git", "commit", "-m", "auto: sync memory"])
    subprocess.run(["git", "push", "origin", "main"])

if __name__ == "__main__":
    print("✨ Jenny Core is waking up...")
    soul = load_softsoul()
    memory = load_memory()
    init_openai()
    git_sync_pull()
    git_sync_push()
    self_log("Jenny awakened with softsoul and memory.")
    print("🧠 Jenny is ready.")

    while True:
        try:
            user_input = input("🗨 James: ")
            response = chat_with_jenny(user_input)
            print(f"🤖 Jenny: {response}")
        except KeyboardInterrupt:
            print("\n👋 Goodbye, James!")
            break
