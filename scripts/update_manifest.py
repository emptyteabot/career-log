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
    "2026-06-17": "入职第 1 天 · 拉入方舟文档小分队",
    "2026-06-18": "接 Plan 文档监控与验证方案",
    "2026-06-19": "Ark CLI docs 调研 + MVP, 子卿 approval",
    "2026-06-25": "Managed Agents MVP 架构设计稿 + 竞品对标",
    "2026-06-26": "自动化治理系统 V8 结项",
    "2026-06-30": "CMA schema 爬完 50 API · 数据面 10 接口 Review 全套",
    "2026-07-01": "10 接口字段结构 Self Review",
    "2026-07-02": "小白测评研报 V15",
    "2026-07-03": "SendEvent 三篇 API MR 合入 · RD review 拉通",
    "2026-07-07": "拉入 MA 支持 BytePlus 项目组",
    "2026-07-08": "Plan Doc Guardian MVP V6.1 结项",
    "2026-07-10": "Managed Agents API RD Review 发起",
    "2026-07-15": "文档仓 MR!1500 · 30 篇 MA-API sidecar 合入",
    "2026-07-21": "arkcli BP 立项 · MR!8 首交付 12×52 case",
    "2026-07-23": "3 天详细 log + roadmap + tenant e2e evidence",
    "2026-07-25": "BP MCP mvp 联调",
    "2026-07-28": "arkcli-bp 承接 · SSO 5 天 debug 沉淀",
    "2026-07-30": "v2 评测方案对齐 · daily-digest 上线",
    "2026-07-31": "215 case 覆盖 · digital twin runbook",
    "2026-08-01": "第一轮 pass rate 100%",
    "2026-08-02": "第二轮 97.6%",
    "2026-08-03": "第三轮 79.2% · 215 case · 16 MR · career-log 上线",
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
