#!/usr/bin/env python3
"""
update_homepage.py — daily.sh 中的一环，重生成 manifest 并保证 latest-*.pdf 指向今天
"""
from __future__ import annotations
import datetime as dt
import pathlib
import shutil
import subprocess

ROOT = pathlib.Path(__file__).resolve().parent.parent
RESUMES = ROOT / "resumes"
HP = ROOT / "homepage" / "resume"
HP.mkdir(parents=True, exist_ok=True)

today = dt.date.today().isoformat()
for kind in ("general", "deepseek", "mindmap"):
    src = RESUMES / f"{today}-{kind}.pdf"
    if src.exists():
        shutil.copy(src, HP / src.name)
        shutil.copy(src, HP / f"latest-{kind}.pdf")

subprocess.run(["python3", str(ROOT / "scripts" / "update_manifest.py")], check=False)
print(f"[update_homepage] {today} synced")
