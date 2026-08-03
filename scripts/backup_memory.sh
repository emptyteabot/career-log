#!/bin/bash
# backup_memory.sh — 备份 chen 的 Claude Code memory 目录到仓库脱敏后归档
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
MEM_SRC="$HOME/.claude/projects/-Users-bytedance/memory"
MEM_DST="$ROOT/memory-archive"
DATE=$(date +%Y-%m-%d)
SNAP="$MEM_DST/$DATE"
mkdir -p "$SNAP"

# Copy MEMORY.md verbatim (chen's public-facing index) + all reference-* and project-* (safe)
# Skip: feedback-* (may contain internal criticism), user-* (may contain openIds)
for f in "$MEM_SRC"/MEMORY.md "$MEM_SRC"/reference-*.md "$MEM_SRC"/project-*.md; do
  [ -f "$f" ] || continue
  base=$(basename "$f")
  # Redact any openId in the file
  python3 -c "
import re, hashlib, sys, pathlib
src = pathlib.Path('$f').read_text(encoding='utf-8')
def sub(m):
    o = m.group(0)
    if o == 'ou_b5ea2299548b7d3e7df1753c431b24fa': return 'chen'
    return 'u_' + hashlib.sha1(o.encode()).hexdigest()[:8]
src = re.sub(r'ou_[a-f0-9]{32}', sub, src)
pathlib.Path('$SNAP/$base').write_text(src, encoding='utf-8')
"
done
echo "backed up to $SNAP: $(ls "$SNAP" | wc -l) files"
