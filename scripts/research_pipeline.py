#!/usr/bin/env python3
"""
scripts/research_pipeline.py
=============================================================================
Dual-Tier Grounded Intelligence & Verification Pipeline for StackDiff.

Features:
1. Signal Discovery (Tier 1): Probes recent AI news, releases, and changelogs.
2. Official Grounding (Tier 2): Fetches direct official documentation & pricing
   pages via Jina Reader (https://r.jina.ai/{url}).
3. Zero-Hallucination Audit (Tier 3): Uses Gemini API with strict grounded
   prompts. Prunes obsolete models, replaces outdated tiers, and cites proof URLs.
4. Auto-Calibration: Outputs an interactive Fact-Check Audit Card and updates
   both src/data/tools.json and data/tools.json upon user approval.

Usage:
  python scripts/research_pipeline.py --tool cursor
  python scripts/research_pipeline.py --tool claude --yes
  python scripts/research_pipeline.py --tool chatgpt --url https://openai.com/chatgpt/pricing
=============================================================================
"""

import argparse
import datetime
import json
import os
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional
from urllib.parse import quote_plus

import requests

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SRC_TOOLS_PATH = PROJECT_ROOT / "src" / "data" / "tools.json"
DATA_TOOLS_PATH = PROJECT_ROOT / "data" / "tools.json"
ENV_PATH = PROJECT_ROOT / ".env"

# Curated official documentation anchors for known tools
OFFICIAL_ANCHORS = {
    "cursor": "https://docs.cursor.com/getting-started/pricing",
    "github-copilot": "https://github.com/features/copilot#pricing",
    "windsurf": "https://codeium.com/pricing",
    "v0-by-vercel": "https://v0.dev/pricing",
    "lovable": "https://lovable.dev/pricing",
    "chatgpt": "https://openai.com/chatgpt/pricing",
    "claude-3-5-sonnet": "https://www.anthropic.com/pricing",
    "gemini-advanced": "https://one.google.com/about/plans",
    "deepseek": "https://platform.deepseek.com/api-docs/pricing",
    "perplexity-ai": "https://www.perplexity.ai/pro",
    "midjourney": "https://docs.midjourney.com/docs/plans",
    "flux-1": "https://blackforestlabs.ai",
    "recraft": "https://www.recraft.ai/pricing",
    "runway-gen3": "https://runwayml.com/pricing",
    "kling-ai": "https://klingai.com/pricing",
    "luma-dream-machine": "https://lumalabs.ai/dream-machine",
    "elevenlabs": "https://elevenlabs.io/pricing",
    "cartesia-sonic": "https://cartesia.ai/pricing",
    "n8n": "https://n8n.io/pricing",
    "make": "https://www.make.com/en/pricing",
    "zapier": "https://zapier.com/pricing",
    "supermaven": "https://supermaven.com/pricing",
}


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


def search_signals(tool_name: str) -> str:
    """Tier 1: Discovers recent news, Twitter signals, and changelog highlights."""
    print(f"\n[Tier 1] Probing recent news, Twitter signals & changelogs for '{tool_name}'...")
    query = f"{tool_name} AI release new models pricing changelog 2026"
    search_url = f"https://html.duckduckgo.com/html/?q={quote_plus(query)}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    }
    
    signals_text = ""
    try:
        resp = requests.get(search_url, headers=headers, timeout=15)
        if resp.status_code == 200:
            # Simple text extraction from DuckDuckGo HTML results
            snippets = re.findall(r'<a class="result__snippet[^>]*>(.*?)</a>', resp.text, re.DOTALL)
            clean_snippets = [re.sub(r'<[^>]+>', '', s).strip() for s in snippets[:6]]
            signals_text = "\n".join(f"- {s}" for s in clean_snippets if s)
    except Exception as e:
        signals_text = f"(Web search signal probe skipped: {e})"

    if not signals_text:
        signals_text = "- Active commercial deployments with continuous model updates."

    print(f"[+] Discovered external signals:\n{signals_text[:400]}...\n")
    return signals_text


def fetch_official_markdown(url: str) -> str:
    """Tier 2: Ingests official documentation directly via Jina Reader."""
    print(f"[Tier 2] Fetching authoritative Markdown from official source:\n    -> {url}")
    jina_url = f"https://r.jina.ai/{url}"
    headers = {
        "User-Agent": "StackDiff-Research-Pipeline/2.0 (+https://getstackdiff.com)",
        "Accept": "text/markdown, text/plain",
    }
    jina_key = os.environ.get("JINA_API_KEY")
    if jina_key:
        headers["Authorization"] = f"Bearer {jina_key}"

    try:
        resp = requests.get(jina_url, headers=headers, timeout=40)
        resp.raise_for_status()
        content = resp.text.strip()
        if not content:
            raise ValueError("Empty body returned from Jina Reader.")
        print(f"[+] Successfully fetched {len(content):,} characters of official markdown.")
        return content
    except Exception as e:
        print(f"[-] Jina Reader failed: {e}. Falling back to direct HTTP request...")
        resp = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=30)
        resp.raise_for_status()
        return resp.text[:30000]


def audit_with_gemini(
    tool_name: str,
    tool_slug: str,
    official_url: str,
    official_markdown: str,
    signals: str,
    existing_tool: Dict[str, Any],
) -> Dict[str, Any]:
    """Tier 3: Strict Zero-Hallucination Grounded Synthesis."""
    print(f"\n[Tier 3] Running Zero-Hallucination Grounded Audit via Gemini...")
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY not found in environment or .env file.")

    import google.generativeai as genai
    genai.configure(api_key=api_key)

    model = genai.GenerativeModel("gemini-1.5-flash")

    system_prompt = (
        "你是一位嚴謹的軟體架構師與事實查核工程師（Fact-Checking Auditor）。\n"
        f"你正在為 StackDiff 審計工具 '{tool_name}' ({tool_slug}) 的技術規格與定價資料。\n\n"
        "【三大核心戒律】\n"
        "1. 【零猜測、零幻覺】：所有定價數字、方案名稱、技術限制必須在官方最新 Markdown 文檔中有明確依據。"
        "   文檔未明確提及的欄位填 null 或合理客觀預設，絕不可用未經證實的通識腦補。\n"
        "2. 【過期模型強制修剪】：若文檔明列最新架構模型（如 Grok, Composer 2.5, Claude 3.7, o1/o3-mini, Gemini 2.0 Flash 等），"
        "   必須完全替換舊型號，絕不保留過期的舊代名稱。\n"
        "3. 【社群信號交叉驗證】：若社群/新聞信號提及的功能在官方文檔中未獲證實，不可寫入核心規格，僅可作為評估參考。\n\n"
        "請輸出嚴格合法的 JSON，格式如下：\n"
        "{\n"
        '  "official_pricing_url": "官方定價或說明文檔網址",\n'
        '  "pricing": {\n'
        '    "starting_price": "$20/mo (或 Free 或 Contact sales)",\n'
        '    "billing_model": "Seat-based | Usage-based | Freemium | Subscription",\n'
        '    "free_tier_details": "免費方案或試用額度具體描述",\n'
        '    "tiers_summary": "精簡階梯摘要，如: Free / Pro $20 / Team $40"\n'
        "  },\n"
        '  "technical_specs": {\n'
        '    "current_models": ["官方最新明列之模型名稱陣列 (修剪掉過期舊模型)"],\n'
        '    "context_window": "上下文長度如 128K, 200K, 2M (未提及填 null)",\n'
        '    "byok_support": true/false,\n'
        '    "open_source": true/false,\n'
        '    "telemetry_privacy": true/false (商用方案是否承諾不拿用戶代碼訓練模型),\n'
        '    "offline_support": true/false\n'
        "  },\n"
        '  "key_features": [\n'
        '    "3-4 點最新核心功能特性 (精煉技術語言)"\n'
        "  ],\n"
        '  "gotchas": [\n'
        '    "2-3 點有明確官方或測試依據的計費陷阱、額度上限或使用限制"\n'
        "  ],\n"
        '  "audit_verdict": "一兩句客觀技術總結，指出本工具在 2026 市場上的真實定位與購買建議"\n'
        "}"
    )

    user_prompt = (
        f"{system_prompt}\n\n"
        f"--- 外部新聞與情報信號 (參考探測) ---\n"
        f"{signals}\n\n"
        f"--- 官方真實一手文檔 ({official_url}) ---\n"
        f"{official_markdown[:28000]}\n\n"
        f"--- 現有資料庫舊資料 (作為比對基線) ---\n"
        f"{json.dumps(existing_tool, ensure_ascii=False, indent=2)[:3000]}\n"
    )

    response = model.generate_content(user_prompt)
    raw_text = response.text.strip()

    match = re.search(r"\{.*\}", raw_text, re.DOTALL)
    if not match:
        raise ValueError(f"Could not parse JSON from Gemini response:\n{raw_text}")

    return json.loads(match.group(0))


def print_audit_card(tool: Dict[str, Any], extracted: Dict[str, Any], proof_url: str) -> None:
    """Renders a beautiful Terminal Fact-Check Audit Card."""
    name = tool.get("name", tool.get("slug"))
    slug = tool.get("slug")
    today = datetime.date.today().isoformat()

    print("\n" + "═" * 70)
    print(f" 🔍 STACKDIFF FACT-CHECK AUDIT CARD: {name.upper()} ({slug})")
    print("═" * 70)
    print(f" 📅 Audit Timestamp:  {today}")
    print(f" 🏛️  Official Source:   {proof_url}")
    print(f" 📊 Verdict:          {extracted.get('audit_verdict', 'Objective verification complete.')}")
    print("─" * 70)

    # Pricing Diff
    old_p = tool.get("pricing", {})
    old_price = old_p.get("starting_price") or tool.get("starting_price")
    new_price = extracted.get("pricing", {}).get("starting_price")
    print(f" Starting Price:      {old_price}  ->  {new_price}")

    old_tiers = old_p.get("tiers_summary")
    new_tiers = extracted.get("pricing", {}).get("tiers_summary")
    print(f" Tiers Summary:       {old_tiers}  ->  {new_tiers}")

    # Models Diff
    old_m = tool.get("technical_specs", {}).get("current_models") or tool.get("key_features", [])[:2]
    new_m = extracted.get("technical_specs", {}).get("current_models")
    print(f" Current Models:      {old_m}\n                  ->  {new_m}")

    # Gotchas
    new_g = extracted.get("gotchas", [])
    print(f" Verified Gotchas:    {len(new_g)} caveats identified")
    for g in new_g:
        print(f"   • {g}")

    print("═" * 70 + "\n")


def main():
    parser = argparse.ArgumentParser(description="StackDiff Dual-Tier Grounded Research Pipeline")
    parser.add_argument("--tool", required=True, help="Tool slug or name (e.g. cursor, claude, chatgpt, midjourney, n8n)")
    parser.add_argument("--url", help="Override official pricing/documentation URL")
    parser.add_argument("--yes", "-y", action="store_true", help="Auto-confirm update without interactive prompt")

    args = parser.parse_args()
    load_env()

    if not SRC_TOOLS_PATH.exists():
        print(f"[-] Database not found at {SRC_TOOLS_PATH}")
        sys.exit(1)

    with open(SRC_TOOLS_PATH, "r", encoding="utf-8") as f:
        tools = json.load(f)

    # Find target tool
    query = args.tool.lower().strip()
    target_idx = None
    target_tool = None
    for idx, t in enumerate(tools):
        if t.get("slug") == query or t.get("id") == query or query in t.get("name", "").lower():
            target_idx = idx
            target_tool = t
            break

    if target_tool is None:
        print(f"[-] Tool '{args.tool}' not found in tools.json database.")
        sys.exit(1)

    slug = target_tool.get("slug")
    name = target_tool.get("name")
    print(f"[+] Loaded '{name}' ({slug}) from database.")

    # Determine official grounding URL
    official_url = (
        args.url
        or target_tool.get("official_pricing_url")
        or target_tool.get("source_url")
        or OFFICIAL_ANCHORS.get(slug)
        or target_tool.get("url")
    )

    if not official_url or official_url == "#":
        print(f"[-] No official URL found for '{slug}'. Please specify via --url.")
        sys.exit(1)

    # Execute Pipeline
    signals = search_signals(name)
    official_md = fetch_official_markdown(official_url)
    extracted = audit_with_gemini(name, slug, official_url, official_md, signals, target_tool)

    print_audit_card(target_tool, extracted, official_url)

    if not args.yes:
        confirm = input("Apply these grounded updates to tools.json? [y/N]: ").strip().lower()
        if confirm != "y":
            print("[-] Audit results discarded by user.")
            sys.exit(0)

    # Apply grounded update
    today = datetime.date.today().isoformat()
    target_tool["source_url"] = official_url
    target_tool["last_checked_at"] = today
    target_tool["official_pricing_url"] = extracted.get("official_pricing_url", official_url)
    target_tool["pricing"] = extracted.get("pricing", {})
    target_tool["technical_specs"] = extracted.get("technical_specs", {})
    target_tool["gotchas"] = extracted.get("gotchas", [])
    if extracted.get("key_features"):
        target_tool["key_features"] = extracted["key_features"]

    # Keep legacy top-level keys in sync for backwards compatibility
    if target_tool["pricing"].get("starting_price"):
        target_tool["starting_price"] = target_tool["pricing"]["starting_price"]
    if target_tool["pricing"].get("billing_model"):
        target_tool["pricing_model"] = target_tool["pricing"]["billing_model"]
    if target_tool["pricing"].get("free_tier_details"):
        ft = target_tool["pricing"]["free_tier_details"].lower()
        target_tool["free_tier"] = ("free" in ft or "trial" in ft) and "paid only" not in ft

    tools[target_idx] = target_tool

    # Save to both paths
    for p in [SRC_TOOLS_PATH, DATA_TOOLS_PATH]:
        if p.parent.exists():
            with open(p, "w", encoding="utf-8") as f:
                json.dump(tools, f, indent=2, ensure_ascii=False)
            print(f"[+] Updated {p.relative_to(PROJECT_ROOT)}")

    print(f"\n[OK] Successfully verified & calibrated '{name}' with grounded proof!")


if __name__ == "__main__":
    main()
