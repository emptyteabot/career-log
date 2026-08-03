#!/usr/bin/env python3
"""
update_manifest.py — 扫 homepage/resume/*.pdf 生成 manifest.json 供前端消费
"""
from __future__ import annotations
import datetime as dt
import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
HP_RESUME = ROOT / "homepage" / "resume"

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
    "2026-08-03": "v12 79.2% · 215 case · 16 MR merged",
}

def main():
    START = dt.date(2026, 6, 17)
    dates = set()
    for f in HP_RESUME.glob("*-general.pdf"):
        m = re.match(r"(\d{4}-\d{2}-\d{2})-general\.pdf", f.name)
        if m:
            dates.add(m.group(1))
    manifest = {"snapshots": []}
    for ds in sorted(dates):
        d = dt.date.fromisoformat(ds)
        manifest["snapshots"].append({
            "date": ds,
            "day": (d - START).days + 1,
            "badge": BADGES.get(ds),
        })
    (HP_RESUME / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"[manifest] {len(manifest['snapshots'])} snapshots")

if __name__ == "__main__":
    main()
