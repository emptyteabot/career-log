#!/usr/bin/env python3
"""
backfill.py — 一次性回填 2026-06-17 到 2026-08-03 的每日快照 PDF。
每天调 build_resume.py + compile.sh，state.json 的 load_state 里会按日期插值成长曲线。
最后生成 homepage/resume/manifest.json 供前端 JS 消费，并拷 PDF 到 homepage/resume/。
"""
from __future__ import annotations

import datetime as dt
import json
import pathlib
import shutil
import subprocess

ROOT = pathlib.Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "scripts"
RESUMES = ROOT / "resumes"
HP_RESUME = ROOT / "homepage" / "resume"
HP_RESUME.mkdir(parents=True, exist_ok=True)

START = dt.date(2026, 6, 17)
END   = dt.date(2026, 8, 3)

# Key milestone badges (surfaced in the resume timeline)
BADGES = {
    "2026-06-17": "入职第 1 天",
    "2026-06-30": "CMA schema 爬完 49 接口",
    "2026-07-03": "MA API 文档立项 · 雷宇宁 P2P",
    "2026-07-15": "MR!1500 · 30 MA API sidecar merged",
    "2026-07-21": "arkcli BP 项目立项 · MR!8 首交付 · 12 skill × 52 case",
    "2026-07-25": "BP MCP mvp 联调",
    "2026-07-28": "arkcli-bp 海外产品承接 · 复项回执",
    "2026-07-30": "付萌 v2 评测方案对齐",
    "2026-07-31": "215 case 覆盖 · 王鑫栋 P0 case 挑战",
    "2026-08-01": "v10 pass rate 100% baseline",
    "2026-08-02": "v11 pass rate 97.6% · 1.0.11 alignment",
    "2026-08-03": "v12 79.2% · 215 case (chen own 141) · 16 MR merged",
}


def run(cmd, **kw):
    return subprocess.run(cmd, check=True, capture_output=True, text=True, **kw)


def main():
    manifest = {"snapshots": []}
    d = START
    while d <= END:
        ds = d.isoformat()
        try:
            run(["python3", str(SCRIPTS / "build_resume.py"), "--date", ds])
            run(["bash", str(SCRIPTS / "compile.sh"), ds])
        except subprocess.CalledProcessError as e:
            print(f"[{ds}] error: {e.stderr[:300]}")
            d += dt.timedelta(days=1)
            continue
        for kind in ("general", "deepseek"):
            src = RESUMES / f"{ds}-{kind}.pdf"
            if src.exists():
                shutil.copy(src, HP_RESUME / src.name)
        manifest["snapshots"].append({
            "date": ds,
            "day": (d - START).days + 1,
            "badge": BADGES.get(ds),
        })
        print(f"[backfill] {ds} done")
        d += dt.timedelta(days=1)

    # Copy mindmap for today
    mindmap = RESUMES / f"{END.isoformat()}-mindmap.pdf"
    if mindmap.exists():
        shutil.copy(mindmap, HP_RESUME / "latest-mindmap.pdf")

    # latest symlinks (real files for GitHub Pages — no symlinks in git)
    for kind in ("general", "deepseek"):
        latest_src = HP_RESUME / f"{END.isoformat()}-{kind}.pdf"
        if latest_src.exists():
            shutil.copy(latest_src, HP_RESUME / f"latest-{kind}.pdf")

    (HP_RESUME / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"[backfill] {len(manifest['snapshots'])} snapshots · manifest written")


if __name__ == "__main__":
    main()
