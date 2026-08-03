# career-log

**陈盈桦 · Ian Chen 的每日更新简历系统。**

从 2026-06-17 入职字节跳动 Data-AML 火山方舟起，每天自动扫飞书消息 + 拉 code.byted.org MR 元数据 + 备份记忆 + 编译 Typst 简历 → 归档 PDF → 部署到 GitHub Pages。

**主页**：https://emptyteabot.github.io/career-log/

**为什么**：离职当天我可以关电脑走人，仓库里 6 个月的历史快照 + 生成代码永远可回放。

## 结构

```
career-log/
├── homepage/            GitHub Pages 静态站
│   ├── index.html       主页（动态粒子 + 硅谷简洁风）
│   ├── assets/          CSS + JS
│   └── resume/          PDF 归档 + manifest.json
├── resumes/             本地 PDF 归档（每日 3 份：general / deepseek / mindmap）
├── templates/           Typst 模板
│   ├── common.typ       共享排版
│   ├── resume-*.typ     手写的初版
│   ├── mindmap-latest.typ  BP skill 线思维导图
│   └── build/           自动生成的每日 .typ 快照
├── data/                每日采集的原始数据（脱敏 openId）
│   └── state.json       项目当前状态（可写入的 source of truth）
├── memory-archive/      Claude Code memory 每日备份（脱敏）
├── scripts/             全部工具脚本
│   ├── collect_lark.py  拉飞书消息
│   ├── backup_memory.sh 备份 memory
│   ├── build_resume.py  按 state.json 渲染当日简历
│   ├── compile.sh       typst → PDF
│   ├── backfill.py      一次性回填历史 47 天
│   ├── update_manifest.py  刷 homepage/resume/manifest.json
│   ├── update_homepage.py  日常同步 latest-*.pdf
│   ├── daily.sh         主 orchestrator（launchd 调用）
│   └── cc.chenyinghua.career-log.plist  macOS launchd 每天凌晨 3 点跑
└── .github/workflows/
    └── build-and-deploy.yml   每日 UTC 19:00 = 北京 03:00 自动跑 + Pages 部署
```

## 手动跑

```bash
cd ~/career-log

# 立即产出今天的 PDF
python3 scripts/build_resume.py --date $(date +%Y-%m-%d)
bash scripts/compile.sh $(date +%Y-%m-%d)

# 或者跑完整 daily 流程
bash scripts/daily.sh

# 只是刷 manifest / 更新主页
python3 scripts/update_homepage.py

# 打开最新简历
open resumes/latest-general.pdf
```

## 装 launchd（本地 macOS 每天自动跑）

```bash
cp scripts/cc.chenyinghua.career-log.plist ~/Library/LaunchAgents/
launchctl load ~/Library/LaunchAgents/cc.chenyinghua.career-log.plist
launchctl start cc.chenyinghua.career-log  # 立刻测试跑一次
```

## GitHub Actions

- 每天 UTC 19:00（北京 03:00）自动 rebuild + deploy Pages
- 也可以在仓库 Actions tab 手动触发（workflow_dispatch）
- 会往 main 分支 commit `auto: refresh YYYY-MM-DD`

## 状态更新（简历硬数字）

改 `data/state.json` 里的 `hard_numbers` 字段。build_resume.py 会按日期插值出成长曲线。当天跑 build_resume.py 会读最新的 state。

如果要往 state.json 加新的 MR 号或 case 数增长，直接编辑 JSON，下次快照自动生效。

## 隐私红线

`.gitignore` 排除：
- `data/*/lark_*.json`（飞书 raw 消息，可能含少量未脱敏字段）
- 任何 `.env` `.env.*` `cookies.txt`

data/ 里所有 openId 用 sha1 前 8 位替代。**永远不要**把飞书 refresh token / GitLab cookie 提交到仓库。

## 联系

hi@[13398580812@163.com](mailto:13398580812@163.com)
