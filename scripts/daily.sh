#!/bin/bash
# daily.sh — 主 orchestrator，本地 launchd 每天凌晨 3 点跑
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
DATE=$(date +%Y-%m-%d)
LOG="$ROOT/data/$DATE/daily.log"
mkdir -p "$ROOT/data/$DATE"
exec > >(tee -a "$LOG") 2>&1

echo "======== career-log daily $DATE ========"

# 1. Pull lark messages (past 30 days rolling window)
echo "[1/5] collect lark..."
python3 "$ROOT/scripts/collect_lark.py" --since-days 30 --date "$DATE" || echo "lark collect failed (token expired?)"

# 2. Backup memory
echo "[2/5] backup memory..."
bash "$ROOT/scripts/backup_memory.sh"

# 3. Regenerate MR list from local state file (chen updates mrs.json manually or via cronjob)
echo "[3/5] refresh mrs..."
[ -f "$ROOT/data/mrs.json" ] || echo '{"mrs":[]}' > "$ROOT/data/mrs.json"

# 4. Build resume + mindmap PDFs for today
echo "[4/5] build resume..."
python3 "$ROOT/scripts/build_resume.py" --date "$DATE"

# 5. Compile typst → PDF
echo "[5/5] compile typst..."
bash "$ROOT/scripts/compile.sh" "$DATE"

# Refresh latest symlinks
cd "$ROOT/resumes"
ln -sfn "$DATE-general.pdf"  latest-general.pdf 2>/dev/null || true
ln -sfn "$DATE-deepseek.pdf" latest-deepseek.pdf 2>/dev/null || true
ln -sfn "$DATE-mindmap.pdf"  latest-mindmap.pdf 2>/dev/null || true

# Update homepage snapshot list
python3 "$ROOT/scripts/update_homepage.py" || echo "homepage update skipped"

# git commit + push (if changed)
cd "$ROOT"
if [ -n "$(git status --porcelain 2>/dev/null)" ]; then
  git add -A
  git commit -m "snapshot: $DATE" || true
  git push origin main 2>&1 || echo "push failed (no remote yet? offline?)"
fi

echo "======== done $DATE ========"
