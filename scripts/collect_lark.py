#!/usr/bin/env python3
"""
collect_lark.py — 每日拉取过去 30 天飞书方舟文档 + BP 相关群消息 + P2P，落到 data/YYYY-MM-DD/。
用 lark-cli (chen 已装, refresh token 到 2026-07-09 之后需 chen 定期重登)。
输出脱敏后的 JSON — openId 用 sha1 前 8 位替代，绝不落 raw token。
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
LARK_CLI = "/opt/homebrew/bin/lark-cli"

# 相关群 chat_id
CHATS = {
    "方舟文档小分队":     "oc_6b697a54265ac86efadcab1d0b66ead9",
    "方舟文档工程组":     "oc_87d3568dbe1cf96b5985bee408a9fabc",
    "arkcli评测开发":     "oc_0180b16aecb9daeaa0b63199316e733f",
    "arkcli支持byteplus": "oc_feb2b0e7f4d797e1d198aae80f4a683c",
    "MA支持BytePlus":     "oc_800e7639b6fc80f4bb1c85d1d82cedfc",
}

CHEN = "ou_b5ea2299548b7d3e7df1753c431b24fa"


def hash_id(oid: str) -> str:
    if not oid or not oid.startswith("ou_"):
        return oid
    if oid == CHEN:
        return "chen"
    return "u_" + hashlib.sha1(oid.encode()).hexdigest()[:8]


def redact(obj):
    """Recursively hash all openIds in the payload."""
    if isinstance(obj, dict):
        return {k: redact(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [redact(x) for x in obj]
    if isinstance(obj, str) and obj.startswith("ou_") and len(obj) > 20:
        return hash_id(obj)
    return obj


def pull_chat(chat_id: str, start: str, end: str) -> list:
    msgs = []
    page_token = ""
    for _ in range(200):  # safety cap
        cmd = [
            LARK_CLI, "im", "+chat-messages-list",
            "--chat-id", chat_id, "--start", start, "--end", end,
            "--page-size", "50", "--order", "desc", "--no-reactions",
        ]
        if page_token:
            cmd += ["--page-token", page_token]
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
        try:
            d = json.loads(r.stdout)
        except Exception:
            sys.stderr.write(f"parse err chat={chat_id[:12]}: {r.stdout[:200]}\n")
            break
        if not d.get("ok"):
            sys.stderr.write(f"api err chat={chat_id[:12]}: {d.get('error')}\n")
            break
        msgs.extend(d.get("data", {}).get("messages", []))
        page_token = d.get("data", {}).get("page_token") or ""
        if not d.get("data", {}).get("has_more") or not page_token:
            break
    return msgs


def summarize(msgs: list) -> dict:
    """Extract chen-relevant summary from redacted messages."""
    chen_sent = [m for m in msgs if m.get("sender", {}).get("id") == "chen"]
    chen_mentions = []
    for m in msgs:
        c = m.get("content", "")
        c = json.dumps(c, ensure_ascii=False) if isinstance(c, dict) else str(c)
        if "陈盈桦" in c and m.get("sender", {}).get("id") != "chen":
            chen_mentions.append(m)
    return {
        "total": len(msgs),
        "chen_sent": len(chen_sent),
        "chen_mentions": len(chen_mentions),
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--since-days", type=int, default=30)
    ap.add_argument("--date", default=None, help="Snapshot date YYYY-MM-DD (default: today)")
    args = ap.parse_args()

    snap_date = args.date or dt.date.today().isoformat()
    start = (dt.date.fromisoformat(snap_date) - dt.timedelta(days=args.since_days)).isoformat() + "T00:00:00Z"
    end = snap_date + "T23:59:59Z"

    out_dir = DATA / snap_date
    out_dir.mkdir(parents=True, exist_ok=True)

    index = {"date": snap_date, "window_start": start, "window_end": end, "chats": {}}
    for name, cid in CHATS.items():
        msgs = pull_chat(cid, start, end)
        redacted = [redact(m) for m in msgs]
        fname = out_dir / f"lark_{name}.json"
        fname.write_text(json.dumps(redacted, ensure_ascii=False), encoding="utf-8")
        index["chats"][name] = summarize(redacted)
        sys.stderr.write(f"[{name}] {index['chats'][name]}\n")

    (out_dir / "lark_index.json").write_text(json.dumps(index, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(index, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
