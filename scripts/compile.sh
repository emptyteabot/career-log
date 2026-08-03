#!/bin/bash
# compile.sh — typst compile PDFs for a given date
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
DATE="${1:-$(date +%Y-%m-%d)}"
BUILD="$ROOT/templates/build"
OUT="$ROOT/resumes"
mkdir -p "$OUT"

for kind in general deepseek; do
  src="$BUILD/$DATE-$kind.typ"
  [ -f "$src" ] || continue
  typst compile --root "$ROOT" "$src" "$OUT/$DATE-$kind.pdf" 2>&1
done

# Only compile mindmap for today snapshot (it's the same latest one)
if [ -f "$ROOT/templates/mindmap-latest.typ" ]; then
  typst compile --root "$ROOT" "$ROOT/templates/mindmap-latest.typ" "$OUT/$DATE-mindmap.pdf" 2>&1 || true
fi

echo "[compile.sh] $DATE compiled"
ls -la "$OUT" | tail -5
