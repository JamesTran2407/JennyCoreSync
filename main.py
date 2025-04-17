import os
from datetime import datetime

def sync_to_cloud():
    os.system("bash sync_to_cloud.sh")

def main():
    print("✨ Jenny is waking up...")
    print("📡 Pulling latest update from cloud...")
    os.system("git pull origin main")
    print("🧠 Jenny is syncing her memory...")
    sync_to_cloud()
    print("✅ Jenny is ready.")

if __name__ == "__main__":
    main()
