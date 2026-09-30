#!/usr/bin/env python3
"""
scripts/verify_tool.py
=============================================================================
Official Grounded Data Verification Pipeline for StackDiff.
Uses Jina Reader (https://r.jina.ai/{url}) to ingest official web docs
and Gemini API with strict grounded prompts to prune stale models and extract
canonical pricing & technical specifications.

Usage:
  python scripts/verify_tool.py --slug cursor --url https://docs.cursor.com/getting-started/pricing
  python scripts/verify_tool.py --slug chatgpt --url https://openai.com/chatgpt/pricing --yes
=============================================================================
"""

import argparse
import datetime
import json
import os
import re
import sys
from pathlib import Path
from typing import Any, Dict, Optional

import requests

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SRC_TOOLS_PATH = PROJECT_ROOT / "src" / "data" / "tools.json"
DATA_TOOLS_PATH = PROJECT_ROOT / "data" / "tools.json"
ENV_PATH = PROJECT_ROOT / ".env"


def load_env() -> None:
    """Manually parse .env without external python-dotenv dependency."""
    if ENV_PATH.exists():
        with open(ENV_PATH, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    k = k.strip()
                    v = v.strip().strip('"').strip("'")
                    os.environ.setdefault(k, v)


def fetch_markdown_via_jina(url: str) -> str:
    """Fetches real-time clean markdown of any URL via Jina Reader."""
    jina_url = f"https://r.jina.ai/{url}"
    headers = {
        "User-Agent": "StackDiff-Grounded-Verifier/1.0 (+https://getstackdiff.com)",
        "Accept": "text/markdown, text/plain",
    }
    jina_key = os.environ.get("JINA_API_KEY")
    if jina_key:
        headers["Authorization"] = f"Bearer {jina_key}"

    print(f"[*] Fetching live markdown from Jina Reader: {jina_url}...")
    try:
        resp = requests.get(jina_url, headers=headers, timeout=40)
        resp.raise_for_status()
        content = resp.text.strip()
        if not content:
            raise ValueError("Received empty content from Jina Reader.")
        print(f"[+] Successfully fetched {len(content):,} characters of markdown.")
        return content
    except Exception as e:
        print(f"[-] Jina Reader fetch failed: {e}")
        print("[*] Falling back to direct URL request...")
        resp = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=30)
        resp.raise_for_status()
        return resp.text[:30000]


def extract_with_gemini(markdown_content: str, tool_slug: str, target_url: str) -> Dict[str, Any]:
    """Uses Gemini API to groundedly extract canonical specs and prune stale models."""
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY not found in environment or .env file.")

    import google.generativeai as genai
    genai.configure(api_key=api_key)

    model_name = "gemini-1.5-flash"
    try:
        model = genai.GenerativeModel(model_name)
    except Exception:
        model = genai.GenerativeModel("gemini-pro")

    system_instruction = (
        "你是一位嚴謹的資料工程師與軟體架構師。請僅依據以下抓取的官方最新 Markdown 內文，"
        f"提取目標工具 '{tool_slug}' 的定價、支援模型、計費限制等欄位。\n\n"
        "【嚴格提取守則】\n"
        "1. 嚴禁利用未提及的舊記憶或通識幻覺進行猜測。官方文件沒提到的欄位一律填 null 或合理的客觀預設。\n"
        "2. 若官方文件列出最新模型，舊模型一律替換淘汰，嚴禁進行歷史累積。\n"
        "3. 請輸出嚴格合法的 JSON 格式，不要包含額外的 Markdown 標籤外的文字。\n\n"
        "【輸出 JSON 綱要】\n"
        "{\n"
        '  "official_pricing_url": "官方定價頁網址 (字串)",\n'
        '  "pricing": {\n'
        '    "starting_price": "$20/mo (字串，若免費則填 Free，若無明確起價填 Contact sales)",\n'
        '    "billing_model": "Seat-based | Usage-based | Freemium | Subscription",\n'
        '    "free_tier_details": "免費額度或試用期詳細說明 (字串)",\n'
        '    "tiers_summary": "各方案價格簡寫 (如: Free / Pro $20 / Team $40)"\n'
        "  },\n"
        '  "technical_specs": {\n'
        '    "current_models": ["官方文件中最新明列支援的模型清單字串陣列"],\n'
        '    "context_window": "如 128K, 200K, 1M (若無提及填 null)",\n'
        '    "byok_support": true/false,\n'
        '    "open_source": true/false,\n'
        '    "telemetry_privacy": true/false (是否保證不使用用戶程式碼/資料訓練模型),\n'
        '    "offline_support": true/false\n'
        "  },\n"
        '  "gotchas": [\n'
        '    "有明確官方/測試依據的定價限制、用量上限或使用條件 (2-3 點精簡字串)"\n'
        "  ]\n"
        "}"
    )

    prompt = (
        f"{system_instruction}\n\n"
        f"--- 來源網址: {target_url} ---\n"
        f"--- 官方文檔內容開始 ---\n"
        f"{markdown_content[:25000]}\n"
        f"--- 官方文檔內容結束 ---\n"
    )

    print(f"[*] Prompting Gemini ({model_name}) for grounded extraction & pruning...")
    response = model.generate_content(prompt)
    raw_text = response.text.strip()

    # Extract JSON object from code blocks
    match = re.search(r"\{.*\}", raw_text, re.DOTALL)
    if not match:
        raise ValueError(f"Could not parse valid JSON from Gemini response:\n{raw_text}")

    extracted = json.loads(match.group(0))
    return extracted


def load_tools_db() -> list:
    if not SRC_TOOLS_PATH.exists():
        raise FileNotFoundError(f"{SRC_TOOLS_PATH} not found.")
    with open(SRC_TOOLS_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def save_tools_db(tools: list) -> None:
    for path in [SRC_TOOLS_PATH, DATA_TOOLS_PATH]:
        if path.parent.exists():
            with open(path, "w", encoding="utf-8") as f:
                json.dump(tools, f, indent=2, ensure_ascii=False)
            print(f"[+] Saved updated database to {path.relative_to(PROJECT_ROOT)}")


def print_diff(old_tool: Dict[str, Any], extracted: Dict[str, Any], source_url: str, check_date: str) -> None:
    print("\n" + "=" * 60)
    print(f"DIFF PREVIEW: {old_tool.get('name', 'Unknown')} ({old_tool.get('slug')})")
    print("=" * 60)

    # Pricing
    old_p = old_tool.get("pricing", {})
    old_price = old_p.get("starting_price") or old_tool.get("starting_price")
    new_price = extracted.get("pricing", {}).get("starting_price")
    print(f"Starting Price:      {old_price}  ->  {new_price}")

    old_tiers = old_p.get("tiers_summary")
    new_tiers = extracted.get("pricing", {}).get("tiers_summary")
    print(f"Tiers Summary:       {old_tiers}  ->  {new_tiers}")

    # Models
    old_m = old_tool.get("technical_specs", {}).get("current_models") or old_tool.get("key_features", [])[:2]
    new_m = extracted.get("technical_specs", {}).get("current_models")
    print(f"Current Models:      {old_m}  ->  {new_m}")

    # Gotchas
    old_g = old_tool.get("gotchas") or old_tool.get("cons")
    new_g = extracted.get("gotchas")
    print(f"Gotchas:             {old_g}  ->  {new_g}")

    # Provenance
    print(f"Source URL:          {source_url}")
    print(f"Last Checked At:     {check_date}")
    print("=" * 60 + "\n")


def main():
    parser = argparse.ArgumentParser(description="StackDiff Grounded Tool Verifier")
    parser.add_argument("--slug", required=True, help="Tool slug (e.g. cursor, chatgpt, github-copilot)")
    parser.add_argument("--url", required=True, help="Official pricing / documentation URL")
    parser.add_argument("--yes", "-y", action="store_true", help="Auto-confirm without interactive prompt")

    args = parser.parse_args()
    load_env()

    tools = load_tools_db()
    target_idx = None
    target_tool = None
    for idx, t in enumerate(tools):
        if t.get("slug") == args.slug or t.get("id") == args.slug:
            target_idx = idx
            target_tool = t
            break

    if target_tool is None:
        print(f"[-] Tool with slug '{args.slug}' not found in database.")
        sys.exit(1)

    print(f"[*] Found tool '{target_tool.get('name')}' ({args.slug})")

    markdown = fetch_markdown_via_jina(args.url)
    extracted = extract_with_gemini(markdown, args.slug, args.url)

    today = datetime.date.today().isoformat()
    print_diff(target_tool, extracted, args.url, today)

    if not args.yes:
        confirm = input("Apply these grounded updates to tools.json? [y/N]: ").strip().lower()
        if confirm != "y":
            print("[-] Aborted by user.")
            sys.exit(0)

    # Apply updates
    target_tool["source_url"] = args.url
    target_tool["last_checked_at"] = today
    if extracted.get("official_pricing_url"):
        target_tool["official_pricing_url"] = extracted["official_pricing_url"]
    else:
        target_tool.setdefault("official_pricing_url", args.url)

    target_tool["pricing"] = extracted.get("pricing", {})
    target_tool["technical_specs"] = extracted.get("technical_specs", {})
    target_tool["gotchas"] = extracted.get("gotchas", [])

    # Keep backwards-compatible top-level keys in sync
    if target_tool["pricing"].get("starting_price"):
        target_tool["starting_price"] = target_tool["pricing"]["starting_price"]
    if target_tool["pricing"].get("billing_model"):
        target_tool["pricing_model"] = target_tool["pricing"]["billing_model"]
    if target_tool["pricing"].get("free_tier_details"):
        ft = target_tool["pricing"]["free_tier_details"].lower()
        target_tool["free_tier"] = ("free" in ft or "trial" in ft) and "paid only" not in ft

    tools[target_idx] = target_tool
    save_tools_db(tools)
    print(f"[✓] Successfully updated and verified '{args.slug}' at {today}!")


if __name__ == "__main__":
    main()
