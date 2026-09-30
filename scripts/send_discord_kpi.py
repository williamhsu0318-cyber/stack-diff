#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scripts/send_discord_kpi.py
==============================================================================
StackDiff 30-Day Observation Phase: Discord KPI Sentinel & Master Sheet Reporter
Sends structured 10-KPI cards, 5-number conversion funnels, and category breakdowns
directly to Discord for real-time mobile and desktop monitoring.
==============================================================================
"""

import os
import sys
import json
import argparse
import urllib.request
import urllib.error
from datetime import datetime
from typing import Dict, Any, Tuple, Optional

# Ensure UTF-8 output on Windows console
if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

# Constants & Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
METRICS_PATH = os.path.join(BASE_DIR, "data", "kpi_metrics.json")
ENV_PATH = os.path.join(BASE_DIR, ".env")

def get_env_var(key: str) -> Optional[str]:
    """Retrieve environment variable from .env or os.environ."""
    if os.path.exists(ENV_PATH):
        try:
            with open(ENV_PATH, "r", encoding="utf-8") as f:
                for line in f:
                    clean = line.strip()
                    if clean.startswith(f"{key}="):
                        return clean.split("=", 1)[1].strip()
        except Exception:
            pass
    return os.environ.get(key)

def load_kpi_metrics() -> Dict[str, Any]:
    """Loads current KPI metrics from data/kpi_metrics.json."""
    if os.path.exists(METRICS_PATH):
        try:
            with open(METRICS_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"Warning: Failed to parse {METRICS_PATH}: {e}")
    
    # Default fallback template
    return {
        "observation_phase": {
            "start_date": "2026-09-30",
            "target_days": 30,
            "current_day": 1,
            "scope_locked": "23 Tools / 36 Diffs"
        },
        "summary": {
            "total_impressions": 0,
            "total_clicks": 0,
            "pages_with_clicks": 0,
            "total_cta_clicks": 0,
            "total_signups": 0,
            "total_revenue": 0.0,
            "overall_ctr": "0.0%",
            "overall_cta_ctr": "0.0%"
        },
        "categories": {
            "Coding AI": {"pairs_count": 10, "impressions": 0, "clicks": 0, "cta_clicks": 0},
            "LLM": {"pairs_count": 10, "impressions": 0, "clicks": 0, "cta_clicks": 0},
            "Workflow AI": {"pairs_count": 3, "impressions": 0, "clicks": 0, "cta_clicks": 0},
            "Image AI": {"pairs_count": 6, "impressions": 0, "clicks": 0, "cta_clicks": 0},
            "Video AI": {"pairs_count": 6, "impressions": 0, "clicks": 0, "cta_clicks": 0},
            "Voice AI": {"pairs_count": 1, "impressions": 0, "clicks": 0, "cta_clicks": 0}
        },
        "top_queries": [],
        "comparisons": []
    }

def format_number(val: Any) -> str:
    """Formats numeric values with commas or currency."""
    if isinstance(val, (int, float)):
        return f"{val:,}" if isinstance(val, int) else f"{val:,.2f}"
    return str(val)

def build_discord_payload(data: Dict[str, Any], mode: str = "summary") -> Dict[str, Any]:
    """
    Builds the Discord Rich Embed payload adhering to the ChatGPT 10-KPI framework.
    """
    summary = data.get("summary", {})
    categories = data.get("categories", {})
    top_queries = data.get("top_queries", [])
    phase = data.get("observation_phase", {})

    total_imp = summary.get("total_impressions", 0)
    total_clicks = summary.get("total_clicks", 0)
    pages_with_clicks = summary.get("pages_with_clicks", 0)
    total_cta = summary.get("total_cta_clicks", 0)
    total_signups = summary.get("total_signups", 0)
    total_rev = summary.get("total_revenue", 0.0)

    ctr = summary.get("overall_ctr", "0.0%")
    cta_ctr = summary.get("overall_cta_ctr", "0.0%")
    curr_day = phase.get("current_day", 1)
    target_days = phase.get("target_days", 30)

    # 5-Number Funnel Strip
    funnel_str = (
        f"**`{format_number(total_imp)}`** Impressions ➔ "
        f"**`{format_number(total_clicks)}`** Clicks ➔ "
        f"**`{format_number(pages_with_clicks)}`** Pages w/ Clicks ➔ "
        f"**`{format_number(total_cta)}`** CTA Clicks ➔ "
        f"**`${format_number(total_rev)}`** Revenue"
    )

    # Queries formatting
    if top_queries:
        queries_str = "\n".join([f"• `{q.get('query')}` ({q.get('clicks', 0)} clicks / {q.get('impressions', 0)} imp)" for q in top_queries[:5]])
    else:
        queries_str = "• *(GSC 數據爬梳中，新頁面通常於 7~14 天陸續出水)*"

    # Category rollup breakdown
    cat_lines = []
    for cat_name, cdata in categories.items():
        c_imp = cdata.get("impressions", 0)
        c_clicks = cdata.get("clicks", 0)
        c_cta = cdata.get("cta_clicks", 0)
        pairs_cnt = cdata.get("pairs_count", 0)
        cat_lines.append(f"• **{cat_name}** ({pairs_cnt} pairs): `{c_imp}` imp | `{c_clicks}` clicks | `{c_cta}` CTA")
    categories_str = "\n".join(cat_lines)

    title = "📊【StackDiff】30天觀測期：10 大核心 KPI 追蹤週報" if mode == "weekly" else "📊【StackDiff】30天觀測期：即時 KPI 監控看板"

    embed = {
        "title": title,
        "description": (
            f"**🔒 範圍嚴格鎖定**：`23 款旗艦工具 / 36 組同類深度對決`\n"
            f"**⏱️ 觀測進度**：第 `{curr_day}` / `{target_days}` 天 (28~30 天決策周期)\n\n"
            f"### 🔻 最關鍵 5 大數字漏斗 (Funnel)\n{funnel_str}"
        ),
        "color": 0x10B981,  # Emerald
        "fields": [
            {
                "name": "🟢 Level 1: SEO 5 大指標 (Google 能見度)",
                "value": (
                    f"**1. Impressions (曝光數)**: `{format_number(total_imp)}`\n"
                    f"**2. Organic Clicks (搜尋點擊)**: `{format_number(total_clicks)}`\n"
                    f"**3. Search CTR (點閱率)**: `{ctr}`\n"
                    f"**4. Avg Position (平均排名)**: `{summary.get('avg_position', '—')}`\n"
                    f"**5. Top Queries (搜尋詞洞察)**:\n{queries_str}"
                ),
                "inline": False,
            },
            {
                "name": "🟡 Level 2: 商業 5 大指標 (訪客意圖與轉化)",
                "value": (
                    f"**6. Page Views (頁面瀏覽)**: `{format_number(summary.get('page_views', 0))}`\n"
                    f"**7. CTA Clicks (Affiliate 點擊)**: `{format_number(total_cta)}`\n"
                    f"**8. CTA CTR (點擊轉換率)**: `{cta_ctr}` *(目標 5%~15%)*\n"
                    f"**9. Affiliate Signups (免費註冊)**: `{format_number(total_signups)}`\n"
                    f"**10. Paid Conversions / Rev**: `${format_number(total_rev)}`"
                ),
                "inline": False,
            },
            {
                "name": "🏆 6 大分類訊號分布 (Category Rollup)",
                "value": categories_str,
                "inline": False,
            },
            {
                "name": "🎯 觀測期 4 大核心自問 (決策檢驗)",
                "value": (
                    "1. **Google 有沒有開始理解/曝光你的 comparison？** *(看總體 Impressions 趨勢)*\n"
                    "2. **哪些 comparison 有真實搜尋需求？** *(看 Top Queries 與 Clicks)*\n"
                    "3. **進站的人有沒有真的產生商業行為？** *(看 CTA Clicks & CTA CTR)*\n"
                    "4. **哪一類工具值得下一波擴張？** *(看 Category Rollup 的轉換訊號)*"
                ),
                "inline": False,
            },
            {
                "name": "⚡ 診斷指引 (Diagnostic Checklist)",
                "value": (
                    "• **有曝光但 0 點擊** ➔ 標題與 Description 吸引力不足？\n"
                    "• **有點擊但 0 CTA** ➔ 頁面沒有解決選擇問題？按鈕不明顯？\n"
                    "• **發現未預期搜尋詞** ➔ (如 `cursor vs copilot byok`) 提煉為下一波擴張依據！"
                ),
                "inline": False,
            },
            {
                "name": "🔗 捷徑工具箱",
                "value": (
                    "[📈 打開 Google Search Console](https://search.google.com/search-console) • "
                    "[🌐 訪問 StackDiff 官網](https://getstackdiff.com) • "
                    "[⚙️ GitHub Actions 巡檢](https://github.com/williamhsu0318-cyber/stack-diff/actions)"
                ),
                "inline": False,
            },
        ],
        "footer": {
            "text": "StackDiff 30-Day Observation Sentinel • 嚴格 Scope Freeze 不盲目擴充",
        },
        "timestamp": datetime.utcnow().isoformat(),
    }

    return {
        "content": "📊 **[StackDiff 觀測期]** 10 大核心 KPI 與決策漏斗更新已就緒：" if mode == "weekly" else "📊 **[StackDiff 即時巡檢]** 觀測期核心指標：",
        "embeds": [embed],
    }

def send_to_discord(payload: Dict[str, Any], webhook_url: Optional[str] = None) -> Tuple[bool, str]:
    """Sends payload to Discord Webhook via urllib."""
    url = webhook_url or get_env_var("DISCORD_WEBHOOK_URL")
    if not url:
        return False, "未設定 DISCORD_WEBHOOK_URL (請檢查 .env 或傳入 --webhook)"

    try:
        data_bytes = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        req = urllib.request.Request(
            url,
            data=data_bytes,
            headers={
                "Content-Type": "application/json",
                "User-Agent": "StackDiff-Sentinel/1.0"
            }
        )
        with urllib.request.urlopen(req, timeout=15) as resp:
            if resp.status in (200, 204):
                return True, "Discord 推播發送成功！"
            return False, f"Discord Webhook 回傳狀態碼: {resp.status}"
    except urllib.error.HTTPError as e:
        body = e.read().decode('utf-8', errors='ignore')[:200]
        return False, f"HTTPError {e.code}: {body}"
    except Exception as e:
        return False, f"連線異常: {str(e)}"

def main():
    parser = argparse.ArgumentParser(description="StackDiff Discord KPI Sentinel")
    parser.add_argument(
        "--mode",
        choices=["weekly", "summary", "test"],
        default="summary",
        help="推播模式: weekly (週報), summary (即時檢驗), test (連線測試)"
    )
    parser.add_argument(
        "--webhook",
        type=str,
        default=None,
        help="自訂 Discord Webhook 網址"
    )
    args = parser.parse_args()

    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 啟動 StackDiff Discord KPI 推播 (Mode: {args.mode})...")

    if args.mode == "test":
        test_payload = {
            "content": "🧪 **[StackDiff 測試推播]** Discord Webhook 連線測試成功！"
        }
        ok, msg = send_to_discord(test_payload, args.webhook)
    else:
        kpi_data = load_kpi_metrics()
        payload = build_discord_payload(kpi_data, mode=args.mode)
        ok, msg = send_to_discord(payload, args.webhook)

    if ok:
        print(f"✅ {msg}")
        sys.exit(0)
    else:
        print(f"❌ {msg}")
        sys.exit(1)

if __name__ == "__main__":
    main()
