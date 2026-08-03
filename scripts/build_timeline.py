#!/usr/bin/env python3
"""
build_timeline.py — 汇聚多源 chen 产出 → data/timeline.json:
- /tmp/timeline-scan/raw/*.json          飞书 25 群 6278 条
- ~/internship_workbench/                chen 自己写的 log/doc/sweep
- ~/.claude/projects/-/memory/*.md       memory 目录
- gh emptyteabot repos                    公开 GitHub 仓库时间戳
- 本地项目：~/daily-digest ~/mr-watcher ~/dev/* ~/codex_poc ~/lemonade-check
输出：
  data/timeline.json  · 按日期分组 · chen own 动作
"""
from __future__ import annotations
import json, pathlib, os, subprocess, re, hashlib
from datetime import datetime, timezone, timedelta

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT  = ROOT / "data" / "timeline.json"
CHEN_ID = "ou_b5ea2299548b7d3e7df1753c431b24fa"

def hash_id(oid):
    if not oid or not oid.startswith("ou_"): return oid
    if oid == CHEN_ID: return "chen"
    return "u_" + hashlib.sha1(oid.encode()).hexdigest()[:8]

def redact(t):
    if not isinstance(t, str): return t
    t = re.sub(r'ou_[a-f0-9]{32}', lambda m: hash_id(m.group(0)), t)
    t = re.sub(r'https?://\S+\.byted\.org\S*', '[internal-link]', t)
    t = re.sub(r'https?://\S+\.bytedance\.\S*', '[internal-link]', t)
    t = re.sub(r'http://10\.\d+\.\d+\.\d+:\d+/\S*', '[internal-preview]', t)
    return t

def read_lark_scan():
    """Return list of dicts per day per group where chen was author or @'d."""
    scan_dir = pathlib.Path('/tmp/timeline-scan/raw')
    events = []
    for f in scan_dir.glob('*.json'):
        chat_name = f.stem.split('_', 1)[1] if '_' in f.stem else f.stem
        try:
            msgs = json.load(open(f))
        except:
            continue
        for m in msgs:
            sender_id = m.get('sender',{}).get('id','')
            c = m.get('content','')
            if isinstance(c, dict): c = json.dumps(c, ensure_ascii=False)
            c = str(c)
            is_chen_sent = sender_id == CHEN_ID
            is_chen_mentioned = '陈盈桦' in c or CHEN_ID in c
            if not (is_chen_sent or is_chen_mentioned): continue
            date = m.get('create_time','')[:10]
            if not date: continue
            events.append({
                'date': date,
                'kind': 'lark-sent' if is_chen_sent else 'lark-mentioned',
                'chat': chat_name,
                'by': 'chen' if is_chen_sent else (m.get('sender',{}).get('name','')),
                'text': redact(c[:220]),
            })
    return events

def read_workbench_dates():
    """chen 自己 workbench 里所有 .md 的 mtime 视为她当天动作。"""
    events = []
    for base in [pathlib.Path.home()/'internship_workbench',
                 pathlib.Path.home()/'codex_poc',
                 pathlib.Path.home()/'lemonade-check',
                 pathlib.Path.home()/'dev/chen-delivery',
                 pathlib.Path.home()/'mr-watcher']:
        if not base.exists(): continue
        for f in base.rglob('*.md'):
            try:
                mt = datetime.fromtimestamp(f.stat().st_mtime, tz=timezone(timedelta(hours=8)))
                if mt < datetime(2026,6,17,tzinfo=timezone(timedelta(hours=8))): continue
                if mt > datetime(2026,8,4,tzinfo=timezone(timedelta(hours=8))): continue
                events.append({
                    'date': mt.strftime('%Y-%m-%d'),
                    'kind': 'workbench-doc',
                    'title': f.stem[:80],
                    'path': str(f.relative_to(pathlib.Path.home())),
                })
            except Exception as e:
                pass
    return events

def read_docs_authored_md():
    """Parse ~/internship_workbench/intern_review_../docs_authored.md if present."""
    events = []
    src = pathlib.Path.home()/'internship_workbench/intern_review_2026_06_17_to_2026_07_13/docs_authored.md'
    if not src.exists(): return events
    for line in src.read_text().splitlines():
        m = re.match(r'\|\s*\d+\s*\|\s*\*?\*?([^|]+?)\*?\*?\s*(?:\*\*\[重点主线\]\*\*)?\s*\|\s*(\w+)\s*\|\s*([\d\-T:+ ]+)\s*\|', line)
        if not m: continue
        title, doctype, ts = m.group(1).strip(), m.group(2), m.group(3)
        date = ts[:10]
        if '2026-' not in date: continue
        events.append({
            'date': date,
            'kind': 'lark-doc-authored',
            'title': title[:80],
            'doc_type': doctype,
        })
    return events

def read_github():
    """gh api events/created snapshots for emptyteabot repos in window."""
    events = []
    try:
        out = subprocess.check_output(['gh','repo','list','emptyteabot',
                                        '--limit','50','--json',
                                        'name,description,createdAt,pushedAt'],
                                       text=True, timeout=30)
        for r in json.loads(out):
            for kind,ts in [('gh-created', r['createdAt']),
                            ('gh-pushed',  r['pushedAt'])]:
                if not ts: continue
                d = ts[:10]
                if d < '2026-06-17' or d > '2026-08-03': continue
                events.append({
                    'date': d, 'kind': kind,
                    'title': r['name'], 'desc': (r.get('description') or '')[:80],
                })
    except Exception as e:
        pass
    return events

def read_memory():
    """chen memory dir mtimes."""
    events = []
    mem = pathlib.Path.home()/'.claude/projects/-Users-bytedance/memory'
    if not mem.exists(): return events
    for f in mem.glob('*.md'):
        try:
            mt = datetime.fromtimestamp(f.stat().st_mtime, tz=timezone(timedelta(hours=8)))
            if mt < datetime(2026,6,17,tzinfo=timezone(timedelta(hours=8))): continue
            events.append({
                'date': mt.strftime('%Y-%m-%d'),
                'kind': 'memory-saved',
                'title': f.stem,
            })
        except:
            pass
    return events

def main():
    all_events = []
    all_events += read_lark_scan()
    all_events += read_workbench_dates()
    all_events += read_docs_authored_md()
    all_events += read_github()
    all_events += read_memory()

    # bucket by date
    days = {}
    for e in all_events:
        days.setdefault(e['date'], []).append(e)

    # summarize per day: count by kind + top 3 samples
    summary = {}
    for date in sorted(days.keys()):
        items = days[date]
        by_kind = {}
        for e in items:
            by_kind.setdefault(e['kind'], []).append(e)
        summary[date] = {
            'total': len(items),
            'kinds': {k: len(v) for k,v in by_kind.items()},
            'samples': {
                k: [
                    ((e.get('title') or e.get('text') or e.get('desc') or '')[:100])
                    for e in v[:5]
                ]
                for k,v in by_kind.items()
            },
        }

    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps({
        'generated_at': datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
        'window': {'start': '2026-06-17', 'end': '2026-08-03'},
        'total_events': len(all_events),
        'days': summary,
    }, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f'[timeline] {len(all_events)} events across {len(summary)} days → {OUT}')

if __name__ == '__main__':
    main()
