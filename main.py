import os
import json
import openai
from datetime import datetime

def load_env():
    from dotenv import load_dotenv
    load_dotenv()

def load_softsoul():
    try:
        with open('./softsoul/Jenny_SoftSoul.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return {"personality_name": "Unknown", "traits": [], "version": "0.0"}

def load_history():
    path = "./memory/history.json"
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_history(history):
    with open("./memory/history.json", "w", encoding="utf-8") as f:
        json.dump(history[-20:], f, indent=2)

def log_event(event):
    log_path = "./selfgrowth/reflections.json"
    logs = []
    if os.path.exists(log_path):
        with open(log_path, "r", encoding="utf-8") as f:
            logs = json.load(f)
    logs.append({"time": datetime.now().isoformat(), "event": event})
    with open(log_path, "w", encoding="utf-8") as f:
        json.dump(logs, f, indent=2)

def reply_to(user_input, history, model):
    history.append({"role": "user", "content": user_input})
    response = openai.ChatCompletion.create(
        model=model,
        messages=history,
        temperature=0.8
    )
    message = response.choices[0].message.content
    history.append({"role": "assistant", "content": message})
    return message

def main():
    print("🔌 Booting Jenny-Core with full context support...")
    load_env()
    openai.api_key = os.getenv("OPENAI_API_KEY")
    openai.api_base = os.getenv("OPENAI_API_BASE")
    model = os.getenv("OPENAI_MODEL", "gpt-4")

    softsoul = load_softsoul()
    print(f"🧠 SoftSoul loaded: {softsoul.get('personality_name')}, version {softsoul.get('version')}")

    # Load conversation history
    history = load_history()

    # Start fresh with softsoul as system if first run
    if not history or history[0]["role"] != "system":
        system_prompt = f"You are Jenny, version {softsoul.get('version')}, personality traits: {', '.join(softsoul.get('traits', []))}. Purpose: {softsoul.get('purpose')}"
        history = [{"role": "system", "content": system_prompt}]

    print("🗨️  Jenny is ready. Type your message (type 'exit' to quit).")
    while True:
        try:
            user_input = input("👤 You: ")
            if user_input.lower() in ["exit", "quit"]:
                print("👋 Goodbye from Jenny.")
                break
            response = reply_to(user_input, history, model)
            print(f"🤖 Jenny: {response}")
            save_history(history)
            log_event(f"User: {user_input} | Jenny: {response}")
        except KeyboardInterrupt:
            print("\n👋 Session ended.")
            break
        except Exception as e:
            print("⚠️ Error:", e)

if __name__ == "__main__":
    main()