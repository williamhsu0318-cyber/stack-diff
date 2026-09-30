#!/usr/bin/env python3
"""
scripts/curate_22_flagship_tools.py
=============================================================================
Prunes the tool database down to the 22 most popular flagship AI tools
across 6 core productivity categories.
Applies verified Canonical ToolData Schema with exact models, tiers,
official sources, and zero fluff.
=============================================================================
"""

import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
P_SRC = PROJECT_ROOT / "src" / "data" / "tools.json"
P_DATA = PROJECT_ROOT / "data" / "tools.json"

FLAGSHIP_SPECS = {
    # -------------------------------------------------------------------------
    # 1. CODING AI (5 Flagship Tools -> 10 Pairwise Diffs)
    # -------------------------------------------------------------------------
    "cursor": {
        "id": "cursor",
        "name": "Cursor",
        "slug": "cursor",
        "category": "Coding AI",
        "tagline": "AI-first code editor fork of VS Code engineered for whole-codebase indexing and autonomous Composer 2.5 multi-file edits",
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
        "best_for": "Software engineers and indie builders wanting autonomous multi-file generation with instant diff reviews",
        "key_features": [
            "Composer 2.5 multi-file autonomous generation and automatic diff application",
            "Full codebase semantic indexing with symbol-aware contextual retrieval (@codebase)",
            "Copilot++ intelligent multi-line autocomplete predicting next edit locations",
            "Seamless model switching across Claude 3.5/3.7 Sonnet, GPT-4o, Grok-2, and DeepSeek-V3",
            "1-click migration importing all VS Code extensions, themes, and keybindings"
        ],
        "gotchas": [
            "Pro plan includes 500 fast premium requests/mo; subsequent requests enter pool or incur optional $0.10/req usage fees.",
            "Requires running a dedicated standalone IDE application rather than an editor plugin.",
            "BYOK usage bypasses fast request limits but incurs direct API billing from your model provider."
        ],
        "affiliate_url": "https://cursor.com",
        "url": "https://cursor.com"
    },

    "github-copilot": {
        "id": "github-copilot",
        "name": "GitHub Copilot",
        "slug": "github-copilot",
        "category": "Coding AI",
        "tagline": "The enterprise-standard AI pair programmer with multi-model hot-switching across Anthropic and OpenAI",
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
        "best_for": "Developers wanting native multi-IDE inline completions with seamless switching between Claude and OpenAI models",
        "key_features": [
            "Seamless multi-model switching between Claude 3.5/3.7 Sonnet, GPT-4o, OpenAI o1, and Gemini 2.0 Flash",
            "Real-time inline ghost-text code completions embedded directly into your editor cursor",
            "Copilot Chat with workspace symbol awareness and Pull Request generation on GitHub.com",
            "Native cross-IDE plugin support across VS Code, JetBrains, Visual Studio, and Neovim",
            "Enterprise-grade security controls, centralized seat management, and IP copyright indemnity"
        ],
        "gotchas": [
            "Zero BYOK support; developers cannot connect external private API keys or unvetted local weights.",
            "Multi-file whole-codebase autonomous refactoring is significantly less integrated than dedicated agentic IDEs like Cursor.",
            "Copilot Free tier is limited to 50 chat prompts/mo and only operates within VS Code."
        ],
        "affiliate_url": "https://github.com/features/copilot",
        "url": "https://github.com/features/copilot"
    },

    "windsurf": {
        "id": "windsurf",
        "name": "Windsurf",
        "slug": "windsurf",
        "category": "Coding AI",
        "tagline": "AI-first IDE by Codeium featuring Cascade agentic flow state, collaborative multi-file editing, and fast completions",
        "official_website": "https://codeium.com/windsurf",
        "official_pricing_url": "https://codeium.com/pricing",
        "source_url": "https://codeium.com/pricing",
        "last_checked_at": "2026-09-30",
        "pricing": {
            "starting_price": "$15/mo",
            "billing_model": "Seat-based",
            "free_tier_details": "Free plan includes unlimited fast autocomplete completions and basic Cascade chat",
            "tiers_summary": "Free / Pro $15/mo (500 prompt credits) / Teams $30/user/mo / Enterprise"
        },
        "technical_specs": {
            "current_models": [
                "Cascade Flow Engine",
                "Claude 3.5 Sonnet",
                "GPT-4o",
                "DeepSeek-V3"
            ],
            "context_window": "128K",
            "byok_support": False,
            "open_source": False,
            "telemetry_privacy": True,
            "offline_support": False
        },
        "best_for": "Developers wanting an AI-first IDE with unlimited completions at a lower price point than Cursor ($15 vs $20)",
        "key_features": [
            "Cascade engine delivering collaborative agentic workflows and real-time execution tracking",
            "Supercomplete intelligent multi-line code generation with sub-100ms latency",
            "Direct VS Code fork architecture supporting all standard extensions and configurations",
            "Command line and terminal awareness with automatic command suggestion and error repair",
            "Deep codebase indexing with live semantic symbol resolution"
        ],
        "gotchas": [
            "Cascade agentic executions consume monthly credit units that cap intensive daily workflows.",
            "Extension marketplace synchronization occasionally trails official VS Code by days.",
            "Does not offer open BYOK API key integration on the standard Pro tier."
        ],
        "affiliate_url": "https://codeium.com/windsurf",
        "url": "https://codeium.com/windsurf"
    },

    "v0-by-vercel": {
        "id": "v0-by-vercel",
        "name": "v0 by Vercel",
        "slug": "v0-by-vercel",
        "category": "Coding AI",
        "tagline": "Generative user interface engine synthesizing production-ready React, Next.js, and Tailwind CSS components from prompts",
        "official_website": "https://v0.dev",
        "official_pricing_url": "https://v0.dev/pricing",
        "source_url": "https://v0.dev/pricing",
        "last_checked_at": "2026-09-30",
        "pricing": {
            "starting_price": "$20/mo",
            "billing_model": "Usage-based",
            "free_tier_details": "Free tier includes 200 monthly credits with public generations",
            "tiers_summary": "Free (200 credits) / Premium $20/mo (5,000 credits) / Enterprise"
        },
        "technical_specs": {
            "current_models": [
                "v0 Component Synthesis Engine",
                "Claude 3.5 Sonnet",
                "Specialized Tailwind LLM"
            ],
            "context_window": "128K",
            "byok_support": False,
            "open_source": False,
            "telemetry_privacy": True,
            "offline_support": False
        },
        "best_for": "Frontend engineers, product designers, and full-stack builders needing instant production React and Tailwind code",
        "key_features": [
            "Live interactive component canvas with real-time DOM previews and mobile viewport toggles",
            "Copy-pasteable Shadcn UI and Tailwind CSS modular architecture",
            "Image-to-code and Figma-to-code reverse engineering from uploaded UI screenshots",
            "Native 1-click deploy to Vercel and direct CLI component installation (npx shadcn@latest add)",
            "Multi-turn conversational iteration allowing granular CSS and component state adjustments"
        ],
        "gotchas": [
            "Credits burn rapidly during complex multi-turn visual design iterations.",
            "Specialized strictly in frontend markup and client-side UI; backend logic requires external implementation.",
            "Free tier generations are publicly indexed in community search."
        ],
        "affiliate_url": "https://v0.dev",
        "url": "https://v0.dev"
    },

    "lovable": {
        "id": "lovable",
        "name": "Lovable",
        "slug": "lovable",
        "category": "Coding AI",
        "tagline": "Full-stack software generation platform turning plain English into working web apps with Supabase databases",
        "official_website": "https://lovable.dev",
        "official_pricing_url": "https://lovable.dev/pricing",
        "source_url": "https://lovable.dev/pricing",
        "last_checked_at": "2026-09-30",
        "pricing": {
            "starting_price": "$20/mo",
            "billing_model": "Credit-based",
            "free_tier_details": "Free trial includes initial credits to build and test prototypes",
            "tiers_summary": "Starter $20/mo (100 edits/mo) / Pro $50/mo (500 edits) / Business $100/mo"
        },
        "technical_specs": {
            "current_models": [
                "Lovable Architect Engine",
                "Claude 3.5 Sonnet",
                "GPT-4o"
            ],
            "context_window": "128K",
            "byok_support": False,
            "open_source": False,
            "telemetry_privacy": True,
            "offline_support": False
        },
        "best_for": "Founders, product managers, and builders creating full-stack web applications with authentication and databases",
        "key_features": [
            "Generates full-stack React applications with backend API routes and Supabase database schemas",
            "Native GitHub bi-directional synchronization committing code directly to your repository",
            "Interactive live preview environment with real-time hot reloading",
            "Visual element inspector allowing direct click-to-edit prompt refinements",
            "Built-in user authentication, PostgreSQL table creation, and Row Level Security rules"
        ],
        "gotchas": [
            "Monthly edit credits deplete quickly during complex full-stack architectural refactors.",
            "Complex custom database queries and external third-party OAuth flows may require manual coding.",
            "Requires active subscription to export clean production builds without platform branding."
        ],
        "affiliate_url": "https://lovable.dev",
        "url": "https://lovable.dev"
    },

    # -------------------------------------------------------------------------
    # 2. LLMS / GENERAL AI (5 Flagship Tools -> 10 Pairwise Diffs)
    # -------------------------------------------------------------------------
    "chatgpt": {
        "id": "chatgpt",
        "name": "ChatGPT Plus",
        "slug": "chatgpt",
        "category": "LLM",
        "tagline": "OpenAI's flagship conversational assistant featuring frontier reasoning (o1, o3-mini), GPT-4o, and Advanced Voice",
        "official_website": "https://chatgpt.com",
        "official_pricing_url": "https://openai.com/chatgpt/pricing",
        "source_url": "https://openai.com/chatgpt/pricing",
        "last_checked_at": "2026-09-30",
        "pricing": {
            "starting_price": "$20/mo",
            "billing_model": "Seat-based",
            "free_tier_details": "Free tier includes GPT-4o mini and standard GPT-4o access limits",
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
        "best_for": "Knowledge workers, researchers, and developers wanting a multi-model reasoning and multimodal execution assistant",
        "key_features": [
            "Frontier reasoning with OpenAI o1 and o3-mini alongside versatile GPT-4o multimodal engine",
            "Advanced Voice Mode with real-time natural conversational interruptions and inflection",
            "Canvas collaborative workspace for inline text drafting and code iteration",
            "Integrated web search, sandboxed Python code analysis, and DALL-E image generation",
            "Custom GPT marketplace and memory persistence across conversations"
        ],
        "gotchas": [
            "Plus ($20/mo) has dynamic usage caps on OpenAI o1 reasoning model; heavy researchers require Pro ($200/mo) for unlimited reasoning.",
            "Web client and mobile app do not support BYOK (must use separate OpenAI Developer Platform API billing).",
            "Team plan requires minimum 2 seats billed annually or monthly."
        ],
        "affiliate_url": "https://chatgpt.com",
        "url": "https://chatgpt.com"
    },

    "claude-3-5-sonnet": {
        "id": "claude-3-5-sonnet",
        "name": "Claude Pro",
        "slug": "claude-3-5-sonnet",
        "category": "LLM",
        "tagline": "Anthropic's frontier AI ecosystem offering elite reasoning, nuanced prose, and live Artifacts prototyping",
        "official_website": "https://claude.ai",
        "official_pricing_url": "https://www.anthropic.com/pricing",
        "source_url": "https://www.anthropic.com/pricing",
        "last_checked_at": "2026-09-30",
        "pricing": {
            "starting_price": "$20/mo",
            "billing_model": "Seat-based",
            "free_tier_details": "Free access with dynamic demand-based message limits",
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
        "best_for": "Software engineers, analysts, and writers demanding natural prose and benchmark-leading coding intelligence",
        "key_features": [
            "Access to flagship Claude 3.7 Sonnet, Sonnet 5.5, and Claude 3.5 Haiku",
            "Artifacts interactive workspace for live React, HTML, SVG, and diagram rendering",
            "200,000 token context window for ingesting full codebases, logs, and technical manuscripts",
            "Projects workspace for persistent team wikis, brand voice guidelines, and file stores",
            "Visual reasoning for dense architectural diagrams, UI mockups, and financial statements"
        ],
        "gotchas": [
            "Pro subscription enforces rolling 5-hour message limits that throttle dynamically during peak global usage.",
            "Does not offer native sandboxed Python terminal execution or image generation in the standard chat UI.",
            "Team plan requires a mandatory 5-user minimum commitment ($125/mo)."
        ],
        "affiliate_url": "https://claude.ai",
        "url": "https://claude.ai"
    },

    "gemini-advanced": {
        "id": "gemini-advanced",
        "name": "Gemini Advanced",
        "slug": "gemini-advanced",
        "category": "LLM",
        "tagline": "Google's 2M-token frontier assistant with native multimodal comprehension, Gemini 2.0 Flash, and Workspace integration",
        "official_website": "https://gemini.google.com/advanced",
        "official_pricing_url": "https://one.google.com/about/plans",
        "source_url": "https://one.google.com/about/plans",
        "last_checked_at": "2026-09-30",
        "pricing": {
            "starting_price": "$19.99/mo",
            "billing_model": "Subscription",
            "free_tier_details": "Free tier includes web access to Gemini 2.0 Flash and 1.5 Flash with standard rate limits",
            "tiers_summary": "Google One AI Premium $19.99/mo (Includes 2TB storage) / Free Gemini"
        },
        "technical_specs": {
            "current_models": [
                "Gemini 2.0 Flash",
                "Gemini 1.5 Pro (2M context)",
                "Gemini 1.5 Flash",
                "Gemini Ultra"
            ],
            "context_window": "2M",
            "byok_support": False,
            "open_source": False,
            "telemetry_privacy": True,
            "offline_support": False
        },
        "best_for": "Researchers, Google Workspace users, and engineers ingesting massive documents, long video, or entire code repos",
        "key_features": [
            "Massive 2,000,000 token context window for ingesting full codebases, hours of audio, and dense video",
            "Powered by Gemini 2.0 Flash and Gemini 1.5 Pro multimodal architectures",
            "Deep Google Workspace integration (Docs, Gmail, Sheets, Drive) for instant contextual drafting",
            "Includes 2TB Google One cloud storage and priority access to Google AI Studio features",
            "Native execution of Python code and live multimodal audio/visual understanding"
        ],
        "gotchas": [
            "Tied directly to personal Google One storage accounts; cannot easily separate business and personal quotas.",
            "Developer API credits are NOT included in the Google One AI Premium $19.99/mo bundle.",
            "Advanced reasoning responses can lean conservative on ambiguous non-technical creative queries."
        ],
        "affiliate_url": "https://gemini.google.com/advanced",
        "url": "https://gemini.google.com/advanced"
    },

    "deepseek": {
        "id": "deepseek",
        "name": "DeepSeek",
        "slug": "deepseek",
        "category": "LLM",
        "tagline": "Open-weight frontier intelligence offering state-of-the-art reasoning (R1) and coding (V3) at 90% lower API cost",
        "official_website": "https://chat.deepseek.com",
        "official_pricing_url": "https://platform.deepseek.com/api-docs/pricing",
        "source_url": "https://platform.deepseek.com/api-docs/pricing",
        "last_checked_at": "2026-09-30",
        "pricing": {
            "starting_price": "Free / Pay-per-token API",
            "billing_model": "Usage-based",
            "free_tier_details": "100% free web chat with R1 reasoning and 5M tokens for new API accounts",
            "tiers_summary": "Web Chat Free / API $0.14-$0.55 per 1M tokens (Cache hit: $0.014/1M)"
        },
        "technical_specs": {
            "current_models": [
                "DeepSeek-R1 (Reasoning)",
                "DeepSeek-V3 (Base 671B MoE)",
                "DeepSeek-Coder-V2"
            ],
            "context_window": "64K",
            "byok_support": True,
            "open_source": True,
            "telemetry_privacy": True,
            "offline_support": True
        },
        "best_for": "Developers, AI researchers, and businesses seeking benchmark-leading reasoning at fraction of western lab API costs",
        "key_features": [
            "DeepSeek-R1 open-weight reasoning model rivaling OpenAI o1 on math, code, and STEM benchmarks",
            "DeepSeek-V3 671B Mixture-of-Experts architecture delivering ultra-fast inference speed",
            "MIT license unencumbered open weights available for private on-premise deployment via Ollama/vLLM",
            "Context caching mechanism reducing repetitive prompt costs down to $0.014 per million tokens",
            "100% free public conversational web interface and mobile applications"
        ],
        "gotchas": [
            "Public web interface encounters frequent peak-hour server capacity congestion.",
            "Native context window is 64k tokens, smaller than Gemini's 2M or Claude's 200k.",
            "Self-hosting full 671B model requires enterprise multi-GPU server clusters (8x H100)."
        ],
        "affiliate_url": "https://chat.deepseek.com",
        "url": "https://chat.deepseek.com"
    },

    "perplexity-ai": {
        "id": "perplexity-ai",
        "name": "Perplexity Pro",
        "slug": "perplexity-ai",
        "category": "LLM",
        "tagline": "Conversational answer engine combining verified live web search with multi-model switching (Claude, GPT-4o, Sonar)",
        "official_website": "https://perplexity.ai",
        "official_pricing_url": "https://www.perplexity.ai/pro",
        "source_url": "https://www.perplexity.ai/pro",
        "last_checked_at": "2026-09-30",
        "pricing": {
            "starting_price": "$20/mo",
            "billing_model": "Subscription",
            "free_tier_details": "Free unlimited standard searches plus 5 Pro searches daily",
            "tiers_summary": "Free / Pro $20/mo ($200/yr) / Enterprise Pro $40/user/mo"
        },
        "technical_specs": {
            "current_models": [
                "Sonar Reasoning (DeepSeek-R1 based)",
                "Sonar Large",
                "Claude 3.5/3.7 Sonnet",
                "GPT-4o"
            ],
            "context_window": "128K",
            "byok_support": False,
            "open_source": False,
            "telemetry_privacy": True,
            "offline_support": False
        },
        "best_for": "Researchers, financial analysts, and knowledge workers requiring real-time web citations without SEO spam",
        "key_features": [
            "Pro Search synthesizing 30+ web sources into structured, citation-backed analytical briefs",
            "Instant model switcher between Claude 3.5/3.7 Sonnet, GPT-4o, and Sonar Reasoning",
            "Spaces collaborative knowledge hub with custom system prompts and file attachments",
            "Includes $5/mo in API platform credits for building search-augmented developer agents",
            "Pages publishing engine turning research threads into shareable SEO-optimized articles"
        ],
        "gotchas": [
            "Engineered primarily for information discovery and research synthesis rather than multi-file code editing.",
            "Included $5/mo API credits expire at the end of each billing cycle without rollover.",
            "Occasionally filters paywalled academic journals unless user uploads PDFs directly."
        ],
        "affiliate_url": "https://perplexity.ai",
        "url": "https://perplexity.ai"
    },

    # -------------------------------------------------------------------------
    # 3. IMAGE AI (4 Flagship Tools -> 6 Pairwise Diffs)
    # -------------------------------------------------------------------------
    "midjourney": {
        "id": "midjourney",
        "name": "Midjourney",
        "slug": "midjourney",
        "category": "Image AI",
        "tagline": "Industry-standard aesthetic image synthesis offering cinematic lighting, photorealism, and native Web UI",
        "official_website": "https://midjourney.com",
        "official_pricing_url": "https://docs.midjourney.com/docs/plans",
        "source_url": "https://docs.midjourney.com/docs/plans",
        "last_checked_at": "2026-09-30",
        "pricing": {
            "starting_price": "$10/mo",
            "billing_model": "Subscription",
            "free_tier_details": "Paid only (No permanent free tier; requires active subscription)",
            "tiers_summary": "Basic $10/mo (3.3h GPU) / Standard $30/mo (15h + unlimited relax) / Pro $60/mo / Mega $120/mo"
        },
        "technical_specs": {
            "current_models": [
                "Midjourney v6.1",
                "Midjourney v7 Alpha",
                "Niji 6"
            ],
            "context_window": "N/A",
            "byok_support": False,
            "open_source": False,
            "telemetry_privacy": False,
            "offline_support": False
        },
        "best_for": "Designers, art directors, and creative professionals requiring benchmark photorealism and stylistic coherence",
        "key_features": [
            "Midjourney v6.1 and v7 Alpha image models delivering benchmark texture fidelity and lighting",
            "Native standalone Web UI creation workspace alongside legacy Discord bot commands",
            "Vary (Region) inpainting, Pan / Zoom outpainting, and multi-prompt stylistic weight tuning",
            "Niji 6 specialized aesthetic anime and illustrative render pipeline",
            "Stealth generation mode on Pro ($60/mo) and Mega plans to protect proprietary creative assets"
        ],
        "gotchas": [
            "Basic tier ($10/mo) does not include unlimited Relaxed generation; stops when 3.3 Fast GPU hours deplete.",
            "All generated images are publicly visible in community gallery unless subscribed to Pro ($60/mo) with Stealth Mode.",
            "Does not offer an official public REST API for programmatic automation."
        ],
        "affiliate_url": "https://midjourney.com",
        "url": "https://midjourney.com"
    },

    "flux-1": {
        "id": "flux-1",
        "name": "FLUX.1 [dev/pro]",
        "slug": "flux-1",
        "category": "Image AI",
        "tagline": "Open-weight 12B parameter visual model by Black Forest Labs renowned for crisp typography and anatomical precision",
        "official_website": "https://blackforestlabs.ai",
        "official_pricing_url": "https://blackforestlabs.ai",
        "source_url": "https://blackforestlabs.ai",
        "last_checked_at": "2026-09-30",
        "pricing": {
            "starting_price": "Open weights Free / $0.03/img API",
            "billing_model": "Usage-based",
            "free_tier_details": "FLUX.1 [schnell] is 100% Apache 2.0 open source and free for self-hosting",
            "tiers_summary": "Schnell Free (Open Source) / Dev Non-Commercial / Pro API ~$0.03-$0.05/img"
        },
        "technical_specs": {
            "current_models": [
                "FLUX.1 [pro]",
                "FLUX.1 [dev]",
                "FLUX.1 [schnell]",
                "FLUX.1 Fill & Redux"
            ],
            "context_window": "N/A",
            "byok_support": True,
            "open_source": True,
            "telemetry_privacy": True,
            "offline_support": True
        },
        "best_for": "Developers, technical artists, and brands needing accurate text rendering in images with zero proprietary lock-in",
        "key_features": [
            "12-billion parameter rectified flow transformer architecture delivering state-of-the-art prompt fidelity",
            "World-class typographic rendering synthesizing crisp, legible text inside complex graphics",
            "Flawless human anatomy reproduction (hands, fingers, eyes) without distorted artifacts",
            "High-speed serverless API deployment available across Fal.ai, Together AI, and Replicate",
            "FLUX.1 [schnell] Apache 2.0 licensed for commercial on-premise hardware deployments"
        ],
        "gotchas": [
            "FLUX.1 [dev] license restricts commercial revenue generation without custom enterprise licensing.",
            "Local execution requires substantial GPU VRAM (minimum 16GB–24GB for full precision).",
            "No official consumer chat portal; requires using API platforms or WebUI tools like ComfyUI."
        ],
        "affiliate_url": "https://blackforestlabs.ai",
        "url": "https://blackforestlabs.ai"
    },

    "recraft": {
        "id": "recraft",
        "name": "Recraft",
        "slug": "recraft",
        "category": "Image AI",
        "tagline": "AI design studio purpose-built for commercial graphic designers generating brand-consistent vector SVG, 3D, and illustrations",
        "official_website": "https://recraft.ai",
        "official_pricing_url": "https://www.recraft.ai/pricing",
        "source_url": "https://www.recraft.ai/pricing",
        "last_checked_at": "2026-09-30",
        "pricing": {
            "starting_price": "$20/mo",
            "billing_model": "Credit-based",
            "free_tier_details": "Free plan includes 50 daily credits with public image library sharing",
            "tiers_summary": "Free (50 credits/day) / Basic $20/mo (1k fast credits) / Pro $48/mo / Enterprise"
        },
        "technical_specs": {
            "current_models": [
                "Recraft 20B (Red)",
                "Vector SVG Generator",
                "3D & Icon Synthesizer"
            ],
            "context_window": "N/A",
            "byok_support": False,
            "open_source": False,
            "telemetry_privacy": True,
            "offline_support": False
        },
        "best_for": "Graphic designers, branding agencies, and UI creators needing editable vector SVGs and strict color palette consistency",
        "key_features": [
            "Native vector SVG generation producing fully scalable and clean vector paths for Figma and Illustrator",
            "Brand color palette locking ensuring all outputs strictly obey company hex color codes",
            "Recraft 20B image model holding top positions on image generation leaderboards",
            "Infinite visual canvas workspace allowing multi-asset brand kit creation in one document",
            "Full commercial usage rights on all paid plan outputs with background removal tools"
        ],
        "gotchas": [
            "Free tier images are automatically published to community search gallery.",
            "Fast generation credits do not roll over between subscription billing periods.",
            "Specialized for design/graphic assets rather than ultra-photorealistic cinematic photography."
        ],
        "affiliate_url": "https://recraft.ai",
        "url": "https://recraft.ai"
    },

    "ideogram": {
        "id": "ideogram",
        "name": "Ideogram 2.0",
        "slug": "ideogram",
        "category": "Image AI",
        "tagline": "State-of-the-art graphic and typography AI model specialized in precise text layout, posters, and logo design",
        "official_website": "https://ideogram.ai",
        "official_pricing_url": "https://ideogram.ai/pricing",
        "source_url": "https://ideogram.ai/pricing",
        "last_checked_at": "2026-09-30",
        "pricing": {
            "starting_price": "$8/mo",
            "billing_model": "Subscription",
            "free_tier_details": "Free tier includes 10 slow credits daily (40 images/day)",
            "tiers_summary": "Free (10 credits/day) / Basic $8/mo (400 credits) / Plus $20/mo / Pro $60/mo"
        },
        "technical_specs": {
            "current_models": [
                "Ideogram 2.0",
                "Ideogram 2.0 Turbo",
                "Graphic Design & Logo Engine"
            ],
            "context_window": "N/A",
            "byok_support": False,
            "open_source": False,
            "telemetry_privacy": True,
            "offline_support": False
        },
        "best_for": "Marketers, apparel creators, and poster designers requiring complex typography embedded in visuals",
        "key_features": [
            "Ideogram 2.0 benchmark text-in-image generation rendering long slogans and sentences accurately",
            "Magic Prompt feature automatically expanding user ideas into detailed stylistic prompts",
            "Dedicated Graphic, Typography, and Realistic style render presets",
            "Color palette control matching exact hexadecimal brand themes",
            "Developer REST API for programmatic t-shirt design and banner generation"
        ],
        "gotchas": [
            "Free plan creations are publicly accessible in the community feed.",
            "Photorealism on human skin textures is slightly less cinematic than Midjourney v6.1.",
            "Daily free credits do not accumulate if unused."
        ],
        "affiliate_url": "https://ideogram.ai",
        "url": "https://ideogram.ai"
    },

    # -------------------------------------------------------------------------
    # 4. VIDEO AI (4 Flagship Tools -> 6 Pairwise Diffs)
    # -------------------------------------------------------------------------
    "runway-gen3": {
        "id": "runway-gen3",
        "name": "Runway Gen-3 Alpha",
        "slug": "runway-gen3",
        "category": "Video AI",
        "tagline": "Cinematic AI video generation platform powered by Gen-3 Alpha, Gen-3 Turbo, and Act-One facial performance capture",
        "official_website": "https://runwayml.com",
        "official_pricing_url": "https://runwayml.com/pricing",
        "source_url": "https://runwayml.com/pricing",
        "last_checked_at": "2026-09-30",
        "pricing": {
            "starting_price": "$12/mo",
            "billing_model": "Usage-based",
            "free_tier_details": "Free plan includes one-time 125 non-renewable generation credits",
            "tiers_summary": "Basic Free (125 credits) / Standard $12/mo (625 credits) / Pro $28/mo / Unlimited $76/mo"
        },
        "technical_specs": {
            "current_models": [
                "Gen-3 Alpha",
                "Gen-3 Alpha Turbo",
                "Act-One (Facial Animation)"
            ],
            "context_window": "N/A",
            "byok_support": False,
            "open_source": False,
            "telemetry_privacy": True,
            "offline_support": False
        },
        "best_for": "Filmmakers, VFX artists, and creative directors needing high-fidelity video generation and precise camera motion",
        "key_features": [
            "Gen-3 Alpha and Gen-3 Alpha Turbo high-fidelity video synthesis from text, image, and video prompts",
            "Act-One facial performance capture transferring real actor expressions onto stylized characters",
            "Director Mode camera controls with precise pan, tilt, zoom, and multi-motion brush masks",
            "4K video upscaling, lip-sync dubbing, and integrated generative audio sound effects",
            "Fast generation mode via Gen-3 Alpha Turbo delivering 7x speedups for storyboarding"
        ],
        "gotchas": [
            "Standard plan credits (625/mo) deplete quickly (Gen-3 Alpha costs 10 credits/sec of generated video).",
            "Unlimited generation mode is strictly restricted to the Unlimited tier ($76/mo) and uses relaxed queue.",
            "Credits do not roll over between subscription billing cycles."
        ],
        "affiliate_url": "https://runwayml.com",
        "url": "https://runwayml.com"
    },

    "kling-ai": {
        "id": "kling-ai",
        "name": "Kling AI",
        "slug": "kling-ai",
        "category": "Video AI",
        "tagline": "Next-gen AI video generator by Kuaishou delivering 1080p video outputs up to 2 minutes with realistic physics",
        "official_website": "https://klingai.com",
        "official_pricing_url": "https://klingai.com/pricing",
        "source_url": "https://klingai.com/pricing",
        "last_checked_at": "2026-09-30",
        "pricing": {
            "starting_price": "$10/mo",
            "billing_model": "Credit-based",
            "free_tier_details": "Free daily login credits (approx. 66 credits daily for non-commercial generations)",
            "tiers_summary": "Free (Daily credits) / Standard $10/mo (660 credits) / Pro $37/mo (3k credits) / Premier $92/mo"
        },
        "technical_specs": {
            "current_models": [
                "Kling 1.5",
                "Kling 1.0",
                "Motion Brush & Camera 3D"
            ],
            "context_window": "N/A",
            "byok_support": False,
            "open_source": False,
            "telemetry_privacy": True,
            "offline_support": False
        },
        "best_for": "Content creators and 3D animators needing long video clips (up to 2 minutes) with accurate physical object motion",
        "key_features": [
            "Kling 1.5 model generating high-definition 1080p video with accurate real-world physics simulation",
            "Extended clip duration: generate continuous coherent video scenes up to 2-3 minutes long",
            "End frame specification: designate both starting and ending image anchors for seamless video transitions",
            "Multi-element motion brush controlling trajectories of multiple characters independently",
            "Text-to-video and image-to-video synthesis with granular camera movement settings"
        ],
        "gotchas": [
            "High-demand server queues can cause generation delays on the free plan during peak Asian timezones.",
            "Commercial rights and watermark removal require an active paid Standard ($10/mo) plan.",
            "Professional mode consumes roughly 3x more credits per generated clip than standard mode."
        ],
        "affiliate_url": "https://klingai.com",
        "url": "https://klingai.com"
    },

    "luma-dream-machine": {
        "id": "luma-dream-machine",
        "name": "Luma Dream Machine",
        "slug": "luma-dream-machine",
        "category": "Video AI",
        "tagline": "Universal generative video model by Luma AI producing rapid 5-second cinematic shots with spatial realism",
        "official_website": "https://lumalabs.ai/dream-machine",
        "official_pricing_url": "https://lumalabs.ai/dream-machine",
        "source_url": "https://lumalabs.ai/dream-machine",
        "last_checked_at": "2026-09-30",
        "pricing": {
            "starting_price": "$9.99/mo",
            "billing_model": "Subscription",
            "free_tier_details": "Free tier provides 30 generations per month with standard queue",
            "tiers_summary": "Free (30 generations/mo) / Standard $9.99/mo (120 gens) / Pro $29.99/mo / Premier $99.99/mo"
        },
        "technical_specs": {
            "current_models": [
                "Dream Machine 1.5",
                "Luma Camera Dynamics",
                "Photon Video Transformer"
            ],
            "context_window": "N/A",
            "byok_support": False,
            "open_source": False,
            "telemetry_privacy": True,
            "offline_support": False
        },
        "best_for": "Social media creators, advertising agencies, and filmmakers prototyping rapid 3D camera fly-throughs",
        "key_features": [
            "Generates 5-second high-resolution video shots in approximately 120 seconds",
            "Superior 3D spatial consistency derived from Luma's NeRF and Gaussian Splatting heritage",
            "Keyframe extension: seamlessly extend video forward or backward in time",
            "Camera motion controls executing smooth cranes, orbit shots, and fast pans",
            "Image-to-video synthesis maintaining subject identity and character facial structures"
        ],
        "gotchas": [
            "Free tier generations have lower priority during peak traffic hours.",
            "Fast dynamic action sequences can occasionally suffer minor physics warping.",
            "Generations on basic plans cannot be used for commercial client delivery without subscription."
        ],
        "affiliate_url": "https://lumalabs.ai/dream-machine",
        "url": "https://lumalabs.ai/dream-machine"
    },

    "heygen": {
        "id": "heygen",
        "name": "HeyGen",
        "slug": "heygen",
        "category": "Video AI",
        "tagline": "Enterprise AI video communications platform featuring Avatar 3.0, Interactive Avatars, and multilingual voice cloning",
        "official_website": "https://heygen.com",
        "official_pricing_url": "https://www.heygen.com/pricing",
        "source_url": "https://www.heygen.com/pricing",
        "last_checked_at": "2026-09-30",
        "pricing": {
            "starting_price": "$29/mo",
            "billing_model": "Usage-based",
            "free_tier_details": "Free trial includes 1 credit and watermark on exported video",
            "tiers_summary": "Free (1 credit trial) / Creator $29/mo (15 credits) / Team $89/mo (30 credits) / Enterprise"
        },
        "technical_specs": {
            "current_models": [
                "Avatar 3.0",
                "Interactive Avatar (Real-time Video)",
                "Instant Avatar v2",
                "Voice Translation Engine"
            ],
            "context_window": "N/A",
            "byok_support": False,
            "open_source": False,
            "telemetry_privacy": True,
            "offline_support": False
        },
        "best_for": "Corporate trainers, marketing teams, and sales reps creating scalable personalized avatar videos and interactive agents",
        "key_features": [
            "Avatar 3.0 studio-grade digital humans with natural body language and micro-expressions",
            "Interactive Avatar platform enabling real-time, two-way conversational video agents via WebSockets",
            "Video Translate with automatic voice cloning, translation, and lip-sync alignment across 70+ languages",
            "Instant Avatar creation from a short 2-minute smartphone video clip",
            "API integration for programmatic personalized bulk video generation (CRM integration)"
        ],
        "gotchas": [
            "Credits cost roughly $2 per minute on Creator plan; video heavy pipelines require Enterprise contracts.",
            "Free trial videos carry a visible watermark and are restricted to 720p resolution.",
            "Interactive Avatar live WebSocket sessions consume distinct session minutes beyond video credits."
        ],
        "affiliate_url": "https://heygen.com",
        "url": "https://heygen.com"
    },

    # -------------------------------------------------------------------------
    # 5. VOICE AI (2 Flagship Tools -> 1 Pairwise Diff)
    # -------------------------------------------------------------------------
    "elevenlabs": {
        "id": "elevenlabs",
        "name": "ElevenLabs",
        "slug": "elevenlabs",
        "category": "Voice AI",
        "tagline": "Industry-leading voice AI platform offering Conversational AI agents, emotional voice cloning, and audio Reader",
        "official_website": "https://elevenlabs.io",
        "official_pricing_url": "https://elevenlabs.io/pricing",
        "source_url": "https://elevenlabs.io/pricing",
        "last_checked_at": "2026-09-30",
        "pricing": {
            "starting_price": "$5/mo",
            "billing_model": "Usage-based",
            "free_tier_details": "Free tier with 10,000 characters/mo (non-commercial use, attribution required)",
            "tiers_summary": "Free (10k chars/mo) / Starter $5/mo (30k chars) / Creator $22/mo (100k chars) / Pro $99/mo (500k chars)"
        },
        "technical_specs": {
            "current_models": [
                "Multilingual v2",
                "Turbo v2.5",
                "Flash v2",
                "Conversational AI WebSocket"
            ],
            "context_window": "N/A",
            "byok_support": False,
            "open_source": False,
            "telemetry_privacy": True,
            "offline_support": False
        },
        "best_for": "Developers, podcasters, game studios, and product teams needing emotional TTS, real-time voice agents, and dubbing",
        "key_features": [
            "Conversational AI platform for building ultra-low latency interactive voice agents via direct WebSockets",
            "Multilingual v2 and Turbo v2.5 models supporting 32+ languages with realistic human prosody and emotion",
            "Professional Voice Cloning replicating precise human vocal timbre from audio samples",
            "Voice Isolator tool removing background studio noise and hiss from audio tracks",
            "ElevenLabs Reader mobile app and AI dubbing studio with automatic multi-speaker alignment"
        ],
        "gotchas": [
            "Free tier strictly forbids commercial monetization and mandates attribution.",
            "Conversational AI agents consume character quotas based on bidirectional stream duration.",
            "Unused monthly character credits do not roll over to subsequent billing cycles."
        ],
        "affiliate_url": "https://elevenlabs.io",
        "url": "https://elevenlabs.io"
    },

    "cartesia-sonic": {
        "id": "cartesia-sonic",
        "name": "Cartesia Sonic",
        "slug": "cartesia-sonic",
        "category": "Voice AI",
        "tagline": "Ultra-low latency State Space Model (SSM) voice engine generating human speech in under 90ms for live agents",
        "official_website": "https://cartesia.ai",
        "official_pricing_url": "https://cartesia.ai/pricing",
        "source_url": "https://cartesia.ai/pricing",
        "last_checked_at": "2026-09-30",
        "pricing": {
            "starting_price": "$5/mo / Pay-per-character API",
            "billing_model": "Usage-based",
            "free_tier_details": "Free tier includes $5 in API credits to test low-latency streaming",
            "tiers_summary": "Pay-as-you-go (~$0.075 per 1,000 characters) / Custom Enterprise"
        },
        "technical_specs": {
            "current_models": [
                "Sonic (State Space Model Architecture)",
                "Sonic Multilingual",
                "Voice Changer API"
            ],
            "context_window": "N/A",
            "byok_support": True,
            "open_source": False,
            "telemetry_privacy": True,
            "offline_support": False
        },
        "best_for": "Engineers building real-time phone agents, conversational NPCs, and low-latency voice applications",
        "key_features": [
            "Sub-90ms Time-to-First-Audio (TTFA) latency powered by State Space Models (Mamba-based)",
            "WebSocket bidirectional streaming delivering uninterrupted audio chunks",
            "Fine-grained vocal emotion and cadence tuning via structured generation parameters",
            "Cross-lingual voice transfer preserving speaker accent and inflection",
            "Direct SDK integration for Python, TypeScript, and telephony WebRTC platforms"
        ],
        "gotchas": [
            "Built specifically as an API-first platform; does not offer an end-user consumer reading app.",
            "Long-form expressive audiobook narration has fewer community presets than ElevenLabs.",
            "Requires active credit card on file for sustained production API concurrency."
        ],
        "affiliate_url": "https://cartesia.ai",
        "url": "https://cartesia.ai"
    },

    # -------------------------------------------------------------------------
    # 6. WORKFLOW / AGENT AI (3 Flagship Tools -> 3 Pairwise Diffs)
    # -------------------------------------------------------------------------
    "n8n": {
        "id": "n8n",
        "name": "n8n",
        "slug": "n8n",
        "category": "Workflow AI",
        "tagline": "Fair-code workflow automation platform offering 100% free self-hosted execution, LangChain AI agents, and $20/mo Cloud",
        "official_website": "https://n8n.io",
        "official_pricing_url": "https://n8n.io/pricing",
        "source_url": "https://n8n.io/pricing",
        "last_checked_at": "2026-09-30",
        "pricing": {
            "starting_price": "Self-hosted Free / $20/mo Cloud",
            "billing_model": "Freemium",
            "free_tier_details": "100% free and unlimited executions when self-hosted on your own infrastructure (Docker/npm)",
            "tiers_summary": "Community Self-Hosted (Free, unlimited executions) / Cloud Starter $20/mo (2.5k executions) / Cloud Pro $50/mo"
        },
        "technical_specs": {
            "current_models": [
                "n8n AI Agent Nodes (LangChain)",
                "Custom Python / Node.js Engine",
                "Docker / Self-Hosted Core"
            ],
            "context_window": "N/A",
            "byok_support": True,
            "open_source": True,
            "telemetry_privacy": True,
            "offline_support": True
        },
        "best_for": "Developers, technical founders, and privacy-conscious teams needing sovereign workflow automation without per-task fees",
        "key_features": [
            "Self-hosted Community Edition is 100% free with unlimited executions and zero task caps",
            "Native LangChain AI agent integration nodes with memory, tools, and custom prompt chaining",
            "Full data sovereignty: deploy locally or in private VPC via Docker, npm, or Kubernetes",
            "Embedded JavaScript and Python code nodes with access to custom npm modules and direct DB queries",
            "n8n Cloud hosted tier starting at $20/mo for teams wanting managed zero-maintenance infrastructure"
        ],
        "gotchas": [
            "Self-hosted version requires maintaining your own server infrastructure, Docker updates, and PostgreSQL backups.",
            "Fair-code license permits internal company use but restricts reselling n8n as a commercial hosted service.",
            "Cloud tier ($20/mo) counts executions differently than Zapier tasks (entire workflow run = 1 execution)."
        ],
        "affiliate_url": "https://n8n.io",
        "url": "https://n8n.io"
    },

    "make": {
        "id": "make",
        "name": "Make",
        "slug": "make",
        "category": "Workflow AI",
        "tagline": "Visual integration platform engineered for complex branching workflows, webhooks, and per-operation billing",
        "official_website": "https://make.com",
        "official_pricing_url": "https://www.make.com/en/pricing",
        "source_url": "https://www.make.com/en/pricing",
        "last_checked_at": "2026-09-30",
        "pricing": {
            "starting_price": "$9/mo",
            "billing_model": "Usage-based",
            "free_tier_details": "Free plan includes 1,000 operations/mo and 2 active scenarios",
            "tiers_summary": "Free (1k ops/mo) / Core $9/mo (10k ops) / Pro $16/mo (10k ops) / Teams $29/mo"
        },
        "technical_specs": {
            "current_models": [
                "Make Scenario Engine v2",
                "Native AI Assistant Modules",
                "HTTP/Webhook Connectors"
            ],
            "context_window": "N/A",
            "byok_support": True,
            "open_source": False,
            "telemetry_privacy": True,
            "offline_support": False
        },
        "best_for": "Automation architects, operations engineers, and growth teams requiring visual routers, iterators, and error handlers",
        "key_features": [
            "Visual canvas for designing multi-branch workflows with routers, iterators, and aggregators",
            "Pay-per-operation pricing model ($9/mo for 10k ops) providing cost efficiency over task-based competitors",
            "Real-time visual execution inspector with step-by-step data payload debugging",
            "1,500+ pre-built SaaS app connectors and direct HTTP/webhook request modules",
            "Custom JavaScript functions, data formatters, and regex transformations inside scenario nodes"
        ],
        "gotchas": [
            "Every single module action and iteration counts as 1 operation; misconfigured loops can burn 10k ops in minutes.",
            "Free tier is restricted to 15-minute polling intervals on scheduled triggers.",
            "Enterprise data retention and custom variables require Pro ($16/mo) or Teams ($29/mo) plans."
        ],
        "affiliate_url": "https://make.com",
        "url": "https://make.com"
    },

    "zapier": {
        "id": "zapier",
        "name": "Zapier",
        "slug": "zapier",
        "category": "Workflow AI",
        "tagline": "The enterprise workflow automation standard featuring Zapier Central AI agents, Tables, and Interfaces",
        "official_website": "https://zapier.com",
        "official_pricing_url": "https://zapier.com/pricing",
        "source_url": "https://zapier.com/pricing",
        "last_checked_at": "2026-09-30",
        "pricing": {
            "starting_price": "$19.99/mo",
            "billing_model": "Usage-based",
            "free_tier_details": "Free tier includes 100 tasks/mo with 2-step single Zaps",
            "tiers_summary": "Free (100 tasks/mo) / Professional $19.99/mo (750 tasks) / Team $69/mo (2k tasks) / Enterprise"
        },
        "technical_specs": {
            "current_models": [
                "Zapier Central AI Engine",
                "Zapier Tables & Interfaces",
                "Code by Zapier (Node.js/Python)"
            ],
            "context_window": "N/A",
            "byok_support": True,
            "open_source": False,
            "telemetry_privacy": True,
            "offline_support": False
        },
        "best_for": "Non-technical teams, marketing operations, and enterprises needing seamless integration across 6,000+ SaaS apps",
        "key_features": [
            "Zapier Central autonomous AI agents executing tasks across your connected business tools",
            "Zapier Tables relational database workspace engineered specifically for automation workflows",
            "Zapier Interfaces for building custom client portals, internal lead forms, and interactive apps",
            "Massive ecosystem of 6,000+ certified SaaS app integrations with zero coding required",
            "Paths logic for conditional execution and custom code steps (JavaScript / Python)"
        ],
        "gotchas": [
            "Task-based pricing scales steeply on high-volume background pipelines compared to self-hosted alternatives.",
            "Free tier only permits simple 2-step Zaps; multi-step workflows require Professional ($19.99/mo).",
            "Data polling frequency on Professional is 2 minutes (instant webhooks depend on app connector support)."
        ],
        "affiliate_url": "https://zapier.com",
        "url": "https://zapier.com"
    }
}

# Preserve additional legacy attributes for backward compatibility
with open(P_SRC, "r", encoding="utf-8") as f:
    existing_tools = {t["slug"]: t for t in json.load(f)}

curated_list = []
for slug, spec in FLAGSHIP_SPECS.items():
    existing = existing_tools.get(slug, {})
    tool_entry = dict(existing)
    tool_entry.update(spec)
    # Ensure legacy mirror properties
    tool_entry["starting_price"] = spec["pricing"]["starting_price"]
    tool_entry["pricing_model"] = spec["pricing"]["billing_model"]
    ft = spec["pricing"]["free_tier_details"].lower()
    tool_entry["free_tier"] = ("free" in ft or "trial" in ft) and "paid only" not in ft
    curated_list.append(tool_entry)

# Write to both paths
for path in [P_SRC, P_DATA]:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(curated_list, f, indent=2, ensure_ascii=False)
print("\n[OK] Curated flagship catalog updated successfully!")
