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
