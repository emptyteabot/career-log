#set document(title: "陈盈桦 · BP skill 线 · 近一个月产出思维导图 v2 · 2026-08-03")
#set page(paper: "a3", flipped: true, margin: 1.0cm)
#set text(font: ("Noto Sans CJK SC", "Helvetica Neue"), size: 8.5pt, lang: "zh")

#let node(title, body, fill: rgb("#eef2f7"), stroke-color: rgb("#1f3a5f"), width: auto, txt: none) = {
  let title-fill = if txt == white { white } else { stroke-color }
  box(
    fill: fill,
    stroke: 1pt + stroke-color,
    inset: 6pt,
    radius: 4pt,
    width: width,
    [
      #text(weight: "bold", fill: title-fill, size: 9.5pt, title)
      #v(-0.2em)
      #block(width: 100%, if txt == white { text(fill: white, body) } else { body })
    ]
  )
}
#let ev(t) = text(size: 7pt, fill: rgb("#666"), style: "italic", "▸ " + t)

#align(center)[
  #text(size: 15pt, weight: "bold", fill: rgb("#1f3a5f"))[陈盈桦 · BP skill 线 · 近一月产出思维导图 v2]
  #v(-0.4em)
  #text(size: 8pt, fill: gray)[快照日期 2026-08-03 · 数据源：飞书 lark-cli + code.byted.org MR 列表 + chen 亲述 · v1 已过时约 10 天全量重写]
]

#v(0.3em)

#align(center)[
  #node(
    "arkcli BP skill 主线",
    [
      #text(size: 8pt)[*Owner*: 付萌（PM）· *MT*: 雷宇宁 · *硬 DL*: 2026-08-10 上线]
      #linebreak()
      #text(size: 7.8pt)[*Chen 角色*: 跨域 meta-work（评测框架 + skill 修复 + 文档补齐），非某 skill 的 audit owner]
    ],
    fill: rgb("#1f3a5f"), stroke-color: rgb("#0d1b2a"), width: 62%, txt: white,
  )
]

#v(0.4em)

// 5 分支：接活 · 首交付 · MR 累积 · 3 版 pass rate · MA/其他仓联动
#grid(
  columns: (1fr, 1fr, 1fr, 1fr, 1fr),
  gutter: 5pt,

  // 分支 1
  node(
    "① 07-21 接活 & 权限",
    [
      #set text(size: 7.8pt)
      #text(size: 7.5pt)[
      · 07-21 10:53 付萌拉入 `arkcli 支持 byteplus`\
      · 07-21 14:33 建 `arkcli 评测开发` 群（付萌 + 范子卿 + 王鑫栋 + chen）\
      · 07-21 15:11 Kani 权限申请 `aml-qa/arkcli-eval-kit`\
      · 07-21 16:59 权限批准 master
      ]
      #v(0.2em)
      #ev("同日拿到仓库 master，当天开工")
    ],
    fill: rgb("#fef3e7"), stroke-color: rgb("#c96f1c"),
  ),

  // 分支 2 · 首交付 + 二次 review
  node(
    "② 07-21 首发交付",
    [
      #set text(size: 7.5pt)
      *MR!8*（07-21 · 已 merged）\
      → `cases(bp): add 12-skill 52-case eval set`\
      → README §零→§八 · 321 行\
      → schema 六字段对齐王鑫栋\
      → upstream 12 skill / 136 case 镜像\
      → 3 家大厂 eval 归纳（Anthropic / OpenAI / LangSmith）\
      · 07-21 17:43 范子卿抛：文档 API 接进来后怎么用\
      · 07-21 22:39 付萌约 07-22 case 有效性 review
      #v(0.2em)
      #ev("首交付当天合入，二次 review 07-22 完成")
    ],
    fill: rgb("#e7f4ea"), stroke-color: rgb("#2a7a3a"),
  ),

  // 分支 3 · 后续 11 MR 累积
  node(
    "③ eval-kit 后续 11 MR",
    [
      #set text(size: 7pt)
      *aml-qa/arkcli-eval-kit* 累计 *!8 + !61-!73*
      #v(0.15em)
      · *!63/!64/!68/!72/!73* 英文版 case 交付\
      · *!66* Runner regex bug 双修\
      · *!68* BP 1.0.11 alignment（billing / understand / custommodel）\
      · *!72* billing 截断 gate case\
      · *!73* v12 fail 10 条修（今天）
      #v(0.2em)
      #text(size: 7.5pt, weight: "bold", fill: rgb("#2a7a3a"))[Kit case 52 → 215]
      #linebreak() #v(-0.1em)
      #text(size: 7pt)[（chen 贡献 141 · 王鑫栋 74）]
      #v(0.15em)
      #ev("英文版 case 已经全交付（sheet X376djampooV + fumeng doc 英文）")
    ],
    fill: rgb("#e5f0f8"), stroke-color: rgb("#2c5985"),
  ),

  // 分支 4 · Pass rate 3 版
  node(
    "④ 3 版 pass rate 数据",
    [
      #set text(size: 7.5pt)
      *v10* · arkcli 1.0.9 · 140 case\
      → *100%* (83/83 real pass)
      #v(0.2em)
      *v11* · arkcli 1.0.11 · 140 case\
      → *97.6%*
      #v(0.2em)
      *v12* · arkcli 1.0.11 · 215 case（含王鑫栋 74）\
      → *79.2%*（chen own 部分仍 ~90%）
      #v(0.2em)
      #ev("这是简历数字。3 版趋势 = 覆盖扩 + baseline 回落 + 修回")
      #v(0.1em)
      #ev("07-30 付萌：会拉宇宁 + chen 对齐 v2 评测方案")
    ],
    fill: rgb("#fef7d7"), stroke-color: rgb("#8a7016"),
  ),

  // 分支 5 · 跨仓联动
  node(
    "⑤ 跨仓联动交付",
    [
      #set text(size: 7.3pt)
      *machinelearning/arkcli* · 3 MR merged\
      · *!379* MA SkillHub cleanup 3 处\
      · *!400* 淑华 custommodel zip merge\
      · *!413* 5 处 SKILL description 强化\
      \  (resources / helper / doctor / gen / usage)
      #v(0.2em)
      *tools/Ark_doc* · 2 MR merged\
      · *!1500* 30 MA API `.code.md` sidecar\
      · *!1752* MA hide\
      · *!1782* input_schema
      #v(0.2em)
      #ev("非 eval-kit 也在稳定输出，覆盖 skill 主仓 + Ark_doc")
    ],
    fill: rgb("#f5e7f4"), stroke-color: rgb("#7d3e75"),
  ),
)

#v(0.4em)

// 二级卡：BP MCP · 支撑动作 · 关联文档 · 未落 signals
#grid(
  columns: (1fr, 1fr, 1fr, 1fr),
  gutter: 5pt,

  node(
    "⑥ BP MCP + arkcli-bp 联调",
    [
      #set text(size: 7.5pt)
      · 07-24 18:44 范子卿追 chen：咋复现（chen 报过 BP issue）\
      · 07-25 20:57 雷宇宁：BP MCP mvp 已部署，你调 arkcli doc\
      · 07-25 23:21 chen：mvp 能跑 · 后续基于此调\
      · 07-27 16:41 chen 找雷：承接 `@byted-aml/ark-cli-bp` 海外产品\
      · 07-28 19:15 chen 复项：docs apis list/spec 正常 · URL 未写死支持环境变量
      #v(0.2em)
      #ev("chen 唯一一次给出结构化回执的动作，模板值得复用")
    ],
    fill: rgb("#f0e7f5"), stroke-color: rgb("#5c3e8a"),
  ),

  node(
    "⑦ 支撑动作（无 MR 但有产出）",
    [
      #set text(size: 7.5pt)
      · *SSO 5 天 debug*：沉淀 memory · 分析出需注册 2 个 OAuth client_id\
      · Kit reference doc `R1nJdkoA`\
      · 飞书扫描 doc `QhICdgVKJ`\
      · Managed-agent 9 case（`bp/cases/domains/managed-agent.yaml`）07-29 skill 验证已 cover\
      · 07-21 22:36 群里首交付原话公开
      #v(0.2em)
      #ev("这些没进 MR count，但在项目上下文有权重")
    ],
    fill: rgb("#e7f5f0"), stroke-color: rgb("#2a7a6a"),
  ),

  node(
    "⑧ 关联文档 & sheet",
    [
      #set text(size: 7.5pt)
      · sheet *X376djampooV* — 英文版 case 主 sheet\
      · sheet *ICUCdNme* — BP vs 火山差异清单（07-27 起付萌 own）\
      · doc *XOQEdlldFomWa7xW5ICct2tBnPh* — 付萌 v2 评测方案交付 doc\
      · doc *R1nJdkoA* — kit reference doc（chen 写）\
      · doc *QhICdgVKJ* — 飞书扫描 doc（chen 写）\
      · README `bp/README.md` §零→§八
      #v(0.2em)
      #ev("外部可引用 6 处，均活着")
    ],
    fill: rgb("#f5f0e7"), stroke-color: rgb("#7a6a2a"),
  ),

  node(
    "⑨ 未在图上但已知的动作",
    [
      #set text(size: 7.5pt)
      · 07-31 22:36 群里首交付原话 · lark-cli 关键词没直接命中 · 从 memory 补入\
      · 07-24 复现步骤 · 若走 P2P 私聊范子卿 · cross-app 拉不到\
      · MR!8 上王鑫栋 review 意见 · code.byted.org 侧 · 未 fetch\
      · 07-31 王鑫栋："agent 全面评审 P0 case · 两边都看看" · 尚未见 chen 回复动作\
      · 付萌 P2P 全部无法 fetch（open_id cross app）
      #v(0.2em)
      #ev("盲区诚实标出，评估自补")
    ],
    fill: rgb("#fdecec"), stroke-color: rgb("#8a2a2a"),
  ),
)

#v(0.4em)

// 最终三卡：硬数字 · gap · 判断
#grid(
  columns: (1fr, 1fr, 1fr),
  gutter: 6pt,

  node(
    "硬产出数字（08-03 快照 · 简历口径）",
    [
      #set text(size: 7.8pt)
      · *16 MR merged* 跨 3 仓（eval-kit 11 + arkcli 3 + Ark_doc 2）\
      · *Kit 215 case* · chen own 141（65%）\
      · *3 版 pass rate*：100% / 97.6% / 79.2%\
      · *5 处 SKILL description 强化*（arkcli MR!413）\
      · *Runner regex bug* 双修（MR!66）\
      · *BP 1.0.11 3 域 alignment*（billing / understand / custommodel）\
      · *managed-agent 9 case + SkillHub 3 处 cleanup*\
      · *MA docs*：30 API sidecar + hide + input_schema\
      · *SSO 5 天 debug*：沉淀 memory + OAuth 分析\
      · *README §零→§八* 321 行 + 3 家大厂 eval 归纳
    ],
    fill: rgb("#eef2f7"),
  ),

  node(
    "08-10 前还需做（诚实版 · 已重排）",
    [
      #set text(size: 7.8pt)
      · *v12 79.2% 回升*：MR!73 修 10 条只是第一批 · 后续 verify 是否稳定回到 ≥95%\
      · *v2 评测架构对齐会*：付萌等她整理完拉 chen + 雷 · 会前 chen 应准备一份 v2 提案而不是等\
      · *王鑫栋 07-31 P0 case 全面评审*：需 chen 给回复 · 目前尚未见到\
      · *bp README 更新到 v12*：README 还停在 12 skill × 52 case 的原始描述 · 应刷成 22 skill / 215 case / 3 版 pass rate\
      · *WangXindong 74 case 交接口径*：他 74 · chen 141 · 若 08-10 后交接需口径\
      · *bp-vs-volc-diff.md*：付萌 own · chen 需消费她的 sheet ICUCdNme 落地到 case
    ],
    fill: rgb("#fef3e7"),
  ),

  node(
    "关键判断（一句话）",
    [
      #set text(size: 8pt)
      过去一个月 chen 在 BP skill 线上*产出量已经不是实习生等级*——16 MR 跨 3 仓 · 215 case 里 own 65% · 3 版 pass rate 有连续 baseline。#linebreak()
      问题已经*不是"做不做得出"，而是"做完后有没有人知道"*。sheet 更新、README 刷版、王鑫栋 07-31 回复、v2 提案主动化——这些 5 分钟的"承重同步动作"你还缺。#linebreak()
      #text(fill: rgb("#c92626"), weight: "bold")[08-10 前，把 v12 pass rate 拉回 ≥95%，同时在评测群主动发一份《截止 08-03 累计交付》清单。这两件事决定组织记忆里你是"陈盈桦交付了"还是"付萌带着实习生交付了"。]
    ],
    fill: rgb("#1f3a5f"), stroke-color: rgb("#0d1b2a"), txt: white,
  ),
)
