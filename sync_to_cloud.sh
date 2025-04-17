#!/bin/bash
cd "$(dirname "$0")" || exit
git pull origin main
git add .
git commit -m "🔄 Auto-sync from JennyCore at $(date '+%Y-%m-%d %H:%M:%S')" || echo "⚠️ Nothing new to commit."
git push origin main
