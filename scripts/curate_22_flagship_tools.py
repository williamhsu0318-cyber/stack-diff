#!/usr/bin/env python3
"""
scripts/curate_22_flagship_tools.py
=============================================================================
Prunes the tool database down to the 23 most popular flagship AI tools
across 6 core productivity categories.
Applies verified Canonical ToolData Schema with evergreen slugs, exact
calibrated models, objective commercial gotchas (strictly quotas, overages,
minimum seats, rollovers, license restrictions; zero subjective commentary).
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
        "tagline": "AI-first code editor fork of VS Code engineered for whole-codebase indexing and autonomous Composer multi-file edits",
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
                "Claude 3.7 Sonnet",
                "Claude 3.5 Sonnet",
                "GPT-4o",
                "OpenAI o1"
            ],
            "context_window": "200K",
            "byok_support": True,
            "open_source": False,
            "telemetry_privacy": True,
            "offline_support": False
        },
        "best_for": "Software engineers wanting autonomous multi-file generation with instant diff reviews",
        "key_features": [
            "Composer multi-file autonomous generation and automatic diff application",
            "Full codebase semantic indexing with symbol-aware contextual retrieval (@codebase)",
            "Copilot++ intelligent multi-line autocomplete predicting next edit locations",
            "Seamless model switching across Claude 3.7/3.5 Sonnet, GPT-4o, and DeepSeek",
            "1-click migration importing all VS Code extensions, themes, and keybindings"
        ],
        "gotchas": [
            "Pro plan includes 500 fast premium requests/mo; subsequent requests enter slow queue or optional $0.10/req overage.",
            "BYOK usage bypasses fast request limits but incurs direct API billing from your model provider.",
            "Hobby free trial downgrades to 50 slow requests/month after 14 days."
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
                "Claude 3.7 Sonnet",
                "Claude 3.5 Sonnet",
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
        "best_for": "Developers wanting native multi-IDE inline completions across VS Code, JetBrains, and Visual Studio",
        "key_features": [
            "Seamless multi-model switching between Claude 3.7/3.5 Sonnet, GPT-4o, OpenAI o1, and Gemini 2.0 Flash",
            "Real-time inline ghost-text code completions embedded directly into your editor cursor",
            "Copilot Chat with workspace symbol awareness and Pull Request generation on GitHub.com",
            "Native cross-IDE plugin support across VS Code, JetBrains, Visual Studio, and Neovim",
            "Enterprise-grade security controls, centralized seat management, and IP copyright indemnity"
        ],
        "gotchas": [
            "Copilot Free tier is limited to 2,000 code completions and 50 chat messages per month.",
            "Zero BYOK support; developers cannot connect external private API keys or private local weights.",
            "Business tier requires centralized GitHub organization seat management ($19/user/mo)."
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
                "Claude 3.7 Sonnet",
                "GPT-4o"
            ],
            "context_window": "128K",
            "byok_support": False,
            "open_source": False,
            "telemetry_privacy": True,
            "offline_support": False
        },
        "best_for": "Developers wanting an AI-first IDE with unlimited completions at a lower price point",
        "key_features": [
            "Cascade engine delivering collaborative agentic workflows and real-time execution tracking",
            "Supercomplete intelligent multi-line code generation with sub-100ms latency",
            "Direct VS Code fork architecture supporting all standard extensions and configurations",
            "Command line and terminal awareness with automatic command suggestion and error repair",
            "Deep codebase indexing with live semantic symbol resolution"
        ],
        "gotchas": [
            "Cascade agentic executions consume monthly prompt credits that cap daily automated workflows.",
            "Standard Pro tier does not provide custom BYOK API key integration.",
            "Teams tier enforces a minimum commitment of 2 seats billed monthly or annually."
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
                "v0 Component Engine",
                "Claude 3.7 Sonnet"
            ],
            "context_window": "128K",
            "byok_support": False,
            "open_source": False,
            "telemetry_privacy": True,
            "offline_support": False
        },
        "best_for": "Frontend engineers and designers needing instant production React and Tailwind code",
        "key_features": [
            "Live interactive component canvas with real-time DOM previews and mobile viewport toggles",
            "Copy-pasteable Shadcn UI and Tailwind CSS modular architecture",
            "Image-to-code and Figma-to-code reverse engineering from uploaded UI screenshots",
            "Native 1-click deploy to Vercel and direct CLI component installation (npx shadcn@latest add)",
            "Multi-turn conversational iteration allowing granular CSS and component state adjustments"
        ],
        "gotchas": [
            "Monthly generation credits do not roll over to subsequent billing cycles.",
            "Free tier generations are publicly indexed in the community explore directory.",
            "Specialized strictly in frontend React and Tailwind markup; backend logic requires external implementation."
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
                "Claude 3.7 Sonnet",
                "GPT-4o"
            ],
            "context_window": "128K",
            "byok_support": False,
            "open_source": False,
            "telemetry_privacy": True,
            "offline_support": False
        },
        "best_for": "Founders and builders creating full-stack web applications with authentication and databases",
        "key_features": [
            "Generates full-stack React applications with backend API routes and Supabase database schemas",
            "Native GitHub bi-directional synchronization committing code directly to your repository",
            "Interactive live preview environment with real-time hot reloading",
            "Visual element inspector allowing direct click-to-edit prompt refinements",
            "Built-in user authentication, PostgreSQL table creation, and Row Level Security rules"
        ],
        "gotchas": [
            "Starter plan ($20/mo) includes 100 message edits per month; overages require upgrading to Pro ($50/mo).",
            "Monthly edit credits do not roll over to subsequent billing cycles.",
            "Active paid subscription is required to export clean production code without platform branding."
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
                "OpenAI o1",
                "OpenAI o3-mini",
                "GPT-4o mini"
            ],
            "context_window": "128K",
            "byok_support": False,
            "open_source": False,
            "telemetry_privacy": True,
            "offline_support": False
        },
        "best_for": "Knowledge workers, researchers, and developers wanting reasoning models and execution tools",
        "key_features": [
            "Frontier reasoning with OpenAI o1 and o3-mini alongside versatile GPT-4o multimodal engine",
            "Advanced Voice Mode with real-time natural conversational interruptions and inflection",
            "Canvas collaborative workspace for inline text drafting and code iteration",
            "Integrated web search, sandboxed Python code analysis, and DALL-E image generation",
            "Custom GPT marketplace and memory persistence across conversations"
        ],
        "gotchas": [
            "Plus ($20/mo) enforces dynamic rate limits on OpenAI o1 reasoning model during peak global usage.",
            "Web and mobile consumer applications do not support BYOK (developer API usage is billed separately).",
            "Team plan requires a mandatory minimum commitment of 2 seats ($25-$30/user/mo)."
        ],
        "affiliate_url": "https://chatgpt.com",
        "url": "https://chatgpt.com"
    },

    "claude": {
        "id": "claude",
        "name": "Claude Pro",
        "slug": "claude",
        "category": "LLM",
        "tagline": "Anthropic's frontier AI ecosystem offering hybrid reasoning, nuanced prose, and live Artifacts prototyping",
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
                "Claude 3.7 Sonnet (Hybrid Reasoning)",
                "Claude 3.5 Sonnet",
                "Claude 3.5 Haiku"
            ],
            "context_window": "200K",
            "byok_support": True,
            "open_source": False,
            "telemetry_privacy": True,
            "offline_support": False
        },
        "best_for": "Software engineers and writers demanding natural prose and coding intelligence",
        "key_features": [
            "Access to flagship Claude 3.7 Sonnet with toggleable extended reasoning alongside Claude 3.5 Haiku",
            "Artifacts interactive workspace for live React, HTML, SVG, and diagram rendering",
            "200,000 token context window for ingesting full codebases, logs, and technical manuscripts",
            "Projects workspace for persistent team wikis, brand voice guidelines, and file stores",
            "Visual reasoning for dense architectural diagrams, UI mockups, and financial statements"
        ],
        "gotchas": [
            "Pro subscription ($20/mo) enforces rolling 5-hour message caps that dynamically throttle during peak demand.",
            "Team plan enforces a mandatory minimum commitment of 5 users ($125/mo).",
            "Standard chat interface does not include sandboxed Python execution or native image generation."
        ],
        "affiliate_url": "https://claude.ai",
        "url": "https://claude.ai"
    },

    "gemini": {
        "id": "gemini",
        "name": "Gemini Advanced",
        "slug": "gemini",
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
                "Gemini 1.5 Flash"
            ],
            "context_window": "2M",
            "byok_support": False,
            "open_source": False,
            "telemetry_privacy": True,
            "offline_support": False
        },
        "best_for": "Researchers, Google Workspace users, and engineers ingesting massive documents or entire code repos",
        "key_features": [
            "Massive 2,000,000 token context window for ingesting full codebases, hours of audio, and dense video",
            "Powered by Gemini 2.0 Flash and Gemini 1.5 Pro multimodal architectures",
            "Deep Google Workspace integration (Docs, Gmail, Sheets, Drive) for instant contextual drafting",
            "Includes 2TB Google One cloud storage and priority access to Google AI Studio features",
            "Native execution of Python code and live multimodal audio/visual understanding"
        ],
        "gotchas": [
            "Tied strictly to personal Google One storage accounts; cannot be billed as a standalone team workspace.",
            "Google AI Studio / developer API usage is billed separately and not included in Google One AI Premium ($19.99/mo).",
            "Free tier enforces lower requests-per-minute rate limits during peak usage periods."
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
                "DeepSeek-V3 (Base 671B MoE)"
            ],
            "context_window": "64K",
            "byok_support": True,
            "open_source": True,
            "telemetry_privacy": True,
            "offline_support": True
        },
        "best_for": "Developers and businesses seeking benchmark-leading reasoning at low API costs",
        "key_features": [
            "DeepSeek-R1 open-weight reasoning model rivaling OpenAI o1 on math, code, and STEM benchmarks",
            "DeepSeek-V3 671B Mixture-of-Experts architecture delivering ultra-fast inference speed",
            "MIT license unencumbered open weights available for private on-premise deployment via Ollama/vLLM",
            "Context caching mechanism reducing repetitive prompt costs down to $0.014 per million tokens",
            "100% free public conversational web interface and mobile applications"
        ],
        "gotchas": [
            "Public web interface (chat.deepseek.com) enforces dynamic capacity limits during peak global traffic.",
            "Native context window is 64,000 tokens (compared to 128k–2M on western commercial platforms).",
            "Self-hosting the full 671B model requires enterprise multi-GPU server infrastructure (8x H100 80GB)."
        ],
        "affiliate_url": "https://chat.deepseek.com",
        "url": "https://chat.deepseek.com"
    },

    "perplexity": {
        "id": "perplexity",
        "name": "Perplexity Pro",
        "slug": "perplexity",
        "category": "LLM",
        "tagline": "Conversational answer engine combining verified live web search with multi-model switching (Claude, GPT-4o, Sonar)",
        "official_website": "https://perplexity.ai",
        "official_pricing_url": "https://www.perplexity.ai/pro",
        "source_url": "https://www.perplexity.ai/pro",
        "last_checked_at": "2026-09-30",
        "pricing": {
            "starting_price": "$20/mo",
            "billing_model": "Subscription",
            "free_tier_details": "Free plan includes unlimited Quick search queries and 5 Pro searches per day",
            "tiers_summary": "Free / Pro $20/mo ($200/yr) / Enterprise Pro $40/seat/mo"
        },
        "technical_specs": {
            "current_models": [
                "Perplexity Sonar Reasoning",
                "Claude 3.7 Sonnet",
                "GPT-4o"
            ],
            "context_window": "128K",
            "byok_support": False,
            "open_source": False,
            "telemetry_privacy": True,
            "offline_support": False
        },
        "best_for": "Researchers and analysts requiring real-time web citations without SEO spam",
        "key_features": [
            "Pro Search with multi-step search query decomposition and cross-source verification",
            "Instant model switching across Sonar, Claude 3.7 Sonnet, and GPT-4o",
            "Inline numbered citations linked directly to live web sources and academic papers",
            "Collections workspace for organizing research threads and sharing knowledge hubs",
            "Upload files (PDFs, CSVs, code) for deep contextual search and data extraction"
        ],
        "gotchas": [
            "Pro plan provides 300+ Pro searches per day; high-frequency automated scraping is prohibited.",
            "Included $5/mo developer API credit does not roll over if unused.",
            "Enterprise security controls (SSO, SOC2, data retention) require Enterprise Pro tier ($40/seat/mo)."
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
        "tagline": "Industry-benchmark image synthesis engine offering photorealism, artistic coherence, and web canvas editor",
        "official_website": "https://midjourney.com",
        "official_pricing_url": "https://docs.midjourney.com/docs/plans",
        "source_url": "https://docs.midjourney.com/docs/plans",
        "last_checked_at": "2026-09-30",
        "pricing": {
            "starting_price": "$10/mo",
            "billing_model": "GPU Hour Subscription",
            "free_tier_details": "No permanent free tier; periodic free trials during major model updates",
            "tiers_summary": "Basic $10/mo (3.3 GPU hrs) / Standard $30/mo (15 fast hrs + unlimited relax) / Pro $60/mo / Mega $120/mo"
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
        "best_for": "Art directors and creators demanding maximum aesthetic quality and cinematic lighting",
        "key_features": [
            "Benchmark cinematic aesthetic quality, photorealistic skin textures, and atmospheric lighting",
            "Dedicated web canvas UI featuring inpainting, pan, zoom out, and region repainting",
            "Style Reference (--sref) and Character Reference (--cref) for consistent visual identity",
            "Unlimited Relax GPU mode on Standard ($30/mo) tier for budget-free background rendering",
            "Niji 6 specialized tuning for anime, illustrative concept art, and comic styling"
        ],
        "gotchas": [
            "Basic ($10/mo) and Standard ($30/mo) tiers publish all generated images publicly in the community gallery.",
            "Private generation (Stealth Mode) is strictly restricted to Pro ($60/mo) and Mega ($120/mo) plans.",
            "No official public REST API; automation must be performed via Web UI or Discord bot."
        ],
        "affiliate_url": "https://midjourney.com",
        "url": "https://midjourney.com"
    },

    "flux": {
        "id": "flux",
        "name": "FLUX",
        "slug": "flux",
        "category": "Image AI",
        "tagline": "Open-weight generative image suite by Black Forest Labs delivering typography rendering and photorealism",
        "official_website": "https://blackforestlabs.ai",
        "official_pricing_url": "https://blackforestlabs.ai",
        "source_url": "https://blackforestlabs.ai",
        "last_checked_at": "2026-09-30",
        "pricing": {
            "starting_price": "Free / API pay-per-image",
            "billing_model": "Usage-based",
            "free_tier_details": "FLUX.1 [schnell] is Apache 2.0 open source and 100% free for local hardware",
            "tiers_summary": "FLUX.1 [schnell] Free Open Source / [dev] Non-commercial / [pro] API ~$0.03-$0.05/image"
        },
        "technical_specs": {
            "current_models": [
                "FLUX.1 [pro]",
                "FLUX.1 [dev]",
                "FLUX.1 [schnell]"
            ],
            "context_window": "N/A",
            "byok_support": True,
            "open_source": True,
            "telemetry_privacy": True,
            "offline_support": True
        },
        "best_for": "AI engineers and designers requiring commercial open weights or accurate in-image text",
        "key_features": [
            "World-class in-image typography and text spelling accuracy inside generated posters and signs",
            "FLUX.1 [schnell] 4-step distilled model available under Apache 2.0 for unrestricted local use",
            "ComfyUI and Diffusers native integration for granular LoRA and ControlNet pipelines",
            "State-of-the-art anatomy rendering (complex hand gestures, multiple subjects, exact prompt adherence)",
            "Commercial API endpoints available across Replicate, Fal.ai, and Together.ai"
        ],
        "gotchas": [
            "FLUX.1 [dev] license is strictly non-commercial; commercial deployment requires [pro] API or commercial license.",
            "Local execution of FLUX.1 [dev] requires minimum 16GB–24GB VRAM GPU hardware.",
            "Black Forest Labs does not host an all-in-one conversational consumer web canvas."
        ],
        "affiliate_url": "https://blackforestlabs.ai",
        "url": "https://blackforestlabs.ai"
    },

    "recraft": {
        "id": "recraft",
        "name": "Recraft",
        "slug": "recraft",
        "category": "Image AI",
        "tagline": "Design-first AI platform generating infinite canvas vector art (SVG), 3D graphics, and brand palettes",
        "official_website": "https://www.recraft.ai",
        "official_pricing_url": "https://www.recraft.ai/pricing",
        "source_url": "https://www.recraft.ai/pricing",
        "last_checked_at": "2026-09-30",
        "pricing": {
            "starting_price": "$20/mo",
            "billing_model": "Credit-based",
            "free_tier_details": "Free plan includes 50 daily credits with public generations",
            "tiers_summary": "Free (50 credits/day) / Basic $20/mo (1,000 fast credits) / Pro $48/mo / Enterprise"
        },
        "technical_specs": {
            "current_models": [
                "Recraft V3 (Red_Panda)",
                "Recraft 20B Vector Engine"
            ],
            "context_window": "N/A",
            "byok_support": False,
            "open_source": False,
            "telemetry_privacy": True,
            "offline_support": False
        },
        "best_for": "Graphic designers and brand teams needing clean SVGs, 3D icons, and vector brand kits",
        "key_features": [
            "Native vector graphics generation outputting clean, editable SVGs with minimal anchor points",
            "Recraft V3 model benchmarked #1 on Artificial Analysis image generation leaderboard",
            "Brand kit synchronization enforcing exact HEX color palettes and visual styles across assets",
            "Infinite 2D canvas with integrated vector editing, background removal, and vectorizer tools",
            "Commercial REST API for programmatic vector and raster asset synthesis"
        ],
        "gotchas": [
            "Free tier creations are public and cannot be made private without a paid subscription.",
            "Monthly fast credits do not roll over past the active billing cycle.",
            "Vector exports on free tier include platform attribution metadata."
        ],
        "affiliate_url": "https://www.recraft.ai",
        "url": "https://www.recraft.ai"
    },

    "ideogram": {
        "id": "ideogram",
        "name": "Ideogram",
        "slug": "ideogram",
        "category": "Image AI",
        "tagline": "AI image generator specializing in typography, graphic design layouts, and marketing banners",
        "official_website": "https://ideogram.ai",
        "official_pricing_url": "https://ideogram.ai/pricing",
        "source_url": "https://ideogram.ai/pricing",
        "last_checked_at": "2026-09-30",
        "pricing": {
            "starting_price": "$8/mo",
            "billing_model": "Subscription / Priority Credits",
            "free_tier_details": "Free plan includes 10 slow credits per day (40 images/day)",
            "tiers_summary": "Free (10 credits/day) / Basic $8/mo (400 priority credits) / Plus $20/mo (1,000 credits) / Pro $60/mo"
        },
        "technical_specs": {
            "current_models": [
                "Ideogram 2.0",
                "Ideogram 2.0 Turbo"
            ],
            "context_window": "N/A",
            "byok_support": False,
            "open_source": False,
            "telemetry_privacy": True,
            "offline_support": False
        },
        "best_for": "Marketing designers and creators requiring accurate lettering and graphic layouts",
        "key_features": [
            "Pioneering graphic text rendering with accurate spelling inside complex typography layouts",
            "Magic Prompt feature automatically expanding shorthand prompts into detailed visual briefs",
            "Canvas workspace with Magic Fill (inpainting) and Extend (outpainting) tools",
            "Color Palette controls allowing users to define exact HEX color schemes for consistent brand assets",
            "Ideogram 2.0 Turbo model offering high-speed generations at 50% lower credit consumption"
        ],
        "gotchas": [
            "Basic ($8/mo) generations remain public in community feed; private mode requires Plus ($20/mo).",
            "Free credits expire daily and do not accumulate across days.",
            "Priority generation credits do not roll over to subsequent months."
        ],
        "affiliate_url": "https://ideogram.ai",
        "url": "https://ideogram.ai"
    },

    # -------------------------------------------------------------------------
    # 4. VIDEO AI (4 Flagship Tools -> 6 Pairwise Diffs)
    # -------------------------------------------------------------------------
    "runway": {
        "id": "runway",
        "name": "Runway",
        "slug": "runway",
        "category": "Video AI",
        "tagline": "Cinematic AI video generation platform powered by Gen-3 Alpha, Gen-3 Turbo, and Act-One facial performance capture",
        "official_website": "https://runwayml.com",
        "official_pricing_url": "https://runwayml.com/pricing",
        "source_url": "https://runwayml.com/pricing",
        "last_checked_at": "2026-09-30",
        "pricing": {
            "starting_price": "$15/mo",
            "billing_model": "Credit-based",
            "free_tier_details": "Free plan includes 125 one-time credits with standard generation queues",
            "tiers_summary": "Basic Free (125 credits) / Standard $15/mo (625 credits) / Pro $35/mo (2,250 credits) / Unlimited $95/mo"
        },
        "technical_specs": {
            "current_models": [
                "Gen-3 Alpha",
                "Gen-3 Alpha Turbo",
                "Act-One"
            ],
            "context_window": "N/A",
            "byok_support": False,
            "open_source": False,
            "telemetry_privacy": True,
            "offline_support": False
        },
        "best_for": "Filmmakers and VFX artists needing cinematic video generation and camera steering",
        "key_features": [
            "Gen-3 Alpha and Gen-3 Alpha Turbo high-fidelity video synthesis from text, image, and video prompts",
            "Act-One facial performance capture transferring real actor expressions onto stylized characters",
            "Director Mode camera controls with precise pan, tilt, zoom, and multi-motion brush masks",
            "4K video upscaling, lip-sync dubbing, and integrated generative audio sound effects",
            "Fast generation mode via Gen-3 Alpha Turbo delivering 7x speedups for storyboarding"
        ],
        "gotchas": [
            "Standard plan ($15/mo) provides 625 credits/mo (Gen-3 Alpha consumes 10 credits per second of video).",
            "Monthly subscription credits do not roll over past billing cycle caps.",
            "Watermark removal is restricted to paid Standard ($15/mo) and higher tiers."
        ],
        "affiliate_url": "https://runwayml.com",
        "url": "https://runwayml.com"
    },

    "kling": {
        "id": "kling",
        "name": "Kling AI",
        "slug": "kling",
        "category": "Video AI",
        "tagline": "High-motion generative video platform engineered by Kuaishou offering 1080p outputs and realistic physics",
        "official_website": "https://klingai.com",
        "official_pricing_url": "https://klingai.com/pricing",
        "source_url": "https://klingai.com/pricing",
        "last_checked_at": "2026-09-30",
        "pricing": {
            "starting_price": "$10/mo",
            "billing_model": "Credit-based",
            "free_tier_details": "Free plan provides 66 daily credits allowing ~6 short video generations per day",
            "tiers_summary": "Free (66 credits/day) / Standard $10/mo (660 credits) / Pro $37/mo (3,000 credits) / Premier $92/mo"
        },
        "technical_specs": {
            "current_models": [
                "Kling 1.5 Pro",
                "Kling 1.0"
            ],
            "context_window": "N/A",
            "byok_support": False,
            "open_source": False,
            "telemetry_privacy": True,
            "offline_support": False
        },
        "best_for": "Motion designers and creators needing complex human movement and high-motion adherence",
        "key_features": [
            "Kling 1.5 model delivering 1080p HD video resolution with physics simulation",
            "Generates long video clips up to 10 seconds in a single generation prompt",
            "Camera Control module with multi-angle rotational, horizontal, and vertical motion trajectories",
            "Motion Brush feature allowing localized animation of up to 6 distinct video regions",
            "Generous free tier offering 66 renewable credits every day without credit card requirement"
        ],
        "gotchas": [
            "Free plan renders with a watermark and restricts video exports to 720p resolution.",
            "Professional Mode generations take 3–8 minutes during peak global server queues.",
            "Daily free credits (66 credits) expire after 24 hours and do not accumulate."
        ],
        "affiliate_url": "https://klingai.com",
        "url": "https://klingai.com"
    },

    "luma": {
        "id": "luma",
        "name": "Luma Dream Machine",
        "slug": "luma",
        "category": "Video AI",
        "tagline": "High-speed generative video engine by Luma AI delivering realistic camera dynamics and 3D spatial awareness",
        "official_website": "https://lumalabs.ai/dream-machine",
        "official_pricing_url": "https://lumalabs.ai/dream-machine/pricing",
        "source_url": "https://lumalabs.ai/dream-machine/pricing",
        "last_checked_at": "2026-09-30",
        "pricing": {
            "starting_price": "$9.99/mo",
            "billing_model": "Credit-based",
            "free_tier_details": "Free plan provides 30 monthly generations with standard queue priority",
            "tiers_summary": "Free (30 gens/mo) / Standard $9.99/mo (120 gens) / Pro $29.99/mo (400 gens) / Premier $99.99/mo"
        },
        "technical_specs": {
            "current_models": [
                "Dream Machine 1.5",
                "Photon Spatial Engine"
            ],
            "context_window": "N/A",
            "byok_support": False,
            "open_source": False,
            "telemetry_privacy": True,
            "offline_support": False
        },
        "best_for": "Visual artists and game developers requiring dynamic 3D camera sweeps and spatial lighting",
        "key_features": [
            "Dream Machine 1.5 transformer architecture predicting consistent camera movements and lighting",
            "Sub-120 second video generation speed for rapid concept iteration",
            "Keyframe-to-Keyframe interpolation smoothly joining start and end frame images",
            "Camera motion paths including 360-degree orbit, crane, dolly, and tracking shots",
            "Native developer API endpoints for programmatic batch video generation"
        ],
        "gotchas": [
            "Free tier video generations enter a shared public queue that experiences latency during peak periods.",
            "Commercial usage rights and unwatermarked video downloads require paid Standard ($9.99/mo) or higher.",
            "Monthly generation credits expire at the end of each billing cycle."
        ],
        "affiliate_url": "https://lumalabs.ai/dream-machine",
        "url": "https://lumalabs.ai/dream-machine"
    },

    "heygen": {
        "id": "heygen",
        "name": "HeyGen",
        "slug": "heygen",
        "category": "Video AI",
        "tagline": "AI avatar and video localization platform creating studio-quality talking presenter videos from text",
        "official_website": "https://heygen.com",
        "official_pricing_url": "https://heygen.com/pricing",
        "source_url": "https://heygen.com/pricing",
        "last_checked_at": "2026-09-30",
        "pricing": {
            "starting_price": "$29/mo",
            "billing_model": "Credit-based",
            "free_tier_details": "Free plan includes 1 free credit (1 minute of video) with HeyGen branding",
            "tiers_summary": "Free (1 credit) / Creator $29/mo (15 credits) / Team $89/mo (30 credits) / Enterprise"
        },
        "technical_specs": {
            "current_models": [
                "Avatar 3.0",
                "Video Translate Engine"
            ],
            "context_window": "N/A",
            "byok_support": False,
            "open_source": False,
            "telemetry_privacy": True,
            "offline_support": False
        },
        "best_for": "Corporate sales and training teams creating localized presenter videos and tutorials",
        "key_features": [
            "100+ photorealistic AI avatars delivering natural speech inflections and eye contact",
            "Instant Video Translation automatically dubbing videos into 175+ languages with matching lip-sync",
            "Custom Instant Avatar generation from simple 2-minute webcam recording clips",
            "Voice cloning technology matching pitch, tone, and accent across international translations",
            "Enterprise API for automated video personalization at scale"
        ],
        "gotchas": [
            "Creator plan ($29/mo) allocates 15 minutes of video credit per month ($1.93 per minute).",
            "Unused monthly video credits on Creator tier do not roll over to subsequent months.",
            "Custom Studio Avatars require a separate one-time production setup fee."
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
        "tagline": "Industry-standard voice synthesis platform delivering emotive speech, voice cloning, and dubbing",
        "official_website": "https://elevenlabs.io",
        "official_pricing_url": "https://elevenlabs.io/pricing",
        "source_url": "https://elevenlabs.io/pricing",
        "last_checked_at": "2026-09-30",
        "pricing": {
            "starting_price": "$5/mo",
            "billing_model": "Character-based",
            "free_tier_details": "Free plan includes 10,000 characters/mo (approx. 10 mins of audio) with attribution required",
            "tiers_summary": "Free (10k chars) / Starter $5/mo (30k chars) / Creator $22/mo (100k chars) / Pro $99/mo (500k chars)"
        },
        "technical_specs": {
            "current_models": [
                "Eleven Multilingual v2",
                "Eleven Flash v2.5"
            ],
            "context_window": "N/A",
            "byok_support": False,
            "open_source": False,
            "telemetry_privacy": True,
            "offline_support": False
        },
        "best_for": "Audiobook narrators, game studios, and developers requiring emotionally nuanced voice acting",
        "key_features": [
            "Industry-leading emotional inflection, pause pacing, and conversational realism in 32+ languages",
            "Instant Voice Cloning from 1-minute audio sample and Professional Voice Cloning for studio narrators",
            "Eleven Flash v2.5 delivering sub-75ms latency for conversational agents and live voicebots",
            "AI Dubbing Studio translating video and audio tracks while preserving speaker original voice timbre",
            "Robust REST and WebSocket APIs with pre-built SDKs in Python, Node, and Go"
        ],
        "gotchas": [
            "Character allowance counts spaces and punctuation in input text.",
            "Free tier strictly mandates ElevenLabs attribution in published commercial outputs.",
            "Commercial usage rights require Starter ($5/mo) or higher subscription tier."
        ],
        "affiliate_url": "https://elevenlabs.io",
        "url": "https://elevenlabs.io"
    },

    "cartesia": {
        "id": "cartesia",
        "name": "Cartesia Sonic",
        "slug": "cartesia",
        "category": "Voice AI",
        "tagline": "State space architecture voice synthesis engine delivering sub-100ms streaming latency for voicebots",
        "official_website": "https://cartesia.ai",
        "official_pricing_url": "https://cartesia.ai/pricing",
        "source_url": "https://cartesia.ai/pricing",
        "last_checked_at": "2026-09-30",
        "pricing": {
            "starting_price": "$5/mo",
            "billing_model": "Usage / Audio Seconds",
            "free_tier_details": "Free tier includes $5 free API credits for sandbox development",
            "tiers_summary": "Free Sandbox ($5 credits) / Pro $5/mo base + $0.075 per audio minute / Enterprise"
        },
        "technical_specs": {
            "current_models": [
                "Sonic (State Space Model)",
                "Sonic Multilingual"
            ],
            "context_window": "N/A",
            "byok_support": True,
            "open_source": False,
            "telemetry_privacy": True,
            "offline_support": False
        },
        "best_for": "Voice AI engineers and customer bot teams requiring ultra-low latency audio streaming",
        "key_features": [
            "Groundbreaking State Space Model (SSM) architecture delivering sub-100ms time-to-first-audio chunk",
            "Ultra-low latency WebSocket streaming designed for live conversational call center bots",
            "Pay-as-you-go audio second billing ($0.075/min) significantly cheaper than character-based models",
            "Voice cloning capabilities allowing rapid duplication of target voice personas",
            "Zero minimum commitment on API usage with transparent per-second metering"
        ],
        "gotchas": [
            "Focused strictly on developer streaming API; does not include an end-user timeline audio editing UI.",
            "Telephony or WebSocket client integration must be implemented by the developer.",
            "Pre-made voice library is smaller than consumer voice marketplaces."
        ],
        "affiliate_url": "https://cartesia.ai",
        "url": "https://cartesia.ai"
    },

    # -------------------------------------------------------------------------
    # 6. WORKFLOW AI (3 Flagship Tools -> 3 Pairwise Diffs)
    # -------------------------------------------------------------------------
    "n8n": {
        "id": "n8n",
        "name": "n8n",
        "slug": "n8n",
        "category": "Workflow AI",
        "tagline": "Fair-code workflow automation platform allowing self-hosting, full data privacy, and LangChain AI agent nodes",
        "official_website": "https://n8n.io",
        "official_pricing_url": "https://n8n.io/pricing",
        "source_url": "https://n8n.io/pricing",
        "last_checked_at": "2026-09-30",
        "pricing": {
            "starting_price": "Free self-hosted / $20/mo Cloud",
            "billing_model": "Execution-based",
            "free_tier_details": "100% free forever when self-hosted on your own server or Docker container",
            "tiers_summary": "Self-Hosted Free (Fair-Code) / Starter Cloud $20/mo (2.5k execs) / Pro Cloud $50/mo (10k execs)"
        },
        "technical_specs": {
            "current_models": [
                "n8n AI Agent Nodes",
                "LangChain Connectors"
            ],
            "context_window": "N/A",
            "byok_support": True,
            "open_source": True,
            "telemetry_privacy": True,
            "offline_support": True
        },
        "best_for": "Developers and privacy-conscious enterprises wanting unlimited automations on private infrastructure",
        "key_features": [
            "Fair-code license allowing unlimited free executions when deployed on private VPS or Docker",
            "Native LangChain and AI Agent nodes supporting tool-calling, vector databases, and memory",
            "Execution-based pricing on Cloud ($20 for 2,500 full workflows) rather than charging per individual step",
            "Complete data privacy with zero external telemetry when self-hosted in air-gapped environments",
            "Custom JavaScript and Python code execution within any workflow node"
        ],
        "gotchas": [
            "Self-hosting Community edition requires managing your own Docker container, database, and backups.",
            "Community license restricts multi-user enterprise governance, advanced RBAC, and SSO.",
            "Cloud Starter tier enforces a 2,500 monthly workflow execution cap."
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
                "AI Assistant Modules"
            ],
            "context_window": "N/A",
            "byok_support": True,
            "open_source": False,
            "telemetry_privacy": True,
            "offline_support": False
        },
        "best_for": "Operations engineers and teams requiring visual routers, iterators, and aggregators",
        "key_features": [
            "Visual canvas for designing multi-branch workflows with routers, iterators, and aggregators",
            "Pay-per-operation pricing model ($9/mo for 10k ops) providing cost efficiency over task-based competitors",
            "Real-time visual execution inspector with step-by-step data payload debugging",
            "1,500+ pre-built SaaS app connectors and direct HTTP/webhook request modules",
            "Custom JavaScript functions, data formatters, and regex transformations inside scenario nodes"
        ],
        "gotchas": [
            "Every individual module execution and route iteration counts as 1 billable operation.",
            "Free tier restricts scheduled trigger polling intervals to a minimum of 15 minutes.",
            "Custom variables and extended data logs require Pro ($16/mo) or Teams ($29/mo) plans."
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
                "Zapier Central AI Agents",
                "Zapier Tables"
            ],
            "context_window": "N/A",
            "byok_support": True,
            "open_source": False,
            "telemetry_privacy": True,
            "offline_support": False
        },
        "best_for": "Non-technical teams needing turnkey integration across 6,000+ SaaS applications",
        "key_features": [
            "Zapier Central autonomous AI agents executing tasks across your connected business tools",
            "Zapier Tables relational database workspace engineered specifically for automation workflows",
            "Zapier Interfaces for building custom client portals, internal lead forms, and interactive apps",
            "Massive ecosystem of 6,000+ certified SaaS app integrations with zero coding required",
            "Paths logic for conditional execution and custom code steps (JavaScript / Python)"
        ],
        "gotchas": [
            "Free plan only permits single-step Zaps (1 trigger + 1 action); multi-step workflows require Professional ($19.99/mo).",
            "Data polling interval on Professional plan is 2 minutes (instant webhooks require supported app webhooks).",
            "Task overages on high-volume pipelines increase per-task costs without annual volume commitments."
        ],
        "affiliate_url": "https://zapier.com",
        "url": "https://zapier.com"
    }
}

# Preserve additional legacy attributes for backward compatibility
with open(P_SRC, "r", encoding="utf-8") as f:
    existing_tools = {t.get("slug"): t for t in json.load(f)}

curated_list = []
for slug, spec in FLAGSHIP_SPECS.items():
    existing = existing_tools.get(slug, {})
    tool_entry = dict(existing)
    tool_entry.update(spec)
    # Ensure legacy mirror properties
    tool_entry["id"] = slug
    tool_entry["slug"] = slug
    tool_entry["starting_price"] = spec["pricing"]["starting_price"]
    tool_entry["pricing_model"] = spec["pricing"]["billing_model"]
    ft = spec["pricing"]["free_tier_details"].lower()
    tool_entry["free_tier"] = ("free" in ft or "trial" in ft) and "paid only" not in ft
    tool_entry["platforms"] = ["Web", "API"]
    if "mac" in spec["tagline"].lower() or "editor" in spec["tagline"].lower() or slug in ["cursor", "windsurf", "github-copilot"]:
        tool_entry["platforms"] = ["Mac", "Windows", "Linux"]
    curated_list.append(tool_entry)

# Write to both paths
for path in [P_SRC, P_DATA]:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(curated_list, f, indent=2, ensure_ascii=False)

print(f"[OK] Curated {len(curated_list)} flagship tools with 100% objective gotchas successfully!")
