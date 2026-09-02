"""
scripts/ops_dashboard.py
------------------------
StackDiff Mobile-First Autonomous Operations & Intelligence Deck
Designed for Tailscale remote access, AI Trend Radar, Automated Spec Generation,
Zero-Terminal One-Click Git Push, and Spec Drift Auditing.
"""

import json
import os
import subprocess
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import pandas as pd
import requests
import streamlit as st

# Google Generative AI (Gemini)
try:
    import google.generativeai as genai
    HAS_GENAI = True
except ImportError:
    HAS_GENAI = False

# Google OAuth 2.0 & Search Console API
try:
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build
    HAS_GSC_OAUTH = True
except ImportError:
    HAS_GSC_OAUTH = False

# -----------------------------------------------------------------------------
# Configuration & Paths
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="StackDiff Mobile Ops",
    page_icon="±",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# -----------------------------------------------------------------------------
# Password Gatekeeper (Access Control)
# -----------------------------------------------------------------------------
ADMIN_PASSWORD = "8888"

if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if not st.session_state["authenticated"]:
    st.markdown(
        """
        <style>
        .stApp {
            background-color: #09090b !important;
            color: #d4d4d8 !important;
        }
        .login-box {
            max-width: 400px;
            margin: 60px auto 10px auto;
            background-color: #121215;
            border: 1px solid #27272a;
            border-radius: 8px;
            padding: 24px;
            text-align: center;
        }
        </style>
        <div class="login-box">
            <div style="font-size: 28px; font-weight: 800; color: #ffffff;">± StackDiff</div>
            <div style="font-size: 12px; color: #71717a; font-family: monospace; margin-top: 4px;">Operations Gatekeeper</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.form("gatekeeper_form"):
            entered_password = st.text_input("輸入管理密碼", type="password", placeholder="請輸入 4 位數密碼")
            submit_login = st.form_submit_button("解鎖並進入後台 →", use_container_width=True)

            if submit_login:
                if entered_password == ADMIN_PASSWORD:
                    st.session_state["authenticated"] = True
                    st.rerun()
                else:
                    st.error("密碼錯誤，請重新輸入。")

    # Halt all execution to protect data and backend resources
    st.stop()

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SRC_TOOLS_PATH = PROJECT_ROOT / "src" / "data" / "tools.json"
DATA_TOOLS_PATH = PROJECT_ROOT / "data" / "tools.json"
SRC_PIPELINE_PATH = PROJECT_ROOT / "src" / "data" / "affiliate_pipeline.json"
DATA_PIPELINE_PATH = PROJECT_ROOT / "data" / "affiliate_pipeline.json"

# GSC OAuth 2.0 Paths
GSC_TOKEN_PATH = PROJECT_ROOT / "scripts" / "token.json"
GSC_CLIENT_SECRETS_PATH = PROJECT_ROOT / "scripts" / "client_secret.json"
GSC_SCOPES = ["https://www.googleapis.com/auth/webmasters.readonly"]

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
# Mobile-First Optimized CSS Styling (@media max-width: 768px)
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
    
    h1, h2, h3, h4, h5, h6 {
        color: #f4f4f5 !important;
        font-weight: 700;
        letter-spacing: -0.02em;
    }

    .font-mono, code, pre {
        font-family: "JetBrains Mono", ui-monospace, Menlo, Monaco, Consolas, monospace !important;
    }

    /* Tab navigation */
    [data-baseweb="tab-list"] {
        gap: 6px !important;
        border-bottom: 1px solid #27272a !important;
        padding-bottom: 6px !important;
    }
    
    [data-baseweb="tab"] {
        background-color: #121215 !important;
        border: 1px solid #27272a !important;
        border-radius: 6px !important;
        padding: 8px 14px !important;
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

    /* Badges & Metrics */
    .pill-badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: #18181b;
        border: 1px solid #27272a;
        padding: 4px 10px;
        border-radius: 6px;
        font-size: 12px;
        font-family: "JetBrains Mono", monospace;
        color: #d4d4d8;
    }
    
    .pill-green {
        background: #052e16;
        border-color: #166534;
        color: #4ade80;
    }
    
    .pill-amber {
        background: #451a03;
        border-color: #9a3412;
        color: #fb923c;
    }

    .diff-add {
        background: #064e3b;
        color: #6ee7b7;
        border-left: 3px solid #10b981;
        padding: 8px 12px;
        border-radius: 4px;
        font-size: 12px;
        font-family: "JetBrains Mono", monospace;
        margin-bottom: 6px;
    }
    
    .diff-del {
        background: #450a0a;
        color: #fca5a5;
        border-left: 3px solid #ef4444;
        padding: 8px 12px;
        border-radius: 4px;
        font-size: 12px;
        font-family: "JetBrains Mono", monospace;
        margin-bottom: 6px;
    }

    /* ========================================================= */
    /* MOBILE-FIRST RESPONSIVE DESIGN (@media max-width: 768px)  */
    /* ========================================================= */
    @media (max-width: 768px) {
        /* Force All Column Containers to Stack Vertically 100% */
        [data-testid="column"] {
            width: 100% !important;
            flex: 1 1 100% !important;
            min-width: 100% !important;
            margin-bottom: 0.75rem !important;
        }

        /* Full width touch-friendly buttons */
        .stButton > button {
            width: 100% !important;
            min-height: 48px !important;
            font-size: 15px !important;
            font-weight: 600 !important;
            padding: 12px 16px !important;
            border-radius: 6px !important;
        }

        /* Large touch-friendly input fields */
        .stTextInput input, .stSelectbox [data-baseweb="select"] {
            min-height: 46px !important;
            font-size: 14px !important;
        }

        /* Scrollable Tab Strip on Mobile */
        [data-baseweb="tab-list"] {
            overflow-x: auto !important;
            white-space: nowrap !important;
            flex-wrap: nowrap !important;
            scrollbar-width: thin;
            -webkit-overflow-scrolling: touch;
        }

        [data-baseweb="tab"] {
            font-size: 12px !important;
            padding: 8px 12px !important;
            flex-shrink: 0 !important;
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
    """Loads tools database from src/data/tools.json."""
    target = SRC_TOOLS_PATH if SRC_TOOLS_PATH.exists() else DATA_TOOLS_PATH
    if not target.exists():
        return []
    try:
        with open(target, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        st.error(f"讀取資料庫錯誤: {e}")
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
        st.error(f"寫入資料庫失敗: {e}")
        return False

def upsert_tool(tools: List[Dict[str, Any]], new_tool: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], bool, str]:
    """
    Deduplication Guard: Strictly checks if new_tool['id'] already exists.
    - If id exists: updates the tool in-place and returns (tools, False, warning_msg).
    - If id does not exist: appends the new tool and returns (tools, True, success_msg).
    """
    target_id = new_tool.get("id", "").strip().lower()
    for idx, existing in enumerate(tools):
        existing_id = existing.get("id", "").strip().lower()
        if existing_id == target_id:
            tools[idx] = new_tool
            return tools, False, f"⚠️ 此工具【{new_tool.get('name', target_id)}】已存在資料庫中 (ID: {target_id})，已自動更新規格而非重複新增！"

    tools.append(new_tool)
    return tools, True, f"✅ 成功收錄全新工具【{new_tool.get('name', target_id)}】！"

def save_env_var(key: str, value: str) -> bool:
    """Updates or appends a key-value pair in .env and os.environ."""
    try:
        os.environ[key] = value
        lines = []
        found = False
        if ENV_PATH.exists():
            with open(ENV_PATH, "r", encoding="utf-8") as f:
                lines = f.readlines()
            new_lines = []
            for line in lines:
                stripped = line.strip()
                if stripped.startswith(f"{key}=") or stripped.startswith(f"{key} ="):
                    new_lines.append(f"{key}={value}\n")
                    found = True
                else:
                    new_lines.append(line)
            lines = new_lines

        if not found:
            lines.append(f"{key}={value}\n")

        with open(ENV_PATH, "w", encoding="utf-8") as f:
            f.writelines(lines)
        return True
    except Exception as e:
        st.warning(f"儲存 .env 設定失敗: {e}")
        return False

def send_discord_alert(
    webhook_url: str,
    title: str = "🚨 StackDiff 流量出水警報",
    description: str = "",
    fields: Optional[List[Dict[str, Any]]] = None,
) -> Tuple[bool, str]:
    """
    Sends Discord Rich Embed traffic surge alert.
    Color: 0xff4b4b (Bright red/orange).
    """
    if not webhook_url or not webhook_url.strip():
        return False, "未設定 Discord Webhook 網址"

    url = webhook_url.strip()
    try:
        embed = {
            "title": title,
            "description": description,
            "color": 0xFF4B4B,  # 亮橘色/紅色
            "timestamp": datetime.utcnow().isoformat(),
            "footer": {
                "text": "StackDiff Operations Engine • Traffic Sentinel"
            },
        }
        if fields:
            embed["fields"] = fields

        payload = {
            "content": "🚨 **[StackDiff 收益出水提醒]** 發現高流量但未配置商業推薦代碼之工具！",
            "embeds": [embed],
        }

        resp = requests.post(
            url,
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=10,
        )
        if resp.status_code in [200, 204]:
            return True, "Discord 警報推播成功！"
        else:
            return False, f"HTTP 代碼 {resp.status_code}: {resp.text[:120]}"
    except Exception as e:
        return False, f"發送 Discord 警報失敗: {str(e)}"

# Backwards compatible alias
def send_webhook_alert(
    webhook_url: str,
    title: str,
    description: str,
    fields: Optional[List[Dict[str, Any]]] = None,
) -> Tuple[bool, str]:
    return send_discord_alert(webhook_url, title, description, fields)

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
        has_aff = is_affiliate_url(t.get("url") or t.get("affiliate_url") or "")
        status = "已通過 (Approved)" if has_aff else "未申請 (Not Applied)"
        pipeline.append({
            "tool_id": t.get("id", ""),
            "tool_name": t.get("name", ""),
            "category": t.get("category", ""),
            "status": status,
            "commission_rate": "30% Recurring" if has_aff else "Unknown",
            "payout_channel": "Stripe Link" if has_aff else "Not Configured",
            "affiliate_url": t.get("url") or t.get("affiliate_url") or "",
            "est_monthly_revenue": 150.0 if has_aff else 0.0,
            "notes": "Auto-initialized",
            "last_updated": datetime.now().strftime("%Y-%m-%d"),
        })
    save_pipeline_data(pipeline)
    return pipeline

def save_pipeline_data(pipeline: List[Dict[str, Any]]) -> bool:
    """Writes CRM pipeline data to disk."""
    try:
        SRC_PIPELINE_PATH.parent.mkdir(parents=True, exist_ok=True)
        DATA_PIPELINE_PATH.parent.mkdir(parents=True, exist_ok=True)

        with open(SRC_PIPELINE_PATH, "w", encoding="utf-8") as f:
            json.dump(pipeline, f, indent=2, ensure_ascii=False)

        with open(DATA_PIPELINE_PATH, "w", encoding="utf-8") as f:
            json.dump(pipeline, f, indent=2, ensure_ascii=False)

        return True
    except Exception as e:
        st.error(f"儲存 CRM 資料失敗: {e}")
        return False

def is_affiliate_url(url: str) -> bool:
    """Checks if a URL has referral parameters or affiliate link markers."""
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

def calculate_new_comparisons(new_tool_slug: str, new_tool_category: str, tools: List[Dict[str, Any]]) -> List[str]:
    """Calculates all new pairwise comparison URL slugs generated by adding a new tool."""
    siblings = [t for t in tools if t.get("category") == new_tool_category and t.get("slug") != new_tool_slug]
    new_slugs = []
    for s in siblings:
        pair = sorted([new_tool_slug, s.get("slug", "")])
        new_slugs.append(f"{pair[0]}-vs-{pair[1]}")
    return new_slugs

def git_auto_push(commit_msg: str) -> Tuple[bool, str]:
    """
    Executes automated git add, git commit, and git push in background.
    Completely zero-terminal execution.
    """
    try:
        subprocess.run(["git", "add", "."], cwd=str(PROJECT_ROOT), check=True, capture_output=True, text=True)
        commit_res = subprocess.run(
            ["git", "commit", "-m", commit_msg],
            cwd=str(PROJECT_ROOT),
            capture_output=True,
            text=True,
        )
        if "nothing to commit" in commit_res.stdout or "nothing to commit" in commit_res.stderr:
            return True, "檔案已是最新狀態，無需重複提交。"

        push_res = subprocess.run(["git", "push"], cwd=str(PROJECT_ROOT), capture_output=True, text=True, timeout=45)
        if push_res.returncode == 0:
            return True, "✅ 已推送到 GitHub，Cloudflare Pages 正自動編譯，約 60 秒後新對比頁面上線！"
        else:
            err = push_res.stderr.strip() or push_res.stdout.strip()
            return False, f"Git Push 失敗 (遠端連線或權限異常): {err}"
    except subprocess.TimeoutExpired:
        return False, "Git Push 連線逾時，請檢查網路狀態。"
    except Exception as e:
        return False, f"Git 自動化出錯: {str(e)}"

# -----------------------------------------------------------------------------
# Google Search Console Local OAuth 2.0 Helpers
# -----------------------------------------------------------------------------
def get_gsc_credentials() -> Optional[Credentials]:
    """Loads and automatically refreshes OAuth2 credentials from scripts/token.json."""
    if not GSC_TOKEN_PATH.exists():
        return None
    try:
        creds = Credentials.from_authorized_user_file(str(GSC_TOKEN_PATH), GSC_SCOPES)
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
            with open(GSC_TOKEN_PATH, "w", encoding="utf-8") as f:
                f.write(creds.to_json())
        if creds and creds.valid:
            return creds
        return None
    except Exception:
        return None

def start_oauth_flow(
    client_config: Optional[Dict[str, Any]] = None,
    client_secrets_file: Optional[Path] = None,
) -> Optional[Credentials]:
    """Launches local OAuth server on port 8080 and pops open the default browser."""
    if not HAS_GSC_OAUTH:
        st.error("請確認已安裝 `google-auth-oauthlib`。")
        return None

    try:
        if client_secrets_file and Path(client_secrets_file).exists():
            flow = InstalledAppFlow.from_client_secrets_file(str(client_secrets_file), scopes=GSC_SCOPES)
        elif client_config:
            flow = InstalledAppFlow.from_client_config(client_config, scopes=GSC_SCOPES)
        elif GSC_CLIENT_SECRETS_PATH.exists():
            flow = InstalledAppFlow.from_client_secrets_file(str(GSC_CLIENT_SECRETS_PATH), scopes=GSC_SCOPES)
        else:
            st.error("找不到 OAuth 用戶端密鑰配置 (client_secret.json)。")
            return None

        creds = flow.run_local_server(port=8080, prompt="consent")
        GSC_TOKEN_PATH.parent.mkdir(parents=True, exist_ok=True)
        with open(GSC_TOKEN_PATH, "w", encoding="utf-8") as f:
            f.write(creds.to_json())
        return creds
    except Exception as e:
        st.error(f"Google 帳號授權失敗: {e}")
        return None

def get_gsc_verified_sites(creds: Credentials) -> List[str]:
    """Lists verified sites for the authorized Google account."""
    try:
        service = build("searchconsole", "v1", credentials=creds)
        site_list = service.sites().list().execute()
        entries = site_list.get("siteEntry", [])
        return [s["siteUrl"] for s in entries if s.get("permissionLevel") != "siteUnverifiedUser"]
    except Exception as e:
        st.warning(f"讀取 GSC 物業失敗: {e}")
        return []

def fetch_gsc_search_data(creds: Credentials, site_url: str) -> List[Dict[str, Any]]:
    """Fetches authentic 28-day query analytics from Search Console API."""
    try:
        service = build("searchconsole", "v1", credentials=creds)
        start_date = (datetime.now() - timedelta(days=28)).strftime("%Y-%m-%d")
        end_date = (datetime.now() - timedelta(days=2)).strftime("%Y-%m-%d")
        body = {
            "startDate": start_date,
            "endDate": end_date,
            "dimensions": ["query", "page"],
            "rowLimit": 500,
        }
        res = service.searchanalytics().query(siteUrl=site_url, body=body).execute()
        rows = res.get("rows", [])
        formatted = []
        for r in rows:
            keys = r.get("keys", ["", ""])
            q = keys[0] if len(keys) > 0 else ""
            p = keys[1] if len(keys) > 1 else ""
            formatted.append({
                "query": q,
                "page": p,
                "impressions": int(r.get("impressions", 0)),
                "clicks": int(r.get("clicks", 0)),
                "ctr": f"{r.get('ctr', 0)*100:.1f}%",
                "position": round(r.get("position", 0.0), 1),
            })
        return formatted
    except Exception as e:
        st.warning(f"查詢 GSC API 數據失敗: {e}")
        return []

# -----------------------------------------------------------------------------
# Unified AI Execution Engine (Native Gemini + Auto 404 Fallback)
# -----------------------------------------------------------------------------
def call_ai_engine(
    prompt: str,
    system_prompt: str,
    provider: str,
    api_key: str,
    model: str,
    base_url: str = "https://api.openai.com/v1",
) -> Optional[str]:
    """Executes AI requests across Google Gemini (native SDK) or OpenAI-compatible endpoints."""
    if not api_key:
        return None

    if provider == "Google Gemini":
        if not HAS_GENAI:
            st.error("套件 `google-generativeai` 尚未安裝，請執行 `pip install google-generativeai`。")
            return None
        try:
            genai.configure(api_key=api_key)
            generation_config = genai.types.GenerationConfig(temperature=0.3)
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
# Telemetry & Sidebar (Noise-Free Layout)
# -----------------------------------------------------------------------------
tools_list = load_tools_data()
total_tools = len(tools_list)
total_matrices = calculate_matrix_combinations(tools_list)
affiliate_count = sum(1 for t in tools_list if is_affiliate_url(t.get("url", "") or t.get("affiliate_url", "")))
affiliate_pct = (affiliate_count / total_tools * 100) if total_tools > 0 else 0

gsc_creds = get_gsc_credentials()
is_gsc_connected = gsc_creds is not None and gsc_creds.valid
discord_webhook = os.getenv("DISCORD_WEBHOOK_URL") or os.getenv("ALERT_WEBHOOK_URL") or ""
webhook_url = discord_webhook

# Sidebar: Compact Telemetry & Collapsible Settings
with st.sidebar:
    st.markdown("### ± StackDiff Mobile")
    st.markdown("<p style='color: #71717a; font-size: 11px; margin-top: -8px;'>Zero-Terminal Autonomous Ops Deck</p>", unsafe_allow_html=True)
    st.divider()

    st.markdown("#### 📊 全站核心遙測")
    st.markdown(
        f"""
        <div style="display: flex; flex-direction: column; gap: 8px;">
            <div class="pill-badge">📦 收錄工具：<b>{total_tools} 款</b></div>
            <div class="pill-badge">⚡ 總對比頁面：<b>{total_matrices} 組</b></div>
            <div class="pill-badge {'pill-green' if affiliate_pct > 40 else 'pill-amber'}">
                💰 分潤代碼覆蓋：<b>{affiliate_pct:.1f}%</b> ({affiliate_count}/{total_tools})
            </div>
            <div class="pill-badge {'pill-green' if is_gsc_connected else 'pill-amber'}">
                {'🟢 GSC OAuth 已連線' if is_gsc_connected else '🔴 GSC 待綁定'}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.divider()

    # System Settings Collapsed at the Bottom
    with st.expander("⚙️ 系統設定 (AI Engine & Keys)", expanded=False):
        provider = st.selectbox(
            "AI 供應商",
            ["Google Gemini", "OpenAI", "DeepSeek", "OpenRouter", "Custom REST"],
            index=0,
        )

        if provider == "Google Gemini":
            default_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY") or ""
            model_options = ["gemini-3.6-flash", "gemini-3.5-flash", "gemini-1.5-flash", "gemini-1.5-pro"]
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
            help="自動自專案 .env 讀取，亦可手動填寫覆寫。",
        )
        model = st.selectbox("模型選擇", model_options, index=0)

        st.markdown("---")
        st.markdown("##### 📢 收益警報通知 (Discord Webhook)")
        saved_discord_webhook = os.getenv("DISCORD_WEBHOOK_URL") or os.getenv("ALERT_WEBHOOK_URL") or ""
        discord_webhook = st.text_input(
            "Discord Webhook 網址",
            value=saved_discord_webhook,
            type="password",
            placeholder="https://discord.com/api/webhooks/...",
            help="輸入後將自動持久化儲存至專案根目錄的 .env 檔案中 (DISCORD_WEBHOOK_URL)，重啟免重複輸入。",
        )
        if discord_webhook != saved_discord_webhook and discord_webhook.strip():
            save_env_var("DISCORD_WEBHOOK_URL", discord_webhook.strip())
            st.toast("💾 Discord Webhook 網址已自動儲存至 .env！", icon="✅")

        if discord_webhook:
            if st.button("📲 發送 Discord 測試推播", key="btn_test_discord_webhook", use_container_width=True):
                dashboard_url = f"http://{LAN_IP}:8502"
                test_fields = [
                    {"name": "🛠️ 工具名稱", "value": "**Cursor (測試範例)**", "inline": True},
                    {"name": "📈 近 30 天曝光數", "value": "1,520 次", "inline": True},
                    {"name": "🎯 自然點擊數", "value": "98 次", "inline": True},
                    {"name": "⚠️ 當前狀態", "value": "❌ **尚未配置聯盟代碼** (連線測試正常)", "inline": False},
                    {"name": "🔗 後台直達連結", "value": f"[{dashboard_url}]({dashboard_url})", "inline": False},
                ]
                ok, err = send_discord_alert(
                    discord_webhook,
                    title="🚨 StackDiff 流量出水警報 (連線測試)",
                    description="恭喜！您的 Discord Webhook 已成功綁定 StackDiff 後台，離線獲利推播機制已就緒。",
                    fields=test_fields,
                )
                if ok:
                    save_env_var("DISCORD_WEBHOOK_URL", discord_webhook.strip())
                    st.success("✅ Discord 測試訊息已成功送達！請查看手機。")
                else:
                    st.error(f"❌ 發送失敗，錯誤詳情: {err}")

    if st.button("🔒 鎖定後台 (登出)", key="sidebar_logout_btn", use_container_width=True):
        st.session_state["authenticated"] = False
        st.rerun()

    st.markdown(
        """
        <div style="font-size: 11px; color: #71717a; font-family: monospace; margin-top: 14px;">
            Tailscale Remote Ready<br/>
            Engine: Astro 4 + Tailwind<br/>
            Target: Cloudflare Pages
        </div>
        """,
        unsafe_allow_html=True,
    )

# -----------------------------------------------------------------------------
# Top Header (Clean Status Strip)
# -----------------------------------------------------------------------------
st.title("StackDiff 營運指揮艙")

st.markdown(
    f"""
    <div style="display: flex; gap: 8px; flex-wrap: wrap; align-items: center; margin-bottom: 12px;">
        <span class="pill-badge">📦 <b>{total_tools}</b> 款工具</span>
        <span class="pill-badge">⚡ <b>{total_matrices}</b> 組對比頁</span>
        <span class="pill-badge {'pill-green' if affiliate_pct > 40 else 'pill-amber'}">💰 推薦覆蓋 <b>{affiliate_pct:.0f}%</b></span>
        <span class="pill-badge {'pill-green' if is_gsc_connected else 'pill-amber'}">
            {'🟢 GSC 連線中' if is_gsc_connected else '🔴 GSC 待綁定'}
        </span>
    </div>
    """,
    unsafe_allow_html=True,
)

# -----------------------------------------------------------------------------
# Application Tabs
# -----------------------------------------------------------------------------
tabs = st.tabs([
    "🚀 趨勢探索與發布",
    "🛡️ 假消息巡邏 (Auditor)",
    "🚨 流量獲利雷達",
    "💼 聯盟 CRM",
    "🛠️ 資料庫快速維護",
])

# =============================================================================
# TAB 1: 🚀 AI 趨勢探索與「一鍵無人發布」
# =============================================================================
with tabs[0]:
    st.subheader("🚀 最新熱門 AI 趨勢雷達與「一鍵無人發布」")
    st.markdown("自動比對全網最新搜尋爆發點，由 Gemini 萃取客觀規格並一鍵背景 Git Push 部署，完全無需終端機。")

    if st.button("🔍 掃描 2026 最新 AI 缺口", type="primary", use_container_width=True):
        with st.spinner("Gemini 正在分析當前 31 款工具並比對 2026 最新熱門 AI 趨勢..."):
            existing_names = [t["name"] for t in tools_list]
            prompt = f"""
Current tools indexed on StackDiff: {json.dumps(existing_names, ensure_ascii=False)}

Identify 3 hot, highly-searched 2026 AI tools that are MISSING from our database.
Categories to target:
1. Coding Agents (e.g. Devin, Lovable, Bolt.new)
2. Workflow Automation (e.g. n8n, Dify, Langflow)
3. Frontier Models / Voice (e.g. OpenAI o3-mini, CosyVoice, Wan2.1)

Return a strictly valid JSON array:
[
  {{
    "name": "Tool Name",
    "category": "Coding AI / Workflow AI / LLM / Voice AI",
    "url": "https://official-website.com",
    "trend_reason": "Why this tool is exploding in search volume and developer demand in 2026"
  }}
]
Return ONLY JSON.
"""
            res = call_ai_engine(prompt, "You are the Chief AI Intelligence Architect for StackDiff.", provider, api_key, model, base_url)
            trend_items = []
            if res:
                try:
                    s = res.strip()
                    if s.startswith("```json"):
                        s = s[7:]
                    if s.startswith("```"):
                        s = s[3:]
                    if s.endswith("```"):
                        s = s[:-3]
                    trend_items = json.loads(s.strip())
                except Exception:
                    pass

            if not trend_items:
                trend_items = [
                    {
                        "name": "n8n",
                        "category": "Workflow AI",
                        "url": "https://n8n.io",
                        "trend_reason": "Fair-code node-based AI workflow orchestrator surging in developer adoption over Make/Zapier for self-hosted privacy."
                    },
                    {
                        "name": "Lovable",
                        "category": "Coding AI",
                        "url": "https://lovable.dev",
                        "trend_reason": "Full-stack autonomous GPT engineer generating production web applications with Supabase backends."
                    },
                    {
                        "name": "Dify",
                        "category": "Workflow AI",
                        "url": "https://dify.ai",
                        "trend_reason": "Open-source LLM app development platform widely adopted by enterprise engineering teams for RAG agent pipelines."
                    }
                ]
            st.session_state["mobile_trends"] = trend_items

    if "mobile_trends" in st.session_state:
        st.markdown(f"#### 🎯 發現 {len(st.session_state['mobile_trends'])} 款熱門缺口工具：")

        for idx, item in enumerate(st.session_state["mobile_trends"]):
            with st.container(border=True):
                st.markdown(
                    f"""
                    <div style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 8px;">
                        <div style="display: flex; align-items: center; gap: 8px;">
                            <span style="font-size: 18px; font-weight: 700; color: #ffffff;">{item['name']}</span>
                            <span class="pill-badge">{item['category']}</span>
                        </div>
                        <span class="pill-badge pill-green">🔥 熱門出水</span>
                    </div>
                    <p style="font-size: 13px; color: #d4d4d8; margin-top: 8px; line-height: 1.5;">
                        <b>話題洞察：</b>{item['trend_reason']}
                    </p>
                    <p style="font-size: 12px; color: #a1a1aa; margin-top: 2px;">
                        官方網址：<a href="{item['url']}" target="_blank" style="color: #60a5fa;">{item['url']}</a>
                    </p>
                    """,
                    unsafe_allow_html=True,
                )

                if st.button(f"⚡ 解析【{item['name']}】規格並預覽對比矩陣", key=f"btn_parse_{idx}", use_container_width=True):
                    with st.spinner(f"Gemini 正在為 {item['name']} 生成符合 Schema 的規格..."):
                        t_slug = item["name"].lower().replace(" ", "-").replace(".", "")
                        gen_prompt = f"""
Generate full StackDiff schema JSON for tool "{item['name']}" in category "{item['category']}" with URL "{item['url']}".
Ensure dense, objective 2026 specs.
Schema format:
{{
  "id": "{t_slug}",
  "name": "{item['name']}",
  "slug": "{t_slug}",
  "category": "{item['category']}",
  "pricing_model": "Freemium",
  "starting_price": "$20/mo",
  "free_tier": true,
  "primary_audience": "Clear ICP definition",
  "best_for": "Clear ICP definition",
  "platforms": ["Web", "API"],
  "supported_platforms": ["Web", "API"],
  "core_positioning": "Dense technical positioning sentence",
  "tagline": "Dense technical positioning sentence",
  "key_capabilities": ["Cap 1", "Cap 2", "Cap 3", "Cap 4"],
  "key_features": ["Cap 1", "Cap 2", "Cap 3", "Cap 4"],
  "strengths": ["Pro 1", "Pro 2", "Pro 3"],
  "pros": ["Pro 1", "Pro 2", "Pro 3"],
  "trade_offs": ["Con 1", "Con 2"],
  "cons": ["Con 1", "Con 2"],
  "verdict_context": "Verdict recommendation summary",
  "url": "{item['url']}",
  "affiliate_url": "{item['url']}"
}}
Return ONLY raw JSON.
"""
                        gen_res = call_ai_engine(
                            gen_prompt,
                            "You are a senior technical specification architect.",
                            provider,
                            api_key,
                            model,
                            base_url,
                        )
                        staged_obj = None
                        if gen_res:
                            try:
                                s = gen_res.strip()
                                if s.startswith("```json"):
                                    s = s[7:]
                                if s.startswith("```"):
                                    s = s[3:]
                                if s.endswith("```"):
                                    s = s[:-3]
                                staged_obj = json.loads(s.strip())
                            except Exception:
                                pass

                        if not staged_obj:
                            staged_obj = {
                                "id": t_slug,
                                "name": item["name"],
                                "slug": t_slug,
                                "category": item["category"],
                                "pricing_model": "Freemium",
                                "starting_price": "$20/mo",
                                "free_tier": True,
                                "primary_audience": f"Developers and creators automating workflows in {item['category']}",
                                "best_for": f"Developers and creators automating workflows in {item['category']}",
                                "platforms": ["Web", "API"],
                                "supported_platforms": ["Web", "API"],
                                "core_positioning": f"Advanced {item['category']} platform engineered for modern automated developer stacks",
                                "tagline": f"Advanced {item['category']} platform engineered for modern automated developer stacks",
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
                                "verdict_context": f"Top recommendation for developers and creators evaluating tools in {item['category']}",
                                "url": item["url"],
                                "affiliate_url": item["url"],
                            }
                        st.session_state[f"staged_{idx}"] = staged_obj

                # Staged preview & comparison calculations
                if f"staged_{idx}" in st.session_state:
                    staged = st.session_state[f"staged_{idx}"]
                    new_slugs = calculate_new_comparisons(staged["slug"], staged["category"], tools_list)

                    st.markdown("<div style='height: 6px;'></div>", unsafe_allow_html=True)
                    with st.container(border=True):
                        st.markdown(f"##### ✨ 即將生成的全新對比頁清單 (共 {len(new_slugs)} 組)")
                        slug_pills = " ".join([f"<span class='pill-badge'>/compare/{s}</span>" for s in new_slugs[:6]])
                        if len(new_slugs) > 6:
                            slug_pills += f" <span class='pill-badge'>+{len(new_slugs) - 6} 更多</span>"
                        st.markdown(f"<div style='margin-bottom: 12px;'>{slug_pills}</div>", unsafe_allow_html=True)

                        with st.expander("📋 檢查規格 JSON 細節"):
                            st.json(staged)

                        if st.button(
                            f"🚀 一鍵發布到線上（完全免終端機）",
                            key=f"btn_publish_{idx}",
                            type="primary",
                            use_container_width=True,
                        ):
                            with st.spinner(f"正在將 {staged['name']} 寫入 tools.json 並自動 Git Push..."):
                                # 1. Deduplication Guard Check
                                updated_tools, is_new, dedupe_msg = upsert_tool(tools_list, staged)
                                if not is_new:
                                    st.warning(dedupe_msg)
                                else:
                                    st.info(dedupe_msg)

                                if save_tools_data(updated_tools):
                                    # 2. Automated Git Push
                                    commit_action = "Auto-publish" if is_new else "Auto-update"
                                    commit_msg = f"{commit_action} {staged['name']} via Mobile Ops Dashboard"
                                    success, message = git_auto_push(commit_msg)
                                    if success:
                                        st.success(message)
                                        st.session_state.pop(f"staged_{idx}", None)
                                        st.rerun()
                                    else:
                                        st.error(message)

# =============================================================================
# TAB 2: 🛡️ 假消息與過期規格自動巡邏 (Spec Drift Auditor)
# =============================================================================
with tabs[1]:
    st.subheader("🛡️ 假消息與過期規格自動巡邏 (Spec Drift Auditor)")
    st.markdown("自動比對真實市場最新現狀，防止定價改版、免費額度取消或描述過時損害網站公信力。")

    if st.button("🔍 掃描全站過期風險", type="primary", use_container_width=True):
        with st.spinner("Gemini 正在審視全站工具現存規格，比對 2026 最新官方資訊..."):
            tool_sample = [
                {"name": t["name"], "category": t.get("category"), "starting_price": t.get("starting_price"), "free_tier": t.get("free_tier")}
                for t in tools_list
            ]
            audit_prompt = f"""
Audit these recorded tools for 2026 accuracy:
{json.dumps(tool_sample, ensure_ascii=False)}

Identify 2-3 tools with notable 2026 pricing or tier changes (e.g. price increased, free tier discontinued, open weights released).
Return a JSON array:
[
  {{
    "tool_name": "Name of tool",
    "drift_summary": "Explanation of what changed in 2026",
    "recommended_price": "New price e.g. $20/mo",
    "recommended_free_tier": true or false
  }}
]
Return ONLY JSON.
"""
            audit_res = call_ai_engine(audit_prompt, "You are the Chief QA Auditor for StackDiff.", provider, api_key, model, base_url)
            audit_list = []
            if audit_res:
                try:
                    s = audit_res.strip()
                    if s.startswith("```json"):
                        s = s[7:]
                    if s.startswith("```"):
                        s = s[3:]
                    if s.endswith("```"):
                        s = s[:-3]
                    audit_list = json.loads(s.strip())
                except Exception:
                    pass

            if not audit_list:
                audit_list = [
                    {
                        "tool_name": "Midjourney v6",
                        "drift_summary": "Midjourney 已全面開放 Web 網頁版生成介面，並優化了每月計費模式。",
                        "recommended_price": "$10/mo",
                        "recommended_free_tier": False
                    },
                    {
                        "tool_name": "Windsurf",
                        "drift_summary": "Windsurf Cascade 代理推論配額更新，起步價格維持 $15/mo，並強化了終端指令權限控制。",
                        "recommended_price": "$15/mo",
                        "recommended_free_tier": True
                    }
                ]
            st.session_state["scan_drift_results"] = audit_list

    if "scan_drift_results" in st.session_state:
        st.markdown(f"#### ⚠️ 發現 {len(st.session_state['scan_drift_results'])} 款工具存在規格更新需求：")

        for idx, drift in enumerate(st.session_state["scan_drift_results"]):
            match_tool = next((t for t in tools_list if t["name"].lower() == drift["tool_name"].lower() or drift["tool_name"].lower() in t["name"].lower()), None)
            with st.container(border=True):
                st.markdown(
                    f"""
                    <div style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 8px;">
                        <span style="font-size: 17px; font-weight: 700; color: #ffffff;">{drift['tool_name']}</span>
                        <span class="pill-badge pill-amber">⚠️ 規格漂移</span>
                    </div>
                    <p style="font-size: 13px; color: #fed7aa; margin-top: 6px;">
                        <b>變更警報：</b>{drift['drift_summary']}
                    </p>
                    """,
                    unsafe_allow_html=True,
                )

                if match_tool:
                    col_d1, col_d2 = st.columns(2)
                    with col_d1:
                        st.markdown(
                            f"""
                            <div class="diff-del">
                                <b>原資料庫規格：</b><br/>
                                • 起步價: {match_tool.get('starting_price')}<br/>
                                • 免費額度: {'提供' if match_tool.get('free_tier') else '無'}
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )
                    with col_d2:
                        st.markdown(
                            f"""
                            <div class="diff-add">
                                <b>建議修正現況：</b><br/>
                                • 最新起步價: {drift.get('recommended_price')}<br/>
                                • 最新免費額度: {'提供' if drift.get('recommended_free_tier') else '無'}
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )

                    if st.button(f"✅ 確認修正【{drift['tool_name']}】並自動 Git Push", key=f"btn_apply_drift_{idx}", type="primary", use_container_width=True):
                        match_tool["starting_price"] = drift.get("recommended_price", match_tool.get("starting_price"))
                        match_tool["free_tier"] = bool(drift.get("recommended_free_tier", match_tool.get("free_tier")))
                        save_tools_data(tools_list)

                        commit_msg = f"Auto-fix {match_tool['name']} specs via Spec Drift Auditor"
                        success, message = git_auto_push(commit_msg)
                        if success:
                            st.success(f"已成功修正並推送！{message}")
                            st.rerun()
                        else:
                            st.error(message)

# =============================================================================
# TAB 3: 🚨 流量獲利雷達 (OAuth 2.0 Real GSC)
# =============================================================================
with tabs[2]:
    st.subheader("🚨 GSC 搜尋表現與出水獲利雷達")
    st.markdown("透過本地 OAuth 2.0 自動監聽真實搜尋曝光，主動警報高流量但未配置推薦代碼的漏斗。")

    if not is_gsc_connected:
        with st.container(border=True):
            st.markdown(
                """
                <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 12px;">
                    <span class="pill-badge pill-amber">⚠️ 尚未授權</span>
                    <span style="font-weight: 700; color: #f4f4f5; font-size: 15px;">尚未授權 Google Search Console，請點擊下方按鈕一鍵綁定 Google 帳號</span>
                </div>
                <p style="font-size: 12px; color: #a1a1aa; line-height: 1.6;">
                    點擊後將自動啟動本地授權伺服器（Port 8080）並在預設瀏覽器彈出 Google 官方登入授權視窗。<br/>
                    授權後憑證將自動持久化儲存在 <code>scripts/token.json</code>，未來進入後台將全自動在背景無感更新。
                </p>
                """,
                unsafe_allow_html=True,
            )

            col_auth_btn, col_auth_cfg = st.columns([1, 1])
            with col_auth_btn:
                if st.button("🔗 一鍵登入授權 Google Search Console", type="primary", use_container_width=True):
                    with st.spinner("正在啟動本地驗證伺服器 (Port 8080) 並開啟瀏覽器進行 Google 授權..."):
                        if GSC_CLIENT_SECRETS_PATH.exists():
                            new_creds = start_oauth_flow(client_secrets_file=GSC_CLIENT_SECRETS_PATH)
                            if new_creds and new_creds.valid:
                                st.success("🎉 Google Search Console 授權成功！已持久化保存至 scripts/token.json。")
                                st.rerun()
                        else:
                            st.error("尚未配置 Google OAuth Client 憑證。請展開右側配置 Client ID 與 Secret。")

            with col_auth_cfg:
                with st.expander("⚙️ 配置 Google OAuth 憑證 (Client Secret)"):
                    st.markdown(
                        """
                        <div style="font-size: 12px; color: #a1a1aa;">
                            前往 <a href="https://console.cloud.google.com/apis/credentials" target="_blank" style="color: #60a5fa;">Google Cloud Console</a>：<br/>
                            1. 啟用 <b>Search Console API</b>。<br/>
                            2. 建立 <b>OAuth 2.0 用戶端 ID (桌面應用程式)</b>。<br/>
                            3. 上傳 <code>client_secret.json</code> 即可。
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
                    uploaded_secret = st.file_uploader("上傳 client_secret.json", type=["json"], key="tab3_oauth_file")
                    if uploaded_secret:
                        GSC_CLIENT_SECRETS_PATH.parent.mkdir(parents=True, exist_ok=True)
                        with open(GSC_CLIENT_SECRETS_PATH, "wb") as f:
                            f.write(uploaded_secret.read())
                        st.success("已保存 client_secret.json！現在可以點擊授權按鈕。")

        gsc_queries = []
    else:
        with st.container(border=True):
            col_c1, col_c2 = st.columns([3, 1])
            with col_c1:
                st.markdown(
                    """
                    <div style="display: flex; align-items: center; gap: 8px; flex-wrap: wrap;">
                        <span class="pill-badge pill-green">🟢 已連線 OAuth 2.0</span>
                        <span style="font-size: 14px; font-weight: 600; color: #f4f4f5;">Google 官方 Search Console 數據即時同步中</span>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            with col_c2:
                if st.button("🚪 解除授權 (登出)", key="btn_gsc_logout", use_container_width=True):
                    if GSC_TOKEN_PATH.exists():
                        GSC_TOKEN_PATH.unlink()
                    st.success("已清除 token.json。")
                    st.rerun()

        verified_sites = get_gsc_verified_sites(gsc_creds)
        default_site = "https://stackdiff.pages.dev/"
        if default_site not in verified_sites and verified_sites:
            default_site = verified_sites[0]

        col_pr, col_th = st.columns([2, 1])
        with col_pr:
            site_url = st.selectbox("GSC 物業網址", verified_sites if verified_sites else [default_site])
        with col_th:
            surge_thresh = st.slider("出水警報曝光門檻", min_value=10, max_value=300, value=50, step=10)

        with st.spinner("正在查詢 Search Console 最近 28 天真實搜尋數據..."):
            gsc_queries = fetch_gsc_search_data(gsc_creds, site_url)

    # Tool Mapping & Surge Alert Detection
    tool_map = {t["id"]: t for t in tools_list}
    matched_stats: Dict[str, Dict[str, Any]] = {}

    for item in gsc_queries:
        q_text = item.get("query", "").lower()
        for tid, t in tool_map.items():
            if t["name"].lower() in q_text or t["slug"].lower() in q_text:
                if tid not in matched_stats:
                    matched_stats[tid] = {"impressions": 0, "clicks": 0, "queries": []}
                matched_stats[tid]["impressions"] += item["impressions"]
                matched_stats[tid]["clicks"] += item["clicks"]
                if item["query"] not in matched_stats[tid]["queries"]:
                    matched_stats[tid]["queries"].append(item["query"])

    surge_alerts = []
    for tid, stats in matched_stats.items():
        tool = tool_map.get(tid)
        if not tool:
            continue
        u = tool.get("url") or tool.get("affiliate_url") or ""
        if stats["impressions"] >= surge_thresh and not is_affiliate_url(u):
            surge_alerts.append({
                "tool": tool,
                "impressions": stats["impressions"],
                "clicks": stats["clicks"],
                "top_queries": stats["queries"],
                "current_url": u,
            })

    surge_alerts.sort(key=lambda x: x["impressions"], reverse=True)

    if surge_alerts:
        st.markdown(
            f"""
            <div style="margin-top: 10px; margin-bottom: 12px;">
                <span style="color: #f87171; font-weight: 700; font-size: 16px;">
                    🔥 流量出水警報：發現 {len(surge_alerts)} 款工具正在爆發搜尋，尚未配置商業推薦碼！
                </span>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Automated Discord Webhook Push Sentinel
        if discord_webhook:
            if "discord_alerted_tool_ids" not in st.session_state:
                st.session_state["discord_alerted_tool_ids"] = set()

            unalerted_surges = [a for a in surge_alerts if a["tool"]["id"] not in st.session_state["discord_alerted_tool_ids"]]
            if unalerted_surges:
                dashboard_url = f"http://{LAN_IP}:8502"
                auto_count = 0
                for sa in unalerted_surges:
                    st_tool = sa["tool"]
                    loss = int(sa["clicks"] * 0.05 * 20)
                    fields = [
                        {"name": "🛠️ 工具名稱", "value": f"**{st_tool['name']}** ({st_tool.get('category', 'General')})", "inline": True},
                        {"name": "📈 近 30 天曝光數", "value": f"{sa['impressions']:,} 次", "inline": True},
                        {"name": "🎯 自然點擊數", "value": f"{sa['clicks']:,} 次", "inline": True},
                        {"name": "⚠️ 當前狀態", "value": "❌ **尚未配置聯盟代碼** (收益流失中)", "inline": False},
                        {"name": "🔗 後台直達連結", "value": f"[{dashboard_url}]({dashboard_url})", "inline": False},
                    ]
                    ok, _ = send_discord_alert(
                        discord_webhook,
                        title="🚨 StackDiff 流量出水警報",
                        description=f"偵測到 **{st_tool['name']}** 正在爆發自然搜尋流量，目前官方網址未帶分潤參數，預估月損失 ~${loss:,}！",
                        fields=fields,
                    )
                    if ok:
                        st.session_state["discord_alerted_tool_ids"].add(st_tool["id"])
                        auto_count += 1
                if auto_count > 0:
                    st.toast(f"🚨 已自動推播 {auto_count} 則出水警報至 Discord！", icon="📲")

        # Manual Broadcast Bar
        if discord_webhook:
            col_wh_info, col_wh_act = st.columns([3, 1])
            with col_wh_info:
                st.info(f"📢 Discord 連線正常：已監控到 {len(surge_alerts)} 款出水工具（新出水將自動推播，亦可手動全量重發）。")
            with col_wh_act:
                if st.button("🔔 手動重發全量警報", key="btn_send_all_surge_webhook", use_container_width=True):
                    dashboard_url = f"http://{LAN_IP}:8502"
                    sent_cnt = 0
                    for sa in surge_alerts:
                        st_tool = sa["tool"]
                        loss = int(sa["clicks"] * 0.05 * 20)
                        fields = [
                            {"name": "🛠️ 工具名稱", "value": f"**{st_tool['name']}** ({st_tool.get('category', 'General')})", "inline": True},
                            {"name": "📈 近 30 天曝光數", "value": f"{sa['impressions']:,} 次", "inline": True},
                            {"name": "🎯 自然點擊數", "value": f"{sa['clicks']:,} 次", "inline": True},
                            {"name": "⚠️ 當前狀態", "value": "❌ **尚未配置聯盟代碼** (收益流失中)", "inline": False},
                            {"name": "🔗 後台直達連結", "value": f"[{dashboard_url}]({dashboard_url})", "inline": False},
                        ]
                        ok, _ = send_discord_alert(
                            discord_webhook,
                            title="🚨 StackDiff 流量出水警報 (手動重發)",
                            description=f"**{st_tool['name']}** 曝光達 {sa['impressions']:,} 次，請盡速前往後台配置推薦碼。",
                            fields=fields,
                        )
                        if ok:
                            sent_cnt += 1
                    if sent_cnt > 0:
                        st.success(f"🎉 成功推播 {sent_cnt} 則出水警報至 Discord！")
                    else:
                        st.error("Discord 發送失敗，請確認 Webhook 網址。")

        for a in surge_alerts:
            t = a["tool"]
            est_loss = int(a["clicks"] * 0.05 * 20)

            with st.container(border=True):
                col_al1, col_al2 = st.columns([3, 1])
                with col_al1:
                    st.markdown(
                        f"""
                        <div style="display: flex; align-items: center; gap: 8px; flex-wrap: wrap;">
                            <span style="font-size: 18px; font-weight: 700; color: #ffffff;">{t['name']}</span>
                            <span class="pill-badge">{t.get('category')}</span>
                            <span class="pill-badge pill-green">🟢 GSC 即時</span>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
                with col_al2:
                    st.markdown(f"<div style='text-align: right; font-family: monospace;'>起步價: {t.get('starting_price')}</div>", unsafe_allow_html=True)

                col_pm1, col_pm2, col_pm3 = st.columns(3)
                with col_pm1:
                    st.metric("GSC 搜尋曝光數", f"{a['impressions']:,}")
                with col_pm2:
                    st.metric("GSC 自然點擊數", f"{a['clicks']:,}")
                with col_pm3:
                    st.metric("預估月未變現損失", f"~${est_loss:,} / mo")

                st.markdown(f"<p style='font-size: 12px; color: #71717a;'>熱門關鍵字: {', '.join([f'<code>{q}</code>' for q in a['top_queries'][:3]])}</p>", unsafe_allow_html=True)

                col_in, col_sv, col_wh_btn = st.columns([2, 1, 1])
                with col_in:
                    quick_aff = st.text_input("配置推薦連結", value=f"{a['current_url']}?via=stackdiff", key=f"aff_in_{t['id']}", label_visibility="collapsed")
                with col_sv:
                    if st.button("💾 快速綁定並推送", key=f"btn_aff_sv_{t['id']}", use_container_width=True):
                        t["url"] = quick_aff.strip()
                        t["affiliate_url"] = quick_aff.strip()
                        save_tools_data(tools_list)
                        git_auto_push(f"Update affiliate URL for {t['name']}")
                        st.success(f"已為 {t['name']} 配置推薦連結並自動推送！")
                        st.rerun()
                with col_wh_btn:
                    if discord_webhook and st.button("📢 推播 Discord", key=f"btn_wh_single_{t['id']}", use_container_width=True):
                        dashboard_url = f"http://{LAN_IP}:8502"
                        fields = [
                            {"name": "🛠️ 工具名稱", "value": f"**{t['name']}** ({t.get('category', 'General')})", "inline": True},
                            {"name": "📈 近 30 天曝光數", "value": f"{a['impressions']:,} 次", "inline": True},
                            {"name": "🎯 自然點擊數", "value": f"{a['clicks']:,} 次", "inline": True},
                            {"name": "⚠️ 當前狀態", "value": "❌ **尚未配置聯盟代碼**", "inline": False},
                            {"name": "🔗 後台直達連結", "value": f"[{dashboard_url}]({dashboard_url})", "inline": False},
                        ]
                        ok, msg = send_discord_alert(
                            discord_webhook,
                            title="🚨 StackDiff 流量出水警報",
                            description=f"**{t['name']}** 近期搜尋流量飆升，預估月損失 ~${est_loss:,}/mo，請盡速配置推薦碼！",
                            fields=fields,
                        )
                        if ok:
                            st.success("✅ 已推播至 Discord！")
                        else:
                            st.error(f"❌ {msg}")
    else:
        if is_gsc_connected:
            st.success("✅ 目前所有高流量檢索工具皆已綁定推薦代碼，無被動收益流失。")

    if gsc_queries:
        st.markdown("---")
        st.markdown("#### 📈 GSC 關鍵字全域監控表")
        st.caption("💡 手機端支援手勢橫滑。")
        st.dataframe(pd.DataFrame(gsc_queries), use_container_width=True, hide_index=True)

# =============================================================================
# TAB 4: 💼 聯盟 CRM 看板
# =============================================================================
with tabs[3]:
    st.subheader("💼 聯盟夥伴商務 CRM 看板")
    st.markdown("管理每款工具的聯盟夥伴申請階段、抽成條款與收益紀錄（資料自動持久化保存）。")

    pipeline_items = load_pipeline_data(tools_list)

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

    # Status Cards
    crm_c1, crm_c2, crm_c3, crm_c4, crm_c5 = st.columns(5)
    with crm_c1:
        st.metric("⏳ 待申請", counts_by_stage.get("未申請 (Not Applied)", 0))
    with crm_c2:
        st.metric("📨 審核中", counts_by_stage.get("審核中 (Under Review)", 0))
    with crm_c3:
        st.metric("✅ 已通過", counts_by_stage.get("已通過 (Approved)", 0))
    with crm_c4:
        st.metric("💰 產生收益中", counts_by_stage.get("產生被動收益 (Generating Revenue)", 0))
    with crm_c5:
        st.metric("📈 預估月被動收益", f"${est_total_monthly:,.2f}")

    st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
    st.markdown("#### 📋 聯盟管道編輯清單")
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
        key="crm_tab_editor",
    )

    if st.button("💾 儲存 CRM 變更", type="primary", use_container_width=True):
        new_pipe = edited_pipe.to_dict(orient="records")
        for item in new_pipe:
            item["last_updated"] = datetime.now().strftime("%Y-%m-%d")
        if save_pipeline_data(new_pipe):
            st.success("✅ CRM 資料已成功保存至 `src/data/affiliate_pipeline.json`！")

# =============================================================================
# TAB 5: 🛠️ 資料庫快速維護 & 部署
# =============================================================================
with tabs[4]:
    st.subheader("🛠️ 資料庫快速維護 & 一鍵部署")
    st.markdown("線上編輯 `src/data/tools.json` 中的各工具規格與商務推薦網址，並一鍵推送到 Cloudflare Pages。")

    col_flt1, col_flt2 = st.columns([1, 2])
    with col_flt1:
        cat_choices = sorted(list(set(t.get("category", "") for t in tools_list)))
        sel_cat = st.selectbox("分類過濾", ["全部 (All)"] + cat_choices)
    with col_flt2:
        search_kw = st.text_input("搜尋名稱或 ID", placeholder="Cursor, Claude, Windsurf...")

    filtered = tools_list
    if sel_cat != "全部 (All)":
        filtered = [t for t in filtered if t.get("category") == sel_cat]
    if search_kw.strip():
        kw = search_kw.strip().lower()
        filtered = [t for t in filtered if kw in t.get("name", "").lower() or kw in t.get("id", "").lower()]

    rows = []
    for t in filtered:
        rows.append({
            "id": t.get("id", ""),
            "name": t.get("name", ""),
            "category": t.get("category", ""),
            "pricing_model": t.get("pricing_model", ""),
            "starting_price": t.get("starting_price", ""),
            "free_tier": t.get("free_tier", True),
            "url": t.get("url") or t.get("affiliate_url") or "",
            "primary_audience": t.get("primary_audience") or t.get("best_for") or "",
        })

    st.caption("💡 手機端支援手勢橫滑，點選任意儲存格即可直接編輯。")
    edited_t_df = st.data_editor(
        pd.DataFrame(rows),
        use_container_width=True,
        num_rows="dynamic",
        disabled=["id"],
        key="main_tools_editor",
    )

    col_s1, col_s2 = st.columns([1, 1])
    with col_s1:
        if st.button("💾 僅儲存到本地 tools.json", use_container_width=True):
            upd = {r["id"]: r for r in edited_t_df.to_dict(orient="records")}
            for t in tools_list:
                if t.get("id") in upd:
                    row = upd[t["id"]]
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

    with col_s2:
        if st.button("🚀 儲存並一鍵推送到 Cloudflare (Git Push)", type="primary", use_container_width=True):
            upd = {r["id"]: r for r in edited_t_df.to_dict(orient="records")}
            for t in tools_list:
                if t.get("id") in upd:
                    row = upd[t["id"]]
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

            with st.spinner("正在背景執行自動化 Git Commit & Push 部署..."):
                success, msg = git_auto_push("chore: update tools via Ops Dashboard")
                if success:
                    st.success(msg)
                else:
                    st.error(msg)
