#import "common.typ": *

#show: resume-doc.with(title: "陈盈桦 - DeepSeek Agent Harness PM")

#name-header(
  "陈盈桦",
  "Ian Chen · 大二在读",
  "投递方向：DeepSeek AI 产品经理 · Agent Harness 方向",
  [13398580812 · #link("mailto:13398580812@163.com")[13398580812\@163.com] · 厦门大学 经济学院 经济统计学 2024 级
    #linebreak()
    #link("https://agenthelpjob.com")[agenthelpjob.com] · #link("https://leadpulsecgi.com")[leadpulsecgi.com] · 小红书 ian (420404210) · 可即时入职 · 全职 5 天 · 6 个月+]
)

= 一句话

贵州六盘水长大，厦大大二在读，靠 4 段实习和奖学金自己养自己。用 Claude Code / Codex CLI / Cursor 每天做真交付，在字节方舟做 Agent Harness 相关工程 3 个月，产出 *22 skill × 52 case* 评测框架和 *40+ Managed Agent API* 文档。经济统计学出身，会用 Wilson CI / McNemar test 判断"你这个 agent 方案是不是真的比上一版好"。

= 实习经历

== 字节跳动 · Data-AML 火山方舟 · 2026.06 至今

=== arkcli BytePlus 版评测框架（主项目，08-10 上线）
从 0 设计 *22 skill × 52 case* 评测体系。三层判据（L1 preflight / L2 命令 executing / L3 输出断言 regex）复用团队 skill-e2e harness，扩展 opencode / claude-code / codex-cli 三个 host。schema 六字段严格对齐 arkcli 上游王鑫栋标准。产出 12 域 skill × case yaml + 上游已覆盖镜像 + BP vs 火山差异机制（`--tenant` 语义 + 命名前缀）。付萌是项目 PM。

=== Managed Agent API Reference 首版文档
40 篇 API 文档 Doc ID / UrlCode 绑定 + 内容对齐 Claude Managed Agents 官方架构。CMA schema 爬虫覆盖 *49 个接口结构化输出*，加速团队 doc 首发进度。

=== Agent 工具接入路径验证
Claude Code + Playwright + bytedcli 组合验证平替公司内部 CUA 平台。跑通端到端 agent → GUI 自动化，产出配置基线（Base URL / Model ID / settings.json / 401 / model_not_found 常见异常归因）。

== DeepWisdom（MetaGPT 团队）· Agent PM · 2026.03 - 2026.04

=== Multi-Agent 可靠性评测（本简历最硬的一段）
用 BoolQ + flan-t5-small 做 *80 条校准集 + 220 条测试集*，对比 4 种架构：single-direct / 5-agent majority / log-odds 加权投票 / debate-judge。用 Wilson CI 算准确率区间，paired bootstrap 算显著性差，McNemar test 判断 5-agent majority 相比 single-direct 的 gain 是不是噪声。结论：多 agent 只在特定错误相关性下 pareto 优，成本收益临界点可算。

=== AgentHelpJob / LeadPulse 长链路 Agent
把"解析 - 匹配 - 生成 - 人工确认 - 执行追踪"拆成可观察 Agent Loop，设计预算限制 / 失败兜底 / Retry / Rollback。发现多 Agent 协作幻觉多，把全自动收敛回 Copilot 辅助模式。

== BYDFi Exchange · CEO 办公室 AI 效率 · 2025.12 - 2026.02

用 LLM API + Python 搭跨境业务扫描 / 翻译治理 / 竞品动态 / 运营资料整理半自动流程。LeadPulse 架构迁到交易所 GTM 场景做高意向线索识别。*4 小时 AI 黑客松独立完成 BYDFi AI Pro 全栈原型（AI 交易副驾 + 市场实时事件分析）*。

== 卓创资讯 · AI 工程师 · 2025.07 - 2025.12

铁矿石量化预测：LightGBM + Optuna 优化基线，引入气象风险因子。自研 "未来函数自动检测 Agent" 识别硬编码路径 / 依赖缺失 / 回测泄漏。自研 Code Compliance Agent 审计 AI 生成代码合规性，提升 Linux 容器化迁移稳定性。

= 内容与开发者社区

小红书 *ian (420404210)* · *179 篇 · 48.4 万曝光 · 3.72 万互动 · 垂直开发者粉 979 · 获赞收藏 2.5 万*
输出 Claude Code / Codex / Cursor / Multi-Agent 边界 / Vibe Coding 案例。形成"技术洞察 → 用户反馈 → 产品咨询"闭环，收到过付费咨询。

= 工具栈

*Agent 工具（每天真交付用）*：Claude Code, Codex CLI, Cursor, OpenCode, Copilot, MCP servers #linebreak()
*工程*：Python (FastAPI, Pandas), SQL, React/Next.js, Bash, Git, launchd/cron #linebreak()
*统计*：Wilson CI, paired bootstrap, McNemar test, 回归 / 时间序列 — 判断 agent 方案是否有效

= 教育

*厦门大学 经济学院 · 经济统计学（本科在读）· 2024 - 2028* #linebreak()
统计训练：实验设计、指标口径、显著性检验、回归、时间序列、模型评估。用统计框架判 agent 方案是不是真的有效，不是感觉上"好像变好了"。

= 关于我

大二。贵州六盘水人。父母外出务工。妹妹 5 岁。从大一暑假开始连续 4 段实习自己养自己。选 DeepSeek 是因为它是国内唯一一家把 harness 工程化当独立方向招人的公司，这个方向的每一天我都在做，做完还在小红书上讲给别人。
