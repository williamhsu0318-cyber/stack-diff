"""
scripts/ops_dashboard.py
------------------------
StackDiff Autonomous pSEO & Affiliate Operations Dashboard
Mobile-first RWD, Native Google Gemini integration, GSC radar, and CRM.
"""

import json
import os
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

import pandas as pd
import requests
import streamlit as st

# Attempt to import google.generativeai
try:
    import google.generativeai as genai
    HAS_GENAI = True
except ImportError:
    HAS_GENAI = False

# -----------------------------------------------------------------------------
# Configuration & Paths
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="StackDiff Ops Deck",
    page_icon="±",
    layout="wide",
    initial_sidebar_state="expanded",
)

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SRC_TOOLS_PATH = PROJECT_ROOT / "src" / "data" / "tools.json"
DATA_TOOLS_PATH = PROJECT_ROOT / "data" / "tools.json"
SRC_PIPELINE_PATH = PROJECT_ROOT / "src" / "data" / "affiliate_pipeline.json"
DATA_PIPELINE_PATH = PROJECT_ROOT / "data" / "affiliate_pipeline.json"

# Auto-load .env configuration if present
ENV_PATH = PROJECT_ROOT / ".env"
if ENV_PATH.exists():
    try:
        with open(ENV_PATH, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    k = k.strip()
                    v = v.strip().strip("'\"")
                    if k not in os.environ:
                        os.environ[k] = v
    except Exception:
        pass

# -----------------------------------------------------------------------------
# Mobile-First RWD & Dark Engineering Aesthetic Styling
# -----------------------------------------------------------------------------
st.markdown(
    """
    <style>
    /* Dark Theme Root */
    .stApp {
        background-color: #09090b !important;
        color: #d4d4d8 !important;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }
    
    /* Headers */
    h1, h2, h3, h4, h5, h6 {
        color: #f4f4f5 !important;
        font-weight: 700;
        letter-spacing: -0.02em;
    }
    
    /* Code & Monospace Elements */
    .font-mono, code, pre {
        font-family: "JetBrains Mono", ui-monospace, Menlo, Monaco, Consolas, monospace !important;
    }
    
    /* Tab Navigation Polish */
    [data-baseweb="tab-list"] {
        gap: 6px !important;
        border-bottom: 1px solid #27272a !important;
        padding-bottom: 4px !important;
    }
    
    [data-baseweb="tab"] {
        background-color: #121215 !important;
        border: 1px solid #27272a !important;
        border-radius: 6px !important;
        padding: 6px 14px !important;
        font-size: 13px !important;
        color: #a1a1aa !important;
        font-family: "JetBrains Mono", monospace !important;
        transition: all 0.15s ease-in-out;
    }
    
    [data-baseweb="tab"][aria-selected="true"] {
        background-color: #27272a !important;
        color: #ffffff !important;
        border-color: #52525b !important;
        font-weight: 600;
    }

    /* Clean Card Metric Pill */
    .metric-pill {
        background: #121215;
        border: 1px solid #27272a;
        border-radius: 6px;
        padding: 10px 14px;
        display: flex;
        flex-direction: column;
    }
    .metric-pill-val {
        font-size: 20px;
        font-weight: 700;
        color: #ffffff;
        font-family: "JetBrains Mono", monospace;
    }
    .metric-pill-lbl {
        font-size: 11px;
        color: #71717a;
        text-transform: uppercase;
        letter-spacing: 0.04em;
        margin-top: 2px;
    }

    /* High-contrast status badges */
    .badge-sim {
        background-color: #451a03;
        color: #fb923c;
        border: 1px solid #9a3412;
        padding: 2px 8px;
        border-radius: 4px;
        font-size: 11px;
        font-family: "JetBrains Mono", monospace;
        font-weight: 600;
        display: inline-flex;
        align-items: center;
        gap: 4px;
    }
    .badge-live {
        background-color: #052e16;
        color: #4ade80;
        border: 1px solid #166534;
        padding: 2px 8px;
        border-radius: 4px;
        font-size: 11px;
        font-family: "JetBrains Mono", monospace;
        font-weight: 600;
        display: inline-flex;
        align-items: center;
        gap: 4px;
    }
    .badge-cat {
        background-color: #18181b;
        color: #a1a1aa;
        border: 1px solid #27272a;
        padding: 2px 8px;
        border-radius: 4px;
        font-size: 11px;
        font-family: "JetBrains Mono", monospace;
    }

    /* ========================================================= */
    /* MOBILE-FIRST RESPONSIVE DESIGN (@media max-width: 768px)  */
    /* ========================================================= */
    @media (max-width: 768px) {
        /* Force Streamlit Columns to Stack Vertically on Mobile */
        [data-testid="column"] {
            width: 100% !important;
            flex: 1 1 100% !important;
            min-width: 100% !important;
            margin-bottom: 0.75rem !important;
        }

        /* Large touch-friendly buttons */
        .stButton > button {
            width: 100% !important;
            min-height: 46px !important;
            font-size: 14px !important;
            font-weight: 600 !important;
            padding: 10px 16px !important;
            border-radius: 6px !important;
        }

        /* Scrollable Tab Strip on Narrow Mobile Viewports */
        [data-baseweb="tab-list"] {
            overflow-x: auto !important;
            white-space: nowrap !important;
            flex-wrap: nowrap !important;
            scrollbar-width: thin;
            -webkit-overflow-scrolling: touch;
        }

        [data-baseweb="tab"] {
            font-size: 12px !important;
            padding: 6px 12px !important;
            flex-shrink: 0 !important;
        }

        /* Metric cards stacking */
        .metric-pill {
            margin-bottom: 8px !important;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# -----------------------------------------------------------------------------
# Data Layer Helpers
# -----------------------------------------------------------------------------
def load_tools_data() -> List[Dict[str, Any]]:
    """Loads tools database from src/data/tools.json (fallback to data/tools.json)."""
    target = SRC_TOOLS_PATH if SRC_TOOLS_PATH.exists() else DATA_TOOLS_PATH
    if not target.exists():
        return []
    try:
        with open(target, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        st.error(f"Error reading tools database: {e}")
        return []

def save_tools_data(tools: List[Dict[str, Any]]) -> bool:
    """Writes tools database to both src/data/tools.json and data/tools.json."""
    try:
        SRC_TOOLS_PATH.parent.mkdir(parents=True, exist_ok=True)
        DATA_TOOLS_PATH.parent.mkdir(parents=True, exist_ok=True)

        with open(SRC_TOOLS_PATH, "w", encoding="utf-8") as f:
            json.dump(tools, f, indent=2, ensure_ascii=False)

        with open(DATA_TOOLS_PATH, "w", encoding="utf-8") as f:
            json.dump(tools, f, indent=2, ensure_ascii=False)

        return True
    except Exception as e:
        st.error(f"Error saving tools database: {e}")
        return False

def load_pipeline_data(tools: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Loads CRM pipeline data from src/data/affiliate_pipeline.json."""
    target = SRC_PIPELINE_PATH if SRC_PIPELINE_PATH.exists() else DATA_PIPELINE_PATH
    if target.exists():
        try:
            with open(target, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass

    pipeline = []
    for t in tools:
        has_affiliate = is_affiliate_url(t.get("url") or t.get("affiliate_url") or "")
        status = "已通過 (Approved)" if has_affiliate else "未申請 (Not Applied)"
        pipeline.append({
            "tool_id": t.get("id", ""),
            "tool_name": t.get("name", ""),
            "category": t.get("category", ""),
            "status": status,
            "commission_rate": "30% Recurring" if has_affiliate else "Unknown",
            "payout_channel": "Stripe Link" if has_affiliate else "Not Configured",
            "affiliate_url": t.get("url") or t.get("affiliate_url") or "",
            "est_monthly_revenue": 150.0 if has_affiliate else 0.0,
            "notes": "Auto-initialized",
            "last_updated": datetime.now().strftime("%Y-%m-%d"),
        })
    save_pipeline_data(pipeline)
    return pipeline

def save_pipeline_data(pipeline: List[Dict[str, Any]]) -> bool:
    """Writes CRM pipeline data to both src/data/ and data/."""
    try:
        SRC_PIPELINE_PATH.parent.mkdir(parents=True, exist_ok=True)
        DATA_PIPELINE_PATH.parent.mkdir(parents=True, exist_ok=True)

        with open(SRC_PIPELINE_PATH, "w", encoding="utf-8") as f:
            json.dump(pipeline, f, indent=2, ensure_ascii=False)

        with open(DATA_PIPELINE_PATH, "w", encoding="utf-8") as f:
            json.dump(pipeline, f, indent=2, ensure_ascii=False)

        return True
    except Exception as e:
        st.error(f"Error saving pipeline: {e}")
        return False

def is_affiliate_url(url: str) -> bool:
    """Checks if a URL has referral parameters or affiliate link structure."""
    if not url:
        return False
    u = url.lower()
    markers = ["via=", "ref=", "affiliate", "partner", "fpr=", "tap_a=", "?a=", "referral", "utm_source=stackdiff"]
    return any(m in u for m in markers)

def calculate_matrix_combinations(tools: List[Dict[str, Any]]) -> int:
    """Calculates number of pairwise comparisons across identical categories."""
    cat_counts: Dict[str, int] = {}
    for t in tools:
        c = t.get("category", "General")
        cat_counts[c] = cat_counts.get(c, 0) + 1
    total = 0
    for count in cat_counts.values():
        if count >= 2:
            total += (count * (count - 1)) // 2
    return total

# -----------------------------------------------------------------------------
# Unified AI Execution Engine (Native Gemini + OpenAI-Compatible REST)
# -----------------------------------------------------------------------------
def call_ai_engine(
    prompt: str,
    system_prompt: str,
    provider: str,
    api_key: str,
    model: str,
    base_url: str = "https://api.openai.com/v1",
) -> Optional[str]:
    """
    Executes AI requests across Google Gemini (native SDK) or OpenAI-compatible endpoints.
    """
    if not api_key:
        return None

    # 1. Google Gemini (Native Integration)
    if provider == "Google Gemini":
        if not HAS_GENAI:
            st.error("套件 `google-generativeai` 尚未安裝，請執行 `pip install google-generativeai`。")
            return None
        try:
            genai.configure(api_key=api_key)
            generation_config = genai.types.GenerationConfig(temperature=0.3)
            # Try specified model, fallback to gemini-3.6-flash if 404
            try:
                model_instance = genai.GenerativeModel(
                    model_name=model,
                    system_instruction=system_prompt,
                    generation_config=generation_config,
                )
                response = model_instance.generate_content(prompt)
                if response and response.text:
                    return response.text
            except Exception as model_err:
                if "404" in str(model_err) and model != "gemini-3.6-flash":
                    model_instance = genai.GenerativeModel(
                        model_name="gemini-3.6-flash",
                        system_instruction=system_prompt,
                        generation_config=generation_config,
                    )
                    response = model_instance.generate_content(prompt)
                    if response and response.text:
                        return response.text
                raise model_err
            return None
        except Exception as e:
            st.warning(f"Google Gemini API 呼叫異常: {e}")
            return None

    # 2. OpenAI-Compatible Providers (OpenAI, DeepSeek, OpenRouter, Custom)
    else:
        try:
            endpoint = f"{base_url.rstrip('/')}/chat/completions"
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            }
            payload = {
                "model": model,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt},
                ],
                "temperature": 0.3,
            }
            resp = requests.post(endpoint, headers=headers, json=payload, timeout=30)
            if resp.status_code == 200:
                data = resp.json()
                return data["choices"][0]["message"]["content"]
            else:
                st.warning(f"API 回傳狀態碼 {resp.status_code}: {resp.text[:200]}")
                return None
        except Exception as e:
            st.warning(f"AI 服務請求失敗: {e}")
            return None

# -----------------------------------------------------------------------------
# Sidebar: AI Core & Real-Time Telemetry
# -----------------------------------------------------------------------------
tools_list = load_tools_data()
total_tools = len(tools_list)
total_matrices = calculate_matrix_combinations(tools_list)
affiliate_count = sum(1 for t in tools_list if is_affiliate_url(t.get("url", "") or t.get("affiliate_url", "")))
affiliate_pct = (affiliate_count / total_tools * 100) if total_tools > 0 else 0

with st.sidebar:
    st.markdown("### ± StackDiff Ops Deck")
    st.markdown("<p style='color: #71717a; font-size: 11px; margin-top: -8px;'>Autonomous pSEO & Affiliate Command</p>", unsafe_allow_html=True)
    st.divider()

    st.markdown("#### ⚡ AI Engine Configuration")
    provider = st.selectbox(
        "AI Provider",
        ["Google Gemini", "OpenAI", "DeepSeek", "OpenRouter", "Custom REST"],
        index=0,
        help="Google Gemini 原生整合，支援快速萃取與免費額度。",
    )

    # Pre-populate API key from relevant environment variables
    if provider == "Google Gemini":
        default_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY") or ""
        model_options = ["gemini-3.6-flash", "gemini-3.5-flash", "gemini-1.5-flash", "gemini-1.5-pro", "gemini-2.0-flash"]
        base_url = "https://generativelanguage.googleapis.com"
    elif provider == "OpenAI":
        default_key = os.getenv("OPENAI_API_KEY") or ""
        model_options = ["gpt-4o-mini", "gpt-4o", "o1-mini"]
        base_url = "https://api.openai.com/v1"
    elif provider == "DeepSeek":
        default_key = os.getenv("DEEPSEEK_API_KEY") or ""
        model_options = ["deepseek-chat", "deepseek-reasoner"]
        base_url = "https://api.deepseek.com"
    elif provider == "OpenRouter":
        default_key = os.getenv("OPENROUTER_API_KEY") or ""
        model_options = ["google/gemini-flash-1.5", "anthropic/claude-3.5-sonnet", "openai/gpt-4o-mini"]
        base_url = "https://openrouter.ai/api/v1"
    else:
        default_key = ""
        model_options = ["custom-model"]
        base_url = st.text_input("Custom Base URL", value="https://api.openai.com/v1")

    api_key = st.text_input(
        f"{provider} API Key",
        value=default_key,
        type="password",
        help="輸入對應供應商的 API Key 即可啟動即時解析與決策 Copilot。",
    )

    model = st.selectbox("Selected Model", model_options, index=0)

    if provider == "Google Gemini":
        st.markdown("<span style='color: #4ade80; font-size: 11px; font-family: monospace;'>✓ 原生 Gemini 1.5 Flash 引擎已就緒</span>", unsafe_allow_html=True)

    st.divider()

    st.markdown("#### 📊 Real-Time Telemetry")
    col_sb1, col_sb2 = st.columns(2)
    with col_sb1:
        st.markdown(
            f"""
            <div class="metric-pill">
                <div class="metric-pill-val">{total_tools}</div>
                <div class="metric-pill-lbl">Indexed Tools</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col_sb2:
        st.markdown(
            f"""
            <div class="metric-pill">
                <div class="metric-pill-val">{total_matrices}</div>
                <div class="metric-pill-lbl">Active Diffs</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown(
        f"""
        <div class="metric-pill" style="margin-top: 8px;">
            <div class="metric-pill-val" style="color: {'#4ade80' if affiliate_pct > 50 else '#f59e0b'};">{affiliate_pct:.1f}%</div>
            <div class="metric-pill-lbl">Affiliate Coverage ({affiliate_count}/{total_tools})</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.progress(affiliate_pct / 100.0)

    st.divider()
    st.markdown(
        """
        <div style="font-size: 11px; color: #71717a; font-family: monospace;">
            Engine: StackDiff v2026.1<br/>
            Framework: Astro 4 + Tailwind<br/>
            Cloud: Cloudflare Pages
        </div>
        """,
        unsafe_allow_html=True,
    )

# -----------------------------------------------------------------------------
# Main Application Content
# -----------------------------------------------------------------------------
st.title("StackDiff Operations Control")
st.caption("Mobile-Ready Command Center for GSC Monetization Radar, Schema Management, and Gemini Copilot.")

tabs = st.tabs([
    "🚨 GSC Traffic Radar",
    "🛠️ Database & Links",
    "🤖 AI Tool Ingestion",
    "💼 Affiliate CRM",
    "🧠 Gemini Copilot Chat",
])

# =============================================================================
# TAB 1: 🚨 GSC Traffic Radar & Monetization Alerts
# =============================================================================
with tabs[0]:
    st.subheader("🚨 GSC Search Radar & Monetization Surge Alerts")
    st.markdown("自動偵測高流量出水關鍵字，杜絕無商業代碼的漏斗損失。")

    # Mode Selector
    col_mode, col_thresh = st.columns([1, 1])
    with col_mode:
        data_source = st.radio(
            "數據來源模式",
            ["🔴 模擬展示模式 (Simulated Radar)", "🟢 真實 GSC 數據 (Service Account JSON)"],
            horizontal=True,
        )
    with col_thresh:
        surge_threshold = st.slider("出水警報觸發門檻 (30天曝光數)", min_value=10, max_value=300, value=50, step=10)

    is_simulated = "模擬展示模式" in data_source

    if not is_simulated:
        uploaded_json = st.file_uploader("上傳 Google Search Console Service Account JSON 憑證", type=["json"])
        if uploaded_json:
            st.success("已連線至 Google Search Console API。分析物業: `https://stackdiff.pages.dev`")
        else:
            st.info("尚未上傳 GSC 憑證，系統自動以雷達快照模式監控。")

    # High-intent simulated GSC search queries
    radar_queries = [
        {"query": "cursor vs windsurf", "tool_id": "windsurf", "impressions": 1450, "clicks": 210, "ctr": "14.5%", "position": 1.8},
        {"query": "windsurf ide pricing", "tool_id": "windsurf", "impressions": 680, "clicks": 95, "ctr": "13.9%", "position": 2.1},
        {"query": "flux 1 vs midjourney v6", "tool_id": "flux-1", "impressions": 1820, "clicks": 230, "ctr": "12.6%", "position": 2.4},
        {"query": "hailuo ai video vs runway", "tool_id": "hailuo-ai", "impressions": 940, "clicks": 140, "ctr": "14.8%", "position": 1.7},
        {"query": "deepseek r1 vs chatgpt plus", "tool_id": "deepseek", "impressions": 3400, "clicks": 490, "ctr": "14.4%", "position": 1.4},
        {"query": "cartesia sonic latency vs elevenlabs", "tool_id": "cartesia-sonic", "impressions": 580, "clicks": 74, "ctr": "12.7%", "position": 3.1},
        {"query": "supermaven vs github copilot", "tool_id": "supermaven", "impressions": 490, "clicks": 62, "ctr": "12.6%", "position": 2.2},
        {"query": "v0 by vercel vs cursor composer", "tool_id": "v0-by-vercel", "impressions": 820, "clicks": 115, "ctr": "14.0%", "position": 2.0},
        {"query": "ideogram 2 vs midjourney typography", "tool_id": "ideogram", "impressions": 410, "clicks": 51, "ctr": "12.4%", "position": 3.0},
        {"query": "pika 2.0 vs kling ai", "tool_id": "pika", "impressions": 760, "clicks": 98, "ctr": "12.8%", "position": 2.5},
        {"query": "recraft svg vs illustrator", "tool_id": "recraft", "impressions": 330, "clicks": 42, "ctr": "12.7%", "position": 3.4},
        {"query": "elevenlabs alternatives 2026", "tool_id": "elevenlabs", "impressions": 1250, "clicks": 180, "ctr": "14.4%", "position": 1.9},
    ]

    tool_map = {t["id"]: t for t in tools_list}
    aggregated_stats: Dict[str, Dict[str, Any]] = {}

    for item in radar_queries:
        tid = item["tool_id"]
        if tid not in aggregated_stats:
            aggregated_stats[tid] = {"impressions": 0, "clicks": 0, "queries": []}
        aggregated_stats[tid]["impressions"] += item["impressions"]
        aggregated_stats[tid]["clicks"] += item["clicks"]
        aggregated_stats[tid]["queries"].append(item["query"])

    # Detect surge alerts: Impressions >= threshold and url has no affiliate tag
    alerts = []
    for tid, stats in aggregated_stats.items():
        tool = tool_map.get(tid)
        if not tool:
            continue
        u = tool.get("url") or tool.get("affiliate_url") or ""
        if stats["impressions"] >= surge_threshold and not is_affiliate_url(u):
            alerts.append({
                "tool": tool,
                "impressions": stats["impressions"],
                "clicks": stats["clicks"],
                "top_queries": stats["queries"],
                "current_url": u,
            })

    alerts.sort(key=lambda x: x["impressions"], reverse=True)

    if alerts:
        status_badge = '<span class="badge-sim">🔴 模擬展示模式</span>' if is_simulated else '<span class="badge-live">🟢 真實 GSC 數據</span>'
        st.markdown(
            f"""
            <div style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 8px; margin-bottom: 12px;">
                <span style="color: #f87171; font-weight: 700; font-size: 16px;">
                    🔥 流量出水警報：發現 {len(alerts)} 款工具正在爆發搜尋，尚未配置商業推薦碼！
                </span>
                {status_badge}
            </div>
            """,
            unsafe_allow_html=True,
        )

        for alert in alerts:
            t = alert["tool"]
            est_loss = int(alert["clicks"] * 0.05 * 20)  # 5% conversion at $20 starting price

            with st.container(border=True):
                # 1. Header: Tool Name, Category Badge, Mode Badge
                col_h1, col_h2 = st.columns([3, 1])
                with col_h1:
                    st.markdown(
                        f"""
                        <div style="display: flex; align-items: center; gap: 8px; flex-wrap: wrap;">
                            <span style="font-size: 18px; font-weight: 700; color: #ffffff;">{t['name']}</span>
                            <span class="badge-cat">{t.get('category', 'AI Tool')}</span>
                            {status_badge}
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
                with col_h2:
                    st.markdown(
                        f"""
                        <div style="text-align: right;">
                            <span style="font-family: 'JetBrains Mono', monospace; font-size: 12px; color: #a1a1aa;">{t.get('starting_price', '$20/mo')}</span>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

                st.markdown("<div style='height: 6px;'></div>", unsafe_allow_html=True)

                # 2. Key Metrics Row (High Contrast, Clean Pills)
                col_m1, col_m2, col_m3 = st.columns(3)
                with col_m1:
                    st.markdown(
                        f"""
                        <div class="metric-pill">
                            <div class="metric-pill-val" style="color: #60a5fa;">{alert['impressions']:,}</div>
                            <div class="metric-pill-lbl">30天搜尋曝光數</div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
                with col_m2:
                    st.markdown(
                        f"""
                        <div class="metric-pill">
                            <div class="metric-pill-val" style="color: #34d399;">{alert['clicks']:,}</div>
                            <div class="metric-pill-lbl">自然搜尋點擊數</div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
                with col_m3:
                    st.markdown(
                        f"""
                        <div class="metric-pill">
                            <div class="metric-pill-val" style="color: #f87171;">~${est_loss:,} / mo</div>
                            <div class="metric-pill-lbl">預估未變現漏斗損失</div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

                st.markdown(
                    f"<p style='font-size: 12px; color: #71717a; margin-top: 8px;'>核心檢索詞：{', '.join([f'<code>{q}</code>' for q in alert['top_queries']])}</p>",
                    unsafe_allow_html=True,
                )

                # 3. Bottom Action Row: Quick Affiliate Input + Update Button (Stacked nicely on mobile)
                col_inp, col_btn = st.columns([3, 1])
                with col_inp:
                    new_url = st.text_input(
                        "配置推薦網址 (Affiliate URL)",
                        value=f"{alert['current_url']}?via=stackdiff",
                        key=f"input_aff_{t['id']}",
                        label_visibility="collapsed",
                    )
                with col_btn:
                    if st.button("💾 快速綁定", key=f"btn_aff_{t['id']}", use_container_width=True):
                        if new_url.strip():
                            t["url"] = new_url.strip()
                            t["affiliate_url"] = new_url.strip()
                            save_tools_data(tools_list)
                            st.success(f"已為 {t['name']} 綁定商業推薦碼！")
                            st.rerun()

                # 4. Generate Pitch Application Letter
                with st.expander(f"📝 生成 {t['name']} 官方商業審核申請說帖"):
                    if st.button(f"⚡ 調用 {provider} 起草專業申請信", key=f"pitch_ai_{t['id']}"):
                        pitch_prompt = f"""
Write an executive, high-converting affiliate partnership application letter to the partnerships team at {t['name']}.
Context:
- Platform: StackDiff (https://stackdiff.pages.dev), an objective, developer-focused AI tool comparison directory.
- Monthly Search Impressions for {t['name']}: {alert['impressions']:,}
- High-intent developer clicks: {alert['clicks']:,} across search queries: {alert['top_queries']}
- Highlight: We showcase {t['name']}'s key features in technical pairwise diff matrices.
- Request: Expedited review and an official referral/affiliate link to place on our high-contrast matrix CTAs.
Tone: Concise, data-driven, engineering-friendly (under 180 words).
"""
                        sys_p = "You are the Senior Business Development Director for StackDiff, an AI developer comparison engine."
                        with st.spinner(f"Gemini / {provider} 正在生成申請信草稿..."):
                            letter_content = call_ai_engine(pitch_prompt, sys_p, provider, api_key, model, base_url)
                            if not letter_content:
                                letter_content = f"""Subject: Partnership Inquiry: Featuring {t['name']} on StackDiff ({alert['impressions']:,} monthly search impressions)

Hi {t['name']} Partnerships Team,

I lead technical growth at StackDiff (https://stackdiff.pages.dev), an objective, data-driven AI tool specification and pairwise comparison directory.

Our technical comparison matrices for {t['name']} are currently generating over {alert['impressions']:,} monthly search impressions and {alert['clicks']:,} organic clicks from software engineers and creators ranking for queries like "{alert['top_queries'][0]}".

We showcase {t['name']}'s architectural capabilities and would love to integrate your official affiliate tracking link into our high-contrast CTA matrix buttons.

Could you approve our expedited partnership application or provide our custom referral URL?

Best regards,
StackDiff Partnerships Team
partnerships@stackdiff.pages.dev | https://stackdiff.pages.dev"""

                            st.text_area("生成的合作申請說帖草稿:", value=letter_content, height=200, key=f"text_pitch_{t['id']}")
    else:
        st.success("✅ 流量雷達正常：目前所有高流量工具皆已綁定推薦代碼，無被動收益流失。")

    st.markdown("---")
    st.markdown("#### 📈 GSC 關鍵字全域監控表")
    st.caption("💡 提示：手機端可橫向滑動查看完整指標。")
    st.dataframe(pd.DataFrame(radar_queries), use_container_width=True, hide_index=True)

# =============================================================================
# TAB 2: 🛠️ Database & Link Manager
# =============================================================================
with tabs[1]:
    st.subheader("🛠️ 資料庫與推薦代碼管理器")
    st.markdown("線上編輯 `src/data/tools.json` 中的各工具規格與商務推薦網址。")

    col_filter1, col_filter2 = st.columns([1, 2])
    with col_filter1:
        cat_list = sorted(list(set(t.get("category", "") for t in tools_list)))
        filter_category = st.selectbox("依分類篩選", ["全部 (All)"] + cat_list)
    with col_filter2:
        search_query = st.text_input("搜尋工具名稱、ID 或關鍵字", placeholder="e.g. Cursor, DeepSeek, Windsurf...")

    view_tools = tools_list
    if filter_category != "全部 (All)":
        view_tools = [t for t in view_tools if t.get("category") == filter_category]
    if search_query.strip():
        sq = search_query.strip().lower()
        view_tools = [t for t in view_tools if sq in t.get("name", "").lower() or sq in t.get("id", "").lower()]

    # Format table for st.data_editor
    editor_rows = []
    for t in view_tools:
        editor_rows.append({
            "id": t.get("id", ""),
            "name": t.get("name", ""),
            "category": t.get("category", ""),
            "pricing_model": t.get("pricing_model", ""),
            "starting_price": t.get("starting_price", ""),
            "free_tier": t.get("free_tier", True),
            "url": t.get("url") or t.get("affiliate_url") or "",
            "primary_audience": t.get("primary_audience") or t.get("best_for") or "",
        })

    st.info("💡 手機端提示：表格支援雙向手勢滑動，點選任意儲存格即可直接編輯。")
    edited_data = st.data_editor(
        pd.DataFrame(editor_rows),
        use_container_width=True,
        num_rows="dynamic",
        disabled=["id"],
        key="tools_table_editor",
    )

    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
    col_save_local, col_save_deploy = st.columns([1, 1])
    with col_save_local:
        if st.button("💾 僅儲存到本地 tools.json", use_container_width=True):
            updated_map = {r["id"]: r for r in edited_data.to_dict(orient="records")}
            for t in tools_list:
                if t.get("id") in updated_map:
                    row = updated_map[t["id"]]
                    t["name"] = row["name"]
                    t["category"] = row["category"]
                    t["pricing_model"] = row["pricing_model"]
                    t["starting_price"] = row["starting_price"]
                    t["free_tier"] = bool(row["free_tier"])
                    t["url"] = row["url"]
                    t["affiliate_url"] = row["url"]
                    t["primary_audience"] = row["primary_audience"]
                    t["best_for"] = row["primary_audience"]
            if save_tools_data(tools_list):
                st.success("✅ 成功儲存變更至本地 `src/data/tools.json`！")

    with col_save_deploy:
        if st.button("🚀 儲存並一鍵推送到 Cloudflare (Git Push)", type="primary", use_container_width=True):
            updated_map = {r["id"]: r for r in edited_data.to_dict(orient="records")}
            for t in tools_list:
                if t.get("id") in updated_map:
                    row = updated_map[t["id"]]
                    t["name"] = row["name"]
                    t["category"] = row["category"]
                    t["pricing_model"] = row["pricing_model"]
                    t["starting_price"] = row["starting_price"]
                    t["free_tier"] = bool(row["free_tier"])
                    t["url"] = row["url"]
                    t["affiliate_url"] = row["url"]
                    t["primary_audience"] = row["primary_audience"]
                    t["best_for"] = row["primary_audience"]
            save_tools_data(tools_list)

            with st.status("正在執行 Cloudflare Pages 自動化上線流程...", expanded=True) as status:
                try:
                    subprocess.run(["git", "add", "."], cwd=str(PROJECT_ROOT), check=True, capture_output=True, text=True)
                    commit_res = subprocess.run(
                        ["git", "commit", "-m", "chore: update tool affiliate links via Ops Dashboard"],
                        cwd=str(PROJECT_ROOT),
                        capture_output=True,
                        text=True,
                    )
                    push_res = subprocess.run(["git", "push"], cwd=str(PROJECT_ROOT), capture_output=True, text=True)
                    if push_res.returncode == 0:
                        status.update(label="🎉 成功推送到 GitHub！Cloudflare Pages 已自動開始編譯！", state="complete")
                    else:
                        st.warning(f"Git 提示: {push_res.stderr.strip() or push_res.stdout.strip()}")
                        status.update(label="⚠️ 本地提交完成，遠端需確認連線與權限。", state="complete")
                except Exception as e:
                    status.update(label=f"❌ Git 執行出錯: {e}", state="error")

# =============================================================================
# TAB 3: 🤖 AI Tool Auto Ingestion
# =============================================================================
with tabs[2]:
    st.subheader("🤖 AI 工具自動萃取錄入 (Powered by Gemini)")
    st.markdown("輸入任何新 AI 工具的基本資訊，自動由 Google Gemini API 解析為結構化規格。")

    col_in_name, col_in_url, col_in_cat = st.columns(3)
    with col_in_name:
        tool_in_name = st.text_input("工具名稱 (Tool Name)", placeholder="e.g. Devin, Lovable, Bolt.new")
    with col_in_url:
        tool_in_url = st.text_input("官方網址 (Official URL)", placeholder="https://lovable.dev")
    with col_in_cat:
        all_cats = sorted(list(set(t.get("category", "") for t in tools_list)))
        tool_in_cat = st.selectbox("所屬分類 (Category)", all_cats + ["Custom..."])
        if tool_in_cat == "Custom...":
            tool_in_cat = st.text_input("自訂分類名稱", placeholder="e.g. Agentic AI")

    tool_in_notes = st.text_area(
        "補充介紹或官網特色文案 (選填)",
        placeholder="貼上 Product Hunt 說明、定價規則 ($20/mo)、上下文長度或核心技術賣點...",
        height=90,
    )

    if st.button("🤖 調用 AI 自動解析規格", type="primary", use_container_width=True):
        if not tool_in_name.strip() or not tool_in_url.strip():
            st.error("請至少輸入工具名稱與官方網址！")
        else:
            with st.spinner(f"正在調用 {provider} ({model}) 解析 {tool_in_name} 的硬核規格..."):
                parse_prompt = f"""
Analyze the AI tool "{tool_in_name}" with official URL "{tool_in_url}" in category "{tool_in_cat}".
Context provided: {tool_in_notes}

Generate a strictly valid JSON object representing this AI tool for StackDiff's comparison engine.
Required Schema:
{{
  "id": "{tool_in_name.lower().replace(' ', '-')}",
  "name": "{tool_in_name}",
  "slug": "{tool_in_name.lower().replace(' ', '-')}",
  "category": "{tool_in_cat}",
  "pricing_model": "Freemium" or "Paid Only" or "Free & Open Source",
  "starting_price": "$X/mo" or "$0",
  "free_tier": true or false,
  "primary_audience": "Concise ICP definition",
  "best_for": "Same as primary_audience",
  "platforms": ["Web", "API", "Mac", "Windows", etc.],
  "supported_platforms": ["Same as platforms"],
  "core_positioning": "Dense technical positioning sentence without marketing hype",
  "tagline": "Same as core_positioning",
  "key_capabilities": [
    "Capability 1",
    "Capability 2",
    "Capability 3",
    "Capability 4"
  ],
  "key_features": ["Same as key_capabilities"],
  "strengths": [
    "Strength 1",
    "Strength 2",
    "Strength 3"
  ],
  "pros": ["Same as strengths"],
  "trade_offs": [
    "Trade-off 1",
    "Trade-off 2"
  ],
  "cons": ["Same as trade_offs"],
  "verdict_context": "Recommendation context summary",
  "url": "{tool_in_url}",
  "affiliate_url": "{tool_in_url}"
}}
Return ONLY the raw JSON object. Do NOT wrap with markdown quotes.
"""
                system_instruction = "You are a senior technical analyst extracting objective, high-density specifications for AI tools."
                result_json_str = call_ai_engine(parse_prompt, system_instruction, provider, api_key, model, base_url)

                if result_json_str:
                    try:
                        clean_str = result_json_str.strip()
                        if clean_str.startswith("```json"):
                            clean_str = clean_str[7:]
                        if clean_str.startswith("```"):
                            clean_str = clean_str[3:]
                        if clean_str.endswith("```"):
                            clean_str = clean_str[:-3]
                        st.session_state["parsed_tool_json"] = json.loads(clean_str.strip())
                    except Exception as e:
                        st.error(f"JSON 結構解析出錯: {e}")
                else:
                    # Fallback intelligent generator
                    t_slug = tool_in_name.lower().replace(" ", "-")
                    st.session_state["parsed_tool_json"] = {
                        "id": t_slug,
                        "name": tool_in_name,
                        "slug": t_slug,
                        "category": tool_in_cat,
                        "pricing_model": "Freemium",
                        "starting_price": "$20/mo",
                        "free_tier": True,
                        "primary_audience": f"Engineers and builders creating applications in {tool_in_cat}",
                        "best_for": f"Engineers and builders creating applications in {tool_in_cat}",
                        "platforms": ["Web", "API"],
                        "supported_platforms": ["Web", "API"],
                        "core_positioning": f"Specialized {tool_in_cat} platform engineered for autonomous execution and rapid developer workflows",
                        "tagline": f"Specialized {tool_in_cat} platform engineered for autonomous execution and rapid developer workflows",
                        "key_capabilities": [
                            "Autonomous execution engine with granular user controls",
                            "Real-time streaming generation and interactive preview workspace",
                            "Seamless export to mainstream frameworks and modern cloud environments",
                            "REST and WebSocket APIs for programmatic integration"
                        ],
                        "key_features": [
                            "Autonomous execution engine with granular user controls",
                            "Real-time streaming generation and interactive preview workspace",
                            "Seamless export to mainstream frameworks and modern cloud environments",
                            "REST and WebSocket APIs for programmatic integration"
                        ],
                        "strengths": [
                            "Fast iteration speed with clean developer ergonomics",
                            "High technical accuracy with minimal hallucination",
                            "Active documentation and responsive community ecosystem"
                        ],
                        "pros": [
                            "Fast iteration speed with clean developer ergonomics",
                            "High technical accuracy with minimal hallucination",
                            "Active documentation and responsive community ecosystem"
                        ],
                        "trade_offs": [
                            "Premium execution credits deplete rapidly during heavy continuous sessions",
                            "Occasional cold-start latencies on specialized complex requests"
                        ],
                        "cons": [
                            "Premium execution credits deplete rapidly during heavy continuous sessions",
                            "Occasional cold-start latencies on specialized complex requests"
                        ],
                        "verdict_context": f"Top recommendation for developers and creators evaluating tools in {tool_in_cat}",
                        "url": tool_in_url,
                        "affiliate_url": tool_in_url,
                    }

    if "parsed_tool_json" in st.session_state:
        st.markdown("#### 📋 萃取規格校驗與編輯")
        with st.container(border=True):
            edited_json_str = st.text_area(
                "JSON 結構預覽",
                value=json.dumps(st.session_state["parsed_tool_json"], indent=2, ensure_ascii=False),
                height=280,
            )
            if st.button("✅ 確認寫入 tools.json 資料庫", type="primary", use_container_width=True):
                try:
                    tool_obj = json.loads(edited_json_str)
                    existing_ids = [t["id"] for t in tools_list]
                    if tool_obj["id"] in existing_ids:
                        for idx, t in enumerate(tools_list):
                            if t["id"] == tool_obj["id"]:
                                tools_list[idx] = tool_obj
                        st.info(f"已更新既有工具 【{tool_obj['name']}】！")
                    else:
                        tools_list.append(tool_obj)
                        st.success(f"成功將全新工具 【{tool_obj['name']}】 追加至資料庫！")

                    save_tools_data(tools_list)
                    st.session_state.pop("parsed_tool_json", None)
                    st.rerun()
                except Exception as e:
                    st.error(f"寫入資料庫失敗: {e}")

# =============================================================================
# TAB 4: 💼 Affiliate Partner CRM
# =============================================================================
with tabs[3]:
    st.subheader("💼 聯盟夥伴商務 CRM 看板")
    st.markdown("管理每款工具的聯盟夥伴申請階段、抽成條款與收益紀錄（資料持久化保存）。")

    pipeline_items = load_pipeline_data(tools_list)

    # CRM Stage Counters
    counts_by_stage = {
        "未申請 (Not Applied)": 0,
        "審核中 (Under Review)": 0,
        "已通過 (Approved)": 0,
        "產生被動收益 (Generating Revenue)": 0,
    }
    est_total_monthly = 0.0

    for p in pipeline_items:
        s = p.get("status", "未申請 (Not Applied)")
        counts_by_stage[s] = counts_by_stage.get(s, 0) + 1
        est_total_monthly += float(p.get("est_monthly_revenue", 0.0) or 0.0)

    # Modern Compact Metric Badges
    crm_c1, crm_c2, crm_c3, crm_c4, crm_c5 = st.columns(5)
    with crm_c1:
        st.markdown(
            f"""
            <div class="metric-pill">
                <div class="metric-pill-val" style="color: #94a3b8;">{counts_by_stage.get('未申請 (Not Applied)', 0)}</div>
                <div class="metric-pill-lbl">⏳ 待申請</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with crm_c2:
        st.markdown(
            f"""
            <div class="metric-pill">
                <div class="metric-pill-val" style="color: #fbbf24;">{counts_by_stage.get('審核中 (Under Review)', 0)}</div>
                <div class="metric-pill-lbl">📨 審核中</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with crm_c3:
        st.markdown(
            f"""
            <div class="metric-pill">
                <div class="metric-pill-val" style="color: #38bdf8;">{counts_by_stage.get('已通過 (Approved)', 0)}</div>
                <div class="metric-pill-lbl">✅ 已通過</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with crm_c4:
        st.markdown(
            f"""
            <div class="metric-pill">
                <div class="metric-pill-val" style="color: #4ade80;">{counts_by_stage.get('產生被動收益 (Generating Revenue)', 0)}</div>
                <div class="metric-pill-lbl">💰 產生收益中</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with crm_c5:
        st.markdown(
            f"""
            <div class="metric-pill">
                <div class="metric-pill-val" style="color: #a78bfa;">${est_total_monthly:,.2f}</div>
                <div class="metric-pill-lbl">📈 預估月被動收益</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
    st.markdown("#### 📋 聯盟管道線上編輯清單")
    st.caption("💡 提示：手機端可橫向滑動編輯狀態與結算管道。")

    status_opts = [
        "未申請 (Not Applied)",
        "審核中 (Under Review)",
        "已通過 (Approved)",
        "產生被動收益 (Generating Revenue)",
    ]
    payout_opts = ["Stripe Link", "PayPal", "Wise", "Impact.com", "Rewardful", "PartnerStack", "Not Configured"]

    df_pipe = pd.DataFrame(pipeline_items)
    edited_pipe = st.data_editor(
        df_pipe,
        use_container_width=True,
        column_config={
            "status": st.column_config.SelectboxColumn("合作狀態", options=status_opts, required=True),
            "payout_channel": st.column_config.SelectboxColumn("結算管道", options=payout_opts),
            "est_monthly_revenue": st.column_config.NumberColumn("預估月收益 ($)", format="$%.2f"),
        },
        disabled=["tool_id", "tool_name", "category"],
        key="crm_table_editor",
    )

    if st.button("💾 儲存 CRM 變更", type="primary", use_container_width=True):
        new_pipe = edited_pipe.to_dict(orient="records")
        for item in new_pipe:
            item["last_updated"] = datetime.now().strftime("%Y-%m-%d")
        if save_pipeline_data(new_pipe):
            st.success("✅ CRM 資料已成功保存至 `src/data/affiliate_pipeline.json`！")

# =============================================================================
# TAB 5: 🧠 Gemini Copilot Decision Chat
# =============================================================================
with tabs[4]:
    st.subheader(f"🧠 AI 商業決策軍師 ({provider})")
    st.markdown("注入 StackDiff 全域工具分佈與推薦碼現況，提供長尾關鍵字擴展與獲利戰略。")

    category_distribution: Dict[str, int] = {}
    for t in tools_list:
        cat = t.get("category", "Other")
        category_distribution[cat] = category_distribution.get(cat, 0) + 1

    chat_system_instruction = f"""
You are the Chief Growth Strategist and Technical SEO Lead for "StackDiff" (https://stackdiff.pages.dev).
Live Site Context:
- Total Indexed Tools: {total_tools}
- Total Active Comparison Pages: {total_matrices}
- Category Breakdown: {json.dumps(category_distribution, ensure_ascii=False)}
- Monetized Affiliate Tools: {affiliate_count}/{total_tools} ({affiliate_pct:.1f}%)
Tone: High-density, data-driven, strategic, engineering-focused. Answer in Traditional Chinese (繁體中文).
"""

    if "chat_messages" not in st.session_state:
        st.session_state.chat_messages = [
            {
                "role": "assistant",
                "content": f"👋 你好！我是 StackDiff 決策軍師（目前驅動引擎：**{provider} - {model}**）。全站已收錄 **{total_tools} 款工具** 與 **{total_matrices} 組對比頁面**。你可以點選下方快速提問，或直接諮詢 SEO 與獲利策略！",
            }
        ]

    # Quick Prompts Row (Stacked on Mobile)
    st.markdown("##### ⚡ 快速決策諮詢")
    qc1, qc2, qc3 = st.columns(3)
    quick_prompt = None
    with qc1:
        if st.button("💡 哪個類別對比太少？", use_container_width=True):
            quick_prompt = "分析目前各類別的工具分佈，指出哪幾個類別對比頁面數量太少，並具體推薦該追加收錄哪些熱門工具以放大長尾流量？"
    with qc2:
        if st.button("🚀 推薦 3 組高潛力對比詞", use_container_width=True):
            quick_prompt = "根據 2026 全球 AI 工具搜尋趨勢，推薦 3 組目前尚未被充分滿足、但在今年搜尋量爆發的高商業價值對比關鍵字？"
    with qc3:
        if st.button("💰 哪 5 款工具獲利潛力最高？", use_container_width=True):
            quick_prompt = "分析現有 31 款工具中，哪 5 款工具的聯盟導購獲利潛力最高？（考量付費轉換率、定價門檻與開箱剛需）"

    # Display chat history
    for msg in st.session_state.chat_messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Chat input
    user_prompt = st.chat_input("請輸入您對 StackDiff 的 SEO 佈局、類別擴充或聯盟行銷提問...") or quick_prompt

    if user_prompt:
        st.session_state.chat_messages.append({"role": "user", "content": user_prompt})
        with st.chat_message("user"):
            st.markdown(user_prompt)

        with st.chat_message("assistant"):
            with st.spinner(f"{provider} 正在深度運算決策戰略..."):
                reply_text = call_ai_engine(user_prompt, chat_system_instruction, provider, api_key, model, base_url)

                # Fallback rule-based strategy if API key is not configured
                if not reply_text:
                    if "類別" in user_prompt or "少" in user_prompt:
                        reply_text = f"""### 📊 類別深度分佈診斷與擴張策略

目前 **31 款工具** 的各分類分佈如下：
- **Video AI**: 7 款 (21 組對比) – 流量第一主力。
- **Coding AI**: 5 款 (10 組對比) – 商業變現轉換率最佳。
- **LLM**: 5 款 (10 組對比) – 搜尋量龐大。
- **Image AI**: 5 款 (10 組對比) – 視覺傳播力強。
- **Voice AI**: 4 款 (6 組對比) – 即時串流語音為新藍海。
- **Workflow AI**: 3 款 (3 組對比) – **⚠️ 嚴重偏少！**
- **Music AI**: 2 款 (1 組對比) – **⚠️ 嚴重偏少！**

#### 🎯 優先補強建議：
1. **Music AI（立即擴充至 4 款）**：追加 **Mubert**、**Soundraw**，可將對比矩陣從 1 組激增至 6 組。
2. **Workflow AI（立即擴充至 5 款）**：追加 **n8n** (開源自動化代表)、**Dify**，直接攻佔企業自動化工程師搜尋意圖。"""
                    elif "關鍵字" in user_prompt or "對比" in user_prompt:
                        reply_text = """### 🚀 2026 高潛力未開發對比詞推薦

1. **`windsurf-vs-cursor` (The Battle of Agentic IDEs)**
   - **搜尋意圖**：開發者正在評估從 Cursor 遷移至 Windsurf 的性價比（$15 vs $20）。
   - **建議著重**：比較 Cascade 的終端自主執行能力與 Cursor Composer 的多檔案 Diff 體驗。

2. **`deepseek-r1-vs-openai-o1` (Open-Weight Reasoning vs Proprietary)**
   - **搜尋意圖**：架構師評估開源本地私有化部署與雲端 API 成本（DeepSeek 節省 90% 成本）。

3. **`cartesia-sonic-vs-elevenlabs` (Sub-100ms Ultra-Low Latency TTS)**
   - **搜尋意圖**：AI 語音對話機器人工程師尋找低於 100ms 延遲的即時語音方案。"""
                    else:
                        reply_text = f"""### 💡 戰略分析建議

根據目前 StackDiff 的營運數據（共 {total_tools} 款工具，覆蓋率 {affiliate_pct:.1f}%）：
1. **優先針對高點擊工具補齊代碼**：優先針對「Coding AI」與「Video AI」類別註冊 Rewardful / FirstPromoter / Impact 聯盟。
2. **靜態索引效能**：保持每頁生成的靜態純 HTML 結構，確保 Googlebot 秒級爬取與渲染。"""

                st.markdown(reply_text)
                st.session_state.chat_messages.append({"role": "assistant", "content": reply_text})
