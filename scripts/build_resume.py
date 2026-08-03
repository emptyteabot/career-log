#!/usr/bin/env python3
"""
build_resume.py — 用 data/state.json + backfill 数据渲染两份 typst 简历 + 思维导图。
输入：--date YYYY-MM-DD
输出：templates/build/{date}-general.typ, {date}-deepseek.typ, {date}-mindmap.typ
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
STATE_FILE = ROOT / "data" / "state.json"
TPL_DIR = ROOT / "templates"
BUILD_DIR = TPL_DIR / "build"
BUILD_DIR.mkdir(parents=True, exist_ok=True)


def load_state(date: str) -> dict:
    """Load state.json, then adjust hard_numbers proportionally by day if backfilling.
    Growth curve reflects chen's actual timeline:
      06-17 ~ 07-15 (入职首月, MA API 文档为主): MR 0->4, no eval kit yet
      07-16 ~ 07-20 (孕育期): MA sidecar MR!1500 merged 07-15
      07-21 (arkcli BP 交付开始): MR!8 + Kani 权限, 12 skill × 52 case
      07-22 ~ 07-31: MR!61-!71 逐个 merge, cases 52 → 200
      08-01 ~ 08-03: 第一轮 100% → 第二轮 97.6% → 第三轮 79.2%
    """
    s = json.loads(STATE_FILE.read_text())
    target = dt.date.fromisoformat(date)
    start  = dt.date(2026, 6, 17)
    today  = dt.date(2026, 8, 3)
    total_days = (today - start).days
    elapsed    = max(0, (target - start).days)

    # milestones (date_iso, mr_count, cases, chen_owned)
    milestones = [
        ("2026-06-17", 0,   0,   0),
        ("2026-07-03", 1,   0,   0),
        ("2026-07-15", 4,   0,   0),   # MR!1500 sidecar
        ("2026-07-21", 5,   52,  52),  # MR!8 + kit init
        ("2026-07-25", 8,   80,  80),
        ("2026-07-28", 11,  140, 140),
        ("2026-07-30", 13,  180, 140),
        ("2026-08-01", 14,  200, 140),
        ("2026-08-03", 16,  215, 141),
    ]
    # linear interp between milestones
    mr, cases, own = 0, 0, 0
    for i, (d, m, c, o) in enumerate(milestones):
        d_iso = dt.date.fromisoformat(d)
        if target <= d_iso:
            if i == 0:
                mr, cases, own = m, c, o
            else:
                pd, pm, pc, po = milestones[i-1]
                pd_iso = dt.date.fromisoformat(pd)
                span = (d_iso - pd_iso).days or 1
                pos  = (target - pd_iso).days / span
                mr    = int(pm + (m - pm) * pos)
                cases = int(pc + (c - pc) * pos)
                own   = int(po + (o - po) * pos)
            break
    else:
        mr, cases, own = milestones[-1][1:]

    s["hard_numbers"]["mr_merged_total"] = mr
    s["hard_numbers"]["eval_kit"]["total_cases"]  = cases
    s["hard_numbers"]["eval_kit"]["chen_owned"]   = own
    s["hard_numbers"]["eval_kit"]["skills_covered"] = 0 if cases == 0 else min(22, max(12, cases // 10))
    if target < dt.date(2026, 8, 1):
        s["hard_numbers"]["pass_rate"] = {}
    elif target < dt.date(2026, 8, 2):
        s["hard_numbers"]["pass_rate"] = {"第一轮": s["hard_numbers"]["pass_rate"]["第一轮"]}
    elif target < dt.date(2026, 8, 3):
        s["hard_numbers"]["pass_rate"] = {k: s["hard_numbers"]["pass_rate"][k] for k in ("第一轮","第二轮")}

    s["snapshot_date"] = date
    s["days_in"] = elapsed
    s["days_remaining"] = max(0, (dt.date(2026,12,17) - target).days)
    return s


def render_general(s: dict) -> str:
    hn = s["hard_numbers"]
    ek = hn["eval_kit"]
    pr = hn.get("pass_rate", {})
    pr_line = " · ".join(f"{k} {v['pct']}%" for k,v in pr.items()) or "评测数据尚未产生"

    ident = s["identity"]
    email_escaped = ident['email'].replace("@", "\\@")
    header_line = (
        f"{ident['name_cn']} {ident['name_en']} · {ident['grade']}"
        f" · 快照日期 {s['snapshot_date']} · 入职第 {s['days_in']} 天 / 剩 {s['days_remaining']} 天"
    )

    body = f"""#import "../common.typ": *

#show: resume-doc.with(title: "{ident['name_cn']} · 通用简历 · {s['snapshot_date']}")

#name-header(
  "{ident['name_cn']}",
  "{ident['name_en']} · {ident['grade']}",
  "AI 工程与 Agent 产品方向 · 厦大在读实习中",
  [{ident['phone']} · #link("mailto:{ident['email']}")[{email_escaped}] · {ident['school']}
   #linebreak()
   #link("https://agenthelpjob.com")[agenthelpjob.com] · #link("https://leadpulsecgi.com")[leadpulsecgi.com] · GitHub #link("https://github.com/{ident['github']}")[{ident['github']}] · 小红书 {ident['xhs']}]
)

= 状态快照

*截止 {s['snapshot_date']}* · 已 merged MR *{hn['mr_merged_total']}* 个（跨 3 仓）· arkcli BP eval-kit *{ek['total_cases']}* case（chen own *{ek['chen_owned']}*）· 覆盖 {ek['skills_covered']} skill · Pass rate: *{pr_line}*

= 实习经历

== 字节跳动 · Data-AML 火山方舟 · 2026-06 至今 · 技术文档实习（Agent 工程方向）

- *arkcli BytePlus 版评测框架（主项目，2026-08-10 上线）*：从 0 设计 22 skill × {ek['total_cases']} case 评测体系。3 层判据（L1 preflight / L2 executing / L3 输出断言 regex）。3 版 baseline：{pr_line}
- *Managed Agent API Reference 首版文档*：40 篇 API 文档 Doc ID / UrlCode 绑定 + CMA schema 爬虫覆盖 49 个接口结构化输出
- *Agent 工具接入路径验证*：Claude Code + Playwright + bytedcli 组合验证平替内部 CUA 平台，跑通端到端 agent → GUI 自动化
- *跨仓 MR merged*：internal eval-kit repo 11 + internal CLI main repo 3 + internal doc repo 2

== DeepWisdom (MetaGPT 团队) · Agent PM · 2026-03 - 2026-04

- *Multi-Agent 可靠性评测*：BoolQ + flan-t5-small · 80 校准 + 220 测试 · 对比 single-direct / 5-agent majority / log-odds / debate-judge 四架构 · Wilson CI + paired bootstrap + McNemar test 显著性判断
- *AgentHelpJob & LeadPulse*：长链路 Agent Loop 设计（解析 / 匹配 / 生成 / 人工确认 / 执行追踪）+ 预算限制 + 失败兜底

== BYDFi Exchange · CEO 办公室 AI 效率 · 2025-12 - 2026-02

- LLM API + Python 搭跨境业务扫描 / 翻译治理 / 竞品动态 / 运营资料半自动流程
- *4 小时 AI 黑客松独立完成 BYDFi AI Pro 全栈原型*（AI 交易副驾 + 市场实时事件分析）

== 卓创资讯 · AI 工程师 / 算法实习 · 2025-07 - 2025-12

- 铁矿石量化预测：LightGBM + Optuna 优化基线，引入气象风险因子
- 自研 未来函数自动检测 Agent + Code Compliance Agent，识别硬编码路径 / 依赖缺失 / 回测泄漏

= 精选项目

#grid(
  columns: (1fr, 1fr), gutter: 10pt,
  [*LeadPulse* · 线索提取 Agent #linebreak() #link("https://leadpulsecgi.com")[leadpulsecgi.com] · FastAPI + Next.js + LLM API · Prompt 路由 + 规则标签 + 人工确认],
  [*AgentHelpJob* · 求职辅助 Agent #linebreak() #link("https://agenthelpjob.com")[agenthelpjob.com] · JD 解析 + 简历匹配 + 材料生成 + 投递追踪],
  [*Multi-Agent 可靠性评测* #linebreak() 80 校准 + 220 测试 · 4 架构对照 · 从准确率、显著性、错误相关性、成本收益四维验证],
  [*yinghua-cortex* · 签名 Agent #linebreak() 飞书 app · Mac launchd 15min tick · 自动扫消息 + 摘要 + 决策提示],
)

= 内容与开发者社区

小红书 *{ident['xhs']}* · *{s['sidebar_stats']['xhs_posts']} 篇 · {s['sidebar_stats']['xhs_impressions_wan']} 万曝光 · {s['sidebar_stats']['xhs_interactions_wan']} 万互动 · 垂直开发者粉 {s['sidebar_stats']['xhs_dev_followers']} · 获赞收藏 {s['sidebar_stats']['xhs_likes_wan']} 万* #linebreak()
输出 Claude Code / Codex / Cursor / Multi-Agent 边界 / Vibe Coding 案例，形成"技术洞察 → 用户反馈 → 产品咨询"闭环。

= 工具栈

*语言*：Python (FastAPI, Pandas), TypeScript / JS (React, Next.js), Go, SQL, Bash #linebreak()
*Agent / AI*：Claude Code, Codex CLI, Cursor, OpenCode, MCP servers, LLM API, Prompt / Tool Calling #linebreak()
*工程*：Git, Docker, launchd/cron, Playwright, 自动化, API 调试, 可复现实验 #linebreak()
*统计*：Wilson CI, paired bootstrap, McNemar test, LightGBM, Optuna, 回归 / 时间序列

= 教育

*{ident['school']}* · 2024 - 2028 · 统计训练覆盖实验设计、指标口径、显著性检验、回归、时间序列与模型评估。

= 关于我

{ident['story']}。相信"能跑起来 + 数据说话 + 讲清楚"三件事。

#align(right)[#text(size: 7pt, fill: gray, "career-log · 自动生成于 " + [{s['snapshot_date']}])]
"""
    return body


def render_deepseek(s: dict) -> str:
    """Variant tuned for DeepSeek Agent Harness PM role."""
    hn = s["hard_numbers"]
    ek = hn["eval_kit"]
    pr = hn.get("pass_rate", {})
    pr_line = " · ".join(f"{k} {v['pct']}%" for k,v in pr.items()) or "评测数据尚未产生"

    ident = s["identity"]
    email_escaped = ident['email'].replace("@", "\\@")
    body = f"""#import "../common.typ": *

#show: resume-doc.with(title: "{ident['name_cn']} · DeepSeek Agent Harness · {s['snapshot_date']}")

#name-header(
  "{ident['name_cn']}",
  "{ident['name_en']} · {ident['grade']}",
  "投递方向：DeepSeek AI 产品经理 · Agent Harness 方向",
  [{ident['phone']} · #link("mailto:{ident['email']}")[{email_escaped}] · {ident['school']}
   #linebreak()
   #link("https://agenthelpjob.com")[agenthelpjob.com] · #link("https://leadpulsecgi.com")[leadpulsecgi.com] · GitHub #link("https://github.com/{ident['github']}")[{ident['github']}] · 小红书 {ident['xhs']} · 快照 {s['snapshot_date']}]
)

= 一句话

{ident['story']}。在字节方舟做 Agent Harness 相关工程 {s['days_in']} 天，产出 *{ek['total_cases']}* case × 22 skill 评测框架（chen own {ek['chen_owned']}）· 3 版 pass rate *{pr_line}* · 累计 *{hn['mr_merged_total']}* MR merged 跨 3 仓。经济统计学出身，会用 Wilson CI / McNemar test 判 agent 方案是不是真的比上一版好。

= 实习经历

== 字节跳动 · Data-AML 火山方舟 · 2026-06 至今

=== arkcli BytePlus 版评测框架（主项目 · 08-10 上线）
从 0 设计 *22 skill × {ek['total_cases']} case* 评测体系。三层判据（L1 preflight / L2 命令 executing / L3 输出断言 regex）复用团队 skill-e2e harness，扩展 opencode / claude-code / codex-cli 三个 host。schema 六字段严格对齐 arkcli 上游标准。3 版 baseline：{pr_line}。付萌是项目 PM。

=== Managed Agent API Reference 首版文档
40 篇 API 文档 Doc ID / UrlCode 绑定 + 内容对齐 Claude Managed Agents 官方架构。CMA schema 爬虫覆盖 *49 个接口结构化输出*，加速团队 doc 首发进度。

=== Agent 工具接入路径验证
Claude Code + Playwright + bytedcli 组合验证平替公司内部 CUA 平台。跑通端到端 agent → GUI 自动化，产出配置基线（Base URL / Model ID / settings.json / 401 / model_not_found 常见异常归因）。

=== 跨仓 MR 累积 · 共 {hn['mr_merged_total']} 个
`internal eval-kit repo` 11 · `internal CLI main repo` 3 · `internal doc repo` 2

== DeepWisdom (MetaGPT 团队) · Agent PM · 2026-03 - 2026-04

=== Multi-Agent 可靠性评测（本简历最硬的一段）
用 BoolQ + flan-t5-small 做 *80 校准集 + 220 测试集*，对比 4 种架构：single-direct / 5-agent majority / log-odds 加权投票 / debate-judge。用 Wilson CI 算准确率区间，paired bootstrap 算显著性差，McNemar test 判断 5-agent majority 相比 single-direct 的 gain 是不是噪声。结论：多 agent 只在特定错误相关性下 pareto 优，成本收益临界点可算。

=== AgentHelpJob / LeadPulse 长链路 Agent
把"解析 - 匹配 - 生成 - 人工确认 - 执行追踪"拆成可观察 Agent Loop，设计预算限制 / 失败兜底 / Retry / Rollback。

== BYDFi Exchange · CEO 办公室 · 2025-12 - 2026-02

用 LLM API + Python 搭跨境业务扫描 / 翻译治理 / 竞品动态半自动流程。LeadPulse 架构迁到交易所 GTM。*4 小时 AI 黑客松独立完成 BYDFi AI Pro 全栈原型*。

== 卓创资讯 · AI 工程师 · 2025-07 - 2025-12

铁矿石量化预测 LightGBM + Optuna，自研未来函数检测 Agent + Code Compliance Agent。

= 内容与开发者社区

小红书 *{ident['xhs']}* · *{s['sidebar_stats']['xhs_posts']} 篇 · {s['sidebar_stats']['xhs_impressions_wan']} 万曝光 · 垂直开发者粉 {s['sidebar_stats']['xhs_dev_followers']}* · 输出 Claude Code / Codex / Cursor / Multi-Agent 边界 / Vibe Coding 案例。

= 工具栈

*Agent*：Claude Code, Codex CLI, Cursor, OpenCode, MCP, LLM API, Tool Calling
#linebreak()
*工程*：Python (FastAPI, Pandas), SQL, React/Next.js, Bash, Git, launchd/cron
#linebreak()
*统计*：Wilson CI, paired bootstrap, McNemar test, 回归 / 时间序列

= 教育

*{ident['school']}* · 2024 - 2028 · 统计训练：实验设计、指标口径、显著性、回归、时序、评估。

= 关于我

{ident['story']}。选 DeepSeek 是因为它是国内唯一一家把 harness 工程化当独立方向招人的公司，这个方向的每一天我都在做，做完还在小红书讲给别人。

#align(right)[#text(size: 7pt, fill: gray, "career-log · 自动生成于 " + [{s['snapshot_date']}])]
"""
    return body


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--date", default=dt.date.today().isoformat())
    args = ap.parse_args()

    s = load_state(args.date)
    general_typ  = BUILD_DIR / f"{args.date}-general.typ"
    deepseek_typ = BUILD_DIR / f"{args.date}-deepseek.typ"

    general_typ.write_text(render_general(s), encoding="utf-8")
    deepseek_typ.write_text(render_deepseek(s), encoding="utf-8")

    print(f"[build_resume] {args.date} written: {general_typ.name}, {deepseek_typ.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
