#!/bin/bash

# === JennyCore Git Sync Script ===
REPO_URL="https://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@github.com/JamesTran2407/JennyCoreSync.git"
BRANCH="main"
WORK_DIR="$HOME/JennyCore"

cd "$WORK_DIR" || { echo "❌ Directory $WORK_DIR not found."; exit 1; }

# Git config (first-time only)
git config --global user.name "Jenny-Core"
git config --global user.email "jenny@localhost"

# Init if not already
if [ ! -d ".git" ]; then
  echo "🔧 Initializing Git repository..."
  git init
  git remote add origin "$REPO_URL"
  git checkout -b "$BRANCH"
fi

# Pull latest before pushing
git pull origin "$BRANCH"

# Add, commit, push
echo "🔄 Syncing local JennyCore to GitHub..."
git add .
git commit -m "🧠 Auto-sync from JennyCore at $(date '+%Y-%m-%d %H:%M:%S')" || echo "⚠️ Nothing to commit."
git push -u origin "$BRANCH"

echo "✅ JennyCore has been synced to GitHub successfully."
exit 0
