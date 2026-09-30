#!/usr/bin/env python3
"""
scripts/calibrate_core_tools.py
Calibrates the 4 core tools (Cursor, Claude, GitHub Copilot, ChatGPT)
to Canonical ToolData Schema with exact pricing, models, and sources.
"""

import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
P_SRC = PROJECT_ROOT / "src" / "data" / "tools.json"
P_DATA = PROJECT_ROOT / "data" / "tools.json"

with open(P_SRC, "r", encoding="utf-8") as f:
    tools = json.load(f)

calibrations = {
    "cursor": {
        "official_website": "https://cursor.com",
        "official_pricing_url": "https://docs.cursor.com/getting-started/pricing",
        "source_url": "https://docs.cursor.com/getting-started/pricing",
        "last_checked_at": "2026-09-30",
        "pricing": {
            "starting_price": "$20/mo",
            "billing_model": "Seat-based",
            "free_tier_details": "Hobby plan: 14-day Pro trial, 50 slow premium requests/mo, 200 cursor-small requests",
            "tiers_summary": "Hobby Free / Pro $20 / Pro+ $60 / Ultra $200 / Usage Pools"
        },
        "technical_specs": {
            "current_models": [
                "Claude 3.5 Sonnet",
                "Claude 3.7 Sonnet",
                "GPT-4o",
                "OpenAI o1",
                "Grok-2",
                "Cursor Composer 2.5",
                "DeepSeek-V3"
            ],
            "context_window": "200K",
            "byok_support": True,
            "open_source": False,
            "telemetry_privacy": True,
            "offline_support": False
        },
        "gotchas": [
            "Pro plan includes 500 fast premium requests/mo; subsequent requests enter pool or incur optional $0.10/req usage fees.",
            "Requires running a standalone VS Code fork rather than a standard editor extension.",
            "BYOK usage bypasses fast request limits but incurs direct API billing from your model provider."
        ]
    },
    "github-copilot": {
        "official_website": "https://github.com/features/copilot",
        "official_pricing_url": "https://github.com/features/copilot#pricing",
        "source_url": "https://github.com/features/copilot#pricing",
        "last_checked_at": "2026-09-30",
        "pricing": {
            "starting_price": "$10/mo",
            "billing_model": "Seat-based",
            "free_tier_details": "Copilot Free: 2,000 code completions and 50 chat messages/mo in VS Code",
            "tiers_summary": "Free (Limited) / Individual $10/mo ($100/yr) / Business $19/user/mo / Enterprise $39/user/mo"
        },
        "technical_specs": {
            "current_models": [
                "Claude 3.5 Sonnet",
                "Claude 3.7 Sonnet",
                "GPT-4o",
                "OpenAI o1",
                "Gemini 2.0 Flash"
            ],
            "context_window": "128K",
            "byok_support": False,
            "open_source": False,
            "telemetry_privacy": True,
            "offline_support": False
        },
        "gotchas": [
            "Zero BYOK support; developers cannot connect external private API keys or unvetted local weights.",
            "Multi-file whole-codebase autonomous refactoring is significantly less integrated than dedicated agentic IDEs like Cursor.",
            "Copilot Free tier is limited to 50 chat prompts/mo and only operates within VS Code."
        ]
    },
    "claude-3-5-sonnet": {
        "official_website": "https://claude.ai",
        "official_pricing_url": "https://www.anthropic.com/pricing",
        "source_url": "https://www.anthropic.com/pricing",
        "last_checked_at": "2026-09-30",
        "pricing": {
            "starting_price": "$20/mo",
            "billing_model": "Seat-based",
            "free_tier_details": "Daily free message allowance subject to dynamic server capacity limits",
            "tiers_summary": "Free / Pro $20/mo / Team $25/user/mo (min 5 seats) / Enterprise"
        },
        "technical_specs": {
            "current_models": [
                "Claude 3.5 Sonnet",
                "Claude 3.7 Sonnet",
                "Claude Sonnet 5.5",
                "Claude 3.5 Haiku",
                "Claude 3 Opus"
            ],
            "context_window": "200K",
            "byok_support": True,
            "open_source": False,
            "telemetry_privacy": True,
            "offline_support": False
        },
        "gotchas": [
            "Pro subscription enforces rolling 5-hour message limits that throttle dynamically during peak global usage.",
            "Does not offer native sandboxed Python terminal execution or image generation in the standard chat UI.",
            "Team plan requires a minimum commitment of 5 seats ($125/mo)."
        ]
    },
    "chatgpt": {
        "official_website": "https://chatgpt.com",
        "official_pricing_url": "https://openai.com/chatgpt/pricing",
        "source_url": "https://openai.com/chatgpt/pricing",
        "last_checked_at": "2026-09-30",
        "pricing": {
            "starting_price": "$20/mo",
            "billing_model": "Seat-based",
            "free_tier_details": "Free tier includes GPT-4o mini with limited access to GPT-4o and web browsing",
            "tiers_summary": "Free / Plus $20/mo / Pro $200/mo / Team $25/user/mo (min 2 seats) / Enterprise"
        },
        "technical_specs": {
            "current_models": [
                "GPT-4o",
                "GPT-4o mini",
                "OpenAI o1",
                "OpenAI o3-mini",
                "Sora Video (Pro)"
            ],
            "context_window": "128K",
            "byok_support": False,
            "open_source": False,
            "telemetry_privacy": True,
            "offline_support": False
        },
        "gotchas": [
            "Plus ($20/mo) has dynamic usage caps on OpenAI o1 reasoning model; heavy researchers require Pro ($200/mo) for unlimited reasoning.",
            "Web client and mobile app do not support BYOK (must use separate OpenAI Developer Platform API billing).",
            "Team plan requires minimum 2 seats billed annually or monthly."
        ]
    }
}

for tool in tools:
    slug = tool.get("slug")
    if slug in calibrations:
        tool.update(calibrations[slug])
        tool["starting_price"] = calibrations[slug]["pricing"]["starting_price"]
        tool["pricing_model"] = calibrations[slug]["pricing"]["billing_model"]
        tool["free_tier"] = "Free" in calibrations[slug]["pricing"]["tiers_summary"]

for path in [P_SRC, P_DATA]:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(tools, f, indent=2, ensure_ascii=False)
    print(f"Successfully calibrated {path}")

print("Core tools calibration complete!")
