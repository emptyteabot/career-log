#import "common.typ": *

#show: resume-doc.with(title: "陈盈桦 · 通用简历")

#name-header(
  "陈盈桦",
  "Ian Chen · 大二在读",
  "AI 工程与 Agent 产品方向 · 大二在读实习中",
  [13398580812 · #link("mailto:13398580812@163.com")[13398580812\@163.com] · 厦门大学 经济学院 经济统计学 2024 级
    #linebreak()
    #link("https://agenthelpjob.com")[agenthelpjob.com] · #link("https://leadpulsecgi.com")[leadpulsecgi.com] · 小红书 ian (420404210) · 可即时入职]
)

= 一句话

贵州六盘水长大，厦大大二在读，靠 4 段实习和奖学金自己养自己。会写 Python / Go / TypeScript 全栈交付，每天用 Claude Code / Codex CLI 做真项目。字节实习期产出 22 skill × 52 case Agent 评测框架 + 40 篇 Managed Agent API 文档。经济统计学出身，习惯用 Wilson CI / McNemar test 判方案有没有真的变好。

= 实习经历

== 字节跳动 · Data-AML 火山方舟 · 2026.06 至今 · 技术文档 / Agent 工程

- *arkcli BytePlus 版评测框架（08-10 上线）*：22 skill × 52 case × 3 层判据（L1 preflight / L2 executing / L3 输出断言）。扩展 opencode / claude-code / codex-cli 三个 agent host。schema 对齐上游标准，产出 12 域 skill yaml + 差异机制。
- *Managed Agent API Reference 首版文档*：40 篇 API 文档 Doc ID / UrlCode 绑定 + CMA schema 爬 49 接口结构化输出。
- *Agent 工具接入验证*：Claude Code + Playwright + bytedcli 组合平替公司内部 CUA 平台，跑通端到端 GUI 自动化。

== DeepWisdom（MetaGPT 团队）· Agent PM · 2026.03 - 2026.04

- *Multi-Agent 可靠性评测*：BoolQ + flan-t5-small · 80 校准集 + 220 测试集 · 对比 single-direct / 5-agent majority / log-odds / debate-judge 四种架构 · Wilson CI + paired bootstrap + McNemar test 显著性判断。
- *AgentHelpJob & LeadPulse*：长链路 Agent Loop 设计（解析 / 匹配 / 生成 / 人工确认 / 执行追踪）+ 预算限制 + 失败兜底 + Retry / Rollback。

== BYDFi Exchange · CEO 办公室 AI 效率 · 2025.12 - 2026.02

- LLM API + Python 搭跨境业务扫描 / 翻译治理 / 竞品动态 / 运营资料半自动流程。
- LeadPulse 架构迁到交易所 GTM 场景做高意向线索识别。
- *4 小时 AI 黑客松独立完成 BYDFi AI Pro 全栈原型*（AI 交易副驾 + 市场实时事件分析）。

== 卓创资讯 · AI 工程师 / 算法实习生 · 2025.07 - 2025.12

- 铁矿石量化预测：LightGBM + Optuna 优化基线，引入气象风险因子。
- 自研 "未来函数自动检测 Agent"：识别硬编码路径 / 依赖缺失 / 回测泄漏。
- 自研 Code Compliance Agent：审计 AI 生成代码合规性，提升 Linux 容器化迁移稳定性。

= 精选项目

#grid(
  columns: (1fr, 1fr),
  gutter: 10pt,
  [
    *LeadPulse · 线索提取 Agent* #linebreak()
    FastAPI + React/Next.js + LLM API 交付 MVP；Prompt 路由 + 规则标签 + 人工确认，把复杂搜索转成可控 Copilot 工作流。
  ],
  [
    *AgentHelpJob · 求职辅助 Agent* #linebreak()
    JD 解析 + 简历匹配 + 材料生成 + 人工确认 + 投递追踪。低信任 / 高决策成本场景的可控性设计。
  ],
  [
    *Multi-Agent 可靠性评测* #linebreak()
    80 校准 + 220 测试 · 4 架构对照 · 从准确率、显著性、错误相关性、成本收益四维验证多 Agent 边界。
  ],
  [
    *yinghua-cortex 签名 Agent* #linebreak()
    飞书 app · Mac launchd 15min tick · 自动扫消息 + 摘要 + 决策提示；离线部署。
  ],
)

= 内容与开发者社区

小红书 *ian (420404210)* · *179 篇 · 48.4 万曝光 · 3.72 万互动 · 垂直开发者粉 979 · 获赞收藏 2.5 万* #linebreak()
输出 Claude Code / Codex / Cursor / Multi-Agent 边界 / Vibe Coding 案例，形成"技术洞察 → 用户反馈 → 产品咨询"闭环。

= 工具栈

*语言*：Python (FastAPI, Pandas), TypeScript / JavaScript (React, Next.js), Go, SQL, Bash #linebreak()
*Agent / AI*：Claude Code, Codex CLI, Cursor, OpenCode, MCP servers, LLM API, Prompt Engineering, Tool Calling #linebreak()
*工程*：Git, Docker, launchd / cron, Playwright, 自动化脚本, API 调试, 状态追踪, 可复现实验 #linebreak()
*统计与评估*：Wilson CI, paired bootstrap, McNemar test, LightGBM, Optuna, 回归 / 时间序列 / 显著性检验

= 教育

*厦门大学 经济学院 · 经济统计学（本科在读）· 2024 - 2028* #linebreak()
统计训练覆盖实验设计、指标口径、显著性检验、回归分析、时间序列与模型评估。

= 关于我

贵州六盘水人。父母外出务工，妹妹 5 岁。从大一暑假开始连续 4 段实习自己养自己。写代码的同时在小红书持续输出，把踩过的 agent 坑讲给别人听。相信"能跑起来 + 数据说话 + 讲清楚"三件事。
