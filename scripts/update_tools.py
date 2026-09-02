"""
scripts/update_tools.py
-----------------------
Merges and updates tools.json to include all 20 specified AI tools
with full schema consistency (both user schema and Astro schema fields).
Emits output to both src/data/tools.json and data/tools.json.
"""

import json
from pathlib import Path

# Load existing tools
project_root = Path(__file__).resolve().parent.parent
data_tools_path = project_root / "data" / "tools.json"

with open(data_tools_path, "r", encoding="utf-8") as f:
    existing_tools = json.load(f)

# Convert existing tools to a dict keyed by id for seamless merging
tools_by_id = {t["id"]: t for t in existing_tools}

# Define the 20 tools specified in the request
# Each tool has complete fields satisfying:
# User Schema: id, name, category, pricing_model, starting_price, free_tier, primary_audience, platforms, core_positioning, key_capabilities, strengths, trade_offs, verdict_context, url
# Astro Schema: slug, tagline, best_for, key_features, pros, cons, supported_platforms, affiliate_url

UPDATED_AND_NEW_TOOLS = [
    # -------------------------------------------------------------
    # 1. Coding AI
    # -------------------------------------------------------------
    {
        "id": "cursor",
        "name": "Cursor",
        "slug": "cursor",
        "category": "Coding AI",
        "pricing_model": "Freemium",
        "starting_price": "$20/mo",
        "free_tier": True,
        "primary_audience": "Software engineers and full-stack builders wanting autonomous multi-file generation and instant diff reviews",
        "platforms": ["Mac", "Windows", "Linux"],
        "core_positioning": "AI-native code editor fork of VS Code engineered for codebase-wide indexing and agentic multi-file edits",
        "key_capabilities": [
            "Composer multi-file autonomous generation and automatic diff application",
            "Full codebase semantic indexing with contextual retrieval (@codebase)",
            "Copilot++ intelligent multi-line autocomplete predicting next edit locations",
            "Frontier model orchestration with Claude 3.5 Sonnet, GPT-4o, and DeepSeek-V3"
        ],
        "strengths": [
            "Fast 1-click diff reviews across complex multi-file architectural refactors",
            "Zero migration friction for VS Code extensions, themes, and keybindings",
            "Best-in-class frontier model orchestration tuned specifically for developer workflows"
        ],
        "trade_offs": [
            "Fast request quotas deplete rapidly during long-running agentic composer sessions",
            "Requires running a dedicated standalone IDE application rather than an extension"
        ],
        "verdict_context": "The premier choice for developers seeking an agentic, multi-file IDE with seamless VS Code compatibility",
        "url": "https://cursor.com"
    },
    {
        "id": "windsurf",
        "name": "Windsurf",
        "slug": "windsurf",
        "category": "Coding AI",
        "pricing_model": "Freemium",
        "starting_price": "$15/mo",
        "free_tier": True,
        "primary_audience": "Developers looking for an agentic IDE with deep terminal integration at a lower price point",
        "platforms": ["Mac", "Windows", "Linux"],
        "core_positioning": "Agentic AI IDE by Codeium featuring Flows and Cascade for autonomous terminal and multi-file reasoning",
        "key_capabilities": [
            "Cascade contextual agent integrating multi-file edits and terminal execution",
            "Supercomplete predictive multi-cursor autocomplete engine",
            "Deep codebase understanding with real-time file tree monitoring",
            "Context pinning and direct terminal command execution with user authorization"
        ],
        "strengths": [
            "More affordable starting price ($15/mo) compared to Cursor ($20/mo)",
            "Cascade agent exhibits strong autonomy in executing tests and fixing build errors",
            "Generous free tier powered by Codeium's proprietary acceleration infrastructure"
        ],
        "trade_offs": [
            "Newer ecosystem with fewer community plugins and templates compared to Cursor",
            "Occasional latency spikes on complex multi-turn Cascade agent tasks"
        ],
        "verdict_context": "Ideal for developers who want deep terminal command automation and agentic reasoning at an accessible price",
        "url": "https://codeium.com/windsurf"
    },
    {
        "id": "github-copilot",
        "name": "GitHub Copilot",
        "slug": "github-copilot",
        "category": "Coding AI",
        "pricing_model": "Paid Only",
        "starting_price": "$10/mo",
        "free_tier": False,
        "primary_audience": "Enterprise development teams requiring strict IP indemnity and existing IDE compatibility",
        "platforms": ["VS Code", "JetBrains", "Visual Studio", "Neovim", "CLI"],
        "core_positioning": "The enterprise-standard AI pair programmer integrated across VS Code, JetBrains, and Visual Studio",
        "key_capabilities": [
            "Real-time inline ghost-text code completions as you type",
            "Copilot Chat with workspace symbol awareness and explanation features",
            "GitHub.com PR summaries and automated code review comments",
            "Multi-IDE plugin support (VS Code, JetBrains IDEs, Visual Studio, Neovim)"
        ],
        "strengths": [
            "Direct native integration in virtually every mainstream IDE without migration",
            "Enterprise-grade security controls, SOC2 audit logs, and IP copyright indemnity",
            "Low-latency inline completions that blend invisibly into existing typing workflows"
        ],
        "trade_offs": [
            "Autonomous multi-file refactoring is less agile than Cursor Composer or Windsurf Cascade",
            "No permanent free tier for individual standard users"
        ],
        "verdict_context": "The industry standard for corporate engineering teams requiring enterprise security and broad IDE support",
        "url": "https://github.com/features/copilot"
    },
    {
        "id": "supermaven",
        "name": "Supermaven",
        "slug": "supermaven",
        "category": "Coding AI",
        "pricing_model": "Freemium",
        "starting_price": "$10/mo",
        "free_tier": True,
        "primary_audience": "Engineers in massive monorepos who prioritize ultra-fast typing completions over autonomous chat agents",
        "platforms": ["VS Code", "JetBrains", "Neovim", "Sublime Text"],
        "core_positioning": "Ultra-low-latency code completion engine powered by a 1-million-token context window (Babble architecture)",
        "key_capabilities": [
            "Sub-50ms completion latency via proprietary Babble transformer architecture",
            "Massive 1,000,000 token context window ingesting full repository state",
            "Lightweight plugins for VS Code, JetBrains, and Neovim",
            "Inline completions tailored for large monorepos and complex APIs"
        ],
        "strengths": [
            "Noticeably faster autocomplete responses than Copilot or Cursor",
            "1M context window eliminates file-hopping hallucinations in massive codebases",
            "Very low local memory and CPU footprint"
        ],
        "trade_offs": [
            "Focuses primarily on inline completion rather than agentic multi-file refactoring",
            "Chat interface is minimal compared to comprehensive IDE chat systems"
        ],
        "verdict_context": "The fastest inline autocomplete engine available, unmatched for navigating giant codebases with zero lag",
        "url": "https://supermaven.com"
    },
    {
        "id": "v0-by-vercel",
        "name": "v0 by Vercel",
        "slug": "v0-by-vercel",
        "category": "Coding AI",
        "pricing_model": "Freemium",
        "starting_price": "$20/mo",
        "free_tier": True,
        "primary_audience": "Frontend engineers, product designers, and full-stack builders rapidly scaffolding React UI layouts",
        "platforms": ["Web", "CLI", "Next.js"],
        "core_positioning": "Generative UI system by Vercel converting natural language prompts into production-ready React and Tailwind components",
        "key_capabilities": [
            "Generates modular React, Next.js, and Tailwind CSS code with live rendering",
            "Interactive visual canvas with direct component inspection and Figma import",
            "1-click deployment to Vercel and npm component export (shadcn/ui style)",
            "Iterative design prompting for micro-adjustments on buttons, tables, and layouts"
        ],
        "strengths": [
            "Generates exceptionally clean, semantic React code styled with Tailwind CSS",
            "Zero setup instant preview in sandbox browser before touching local codebase",
            "Seamless integration with shadcn/ui component standards and Vercel deployments"
        ],
        "trade_offs": [
            "Specialized for front-end UI components; not designed for full backend logic or database schemas",
            "Credits can deplete quickly when rerolling complex multi-page dashboard layouts"
        ],
        "verdict_context": "The gold standard for generating modern frontend React components and landing pages from scratch",
        "url": "https://v0.dev"
    },

    # -------------------------------------------------------------
    # 2. LLM / Frontier Models
    # -------------------------------------------------------------
    {
        "id": "chatgpt",
        "name": "ChatGPT Plus",
        "slug": "chatgpt",
        "category": "LLM",
        "pricing_model": "Freemium",
        "starting_price": "$20/mo",
        "free_tier": True,
        "primary_audience": "Knowledge workers, researchers, and developers wanting the most versatile multimodal AI assistant",
        "platforms": ["Web", "iOS", "Android", "Mac", "Windows", "API"],
        "core_positioning": "OpenAI's flagship subscription offering priority access to o1 reasoning models, GPT-4o, and Advanced Voice",
        "key_capabilities": [
            "Access to OpenAI o1 reasoning model and GPT-4o multimodal engine",
            "Real-time Advanced Voice Mode with conversational interruptions",
            "Sandboxed Python code execution and Advanced Data Analysis",
            "Custom GPT marketplace, memory persistence, and Canvas collaborative workspace"
        ],
        "strengths": [
            "Unrivaled tool ecosystem combining web search, code sandbox, and image generation in one place",
            "Superior multimodal voice interactivity with near-human prosody",
            "Continuous access to OpenAI's latest frontier reasoning architectures"
        ],
        "trade_offs": [
            "Usage message caps on flagship reasoning models (o1 and o1-mini)",
            "Strict automated guardrails can occasionally refuse benign technical prompts"
        ],
        "verdict_context": "The benchmark all-in-one assistant for general productivity, multimodal voice, and frontier reasoning",
        "url": "https://chat.openai.com"
    },
    {
        "id": "claude-3-5-sonnet",
        "name": "Claude Pro",
        "slug": "claude-3-5-sonnet",
        "category": "LLM",
        "pricing_model": "Freemium",
        "starting_price": "$20/mo",
        "free_tier": True,
        "primary_audience": "Software engineers, analytical writers, and researchers requiring elite reasoning and coding accuracy",
        "platforms": ["Web", "iOS", "Android", "Mac", "Windows", "API"],
        "core_positioning": "Anthropic's premium subscription providing 5x higher usage of Claude 3.5 Sonnet and interactive Artifacts",
        "key_capabilities": [
            "200,000 token context window for ingesting full codebases, logs, and books",
            "Artifacts interactive workspace for live React, SVG, HTML, and diagram rendering",
            "State-of-the-art coding, mathematical reasoning, and nuanced prose benchmarks",
            "Projects feature for organizing team wikis and contextual documentation"
        ],
        "strengths": [
            "Industry benchmark code generation quality with minimal need for manual refactoring",
            "Interactive Artifacts drastically accelerate front-end component prototyping",
            "Nuanced, natural prose that avoids formulaic AI clichés"
        ],
        "trade_offs": [
            "Enforces rolling dynamic message volume limits during high-traffic windows",
            "Lacks native image generation and sandboxed Python code execution in UI"
        ],
        "verdict_context": "The reigning champion for coding accuracy, complex reasoning, and natural literary writing tone",
        "url": "https://claude.ai"
    },
    {
        "id": "gemini-advanced",
        "name": "Gemini Advanced",
        "slug": "gemini-advanced",
        "category": "LLM",
        "pricing_model": "Freemium",
        "starting_price": "$19.99/mo",
        "free_tier": True,
        "primary_audience": "Researchers and Google Workspace power users needing immense context windows and native Google integration",
        "platforms": ["Web", "Android", "iOS", "API"],
        "core_positioning": "Google's flagship multimodal AI suite powered by Gemini 1.5 Pro with an industry-leading 2-million-token context",
        "key_capabilities": [
            "Industry-record 2,000,000 token context window capable of analyzing hours of video or full audio files",
            "Deep native integration with Google Workspace (Docs, Gmail, Drive, YouTube)",
            "Multimodal comprehension across audio, video, code, and high-res documents",
            "Includes 2TB Google One cloud storage with monthly subscription"
        ],
        "strengths": [
            "Unrivaled context length handles 1-hour videos and 50,000 lines of code without chunking",
            "Bundled 2TB Google One storage provides exceptional ecosystem consumer value",
            "Superior native multimodal processing of raw video and audio files"
        ],
        "trade_offs": [
            "Coding benchmark adherence can occasionally lag behind Claude 3.5 Sonnet on intricate edge cases",
            "Workspace extensions can occasionally experience retrieval latency on large shared drives"
        ],
        "verdict_context": "The undisputed king of long-context document and video ingestion, paired with unmatched Google Workspace synergy",
        "url": "https://gemini.google.com"
    },
    {
        "id": "perplexity-ai",
        "name": "Perplexity Pro",
        "slug": "perplexity-ai",
        "category": "LLM",
        "pricing_model": "Freemium",
        "starting_price": "$20/mo",
        "free_tier": True,
        "primary_audience": "Market analysts, investigative researchers, and students seeking cited, real-time factual synthesis",
        "platforms": ["Web", "iOS", "Android", "Mac", "Chrome Extension", "API"],
        "core_positioning": "Premium AI answer engine combining real-time multi-source web synthesis with flexible frontier model routing",
        "key_capabilities": [
            "Pro Search performing multi-step query decomposition and deep web synthesis",
            "Flexible model switching (Claude 3.5 Sonnet, GPT-4o, Sonar Large 32k)",
            "Interactive Collections workspace with document upload and citation tracking",
            "Generates verified inline clickable citations for every factual claim"
        ],
        "strengths": [
            "Eliminates blue-link search browsing with structured, cited executive summaries",
            "Verifiable citations drastically reduce hallucination risk for enterprise research",
            "Includes $5/mo API credits and access to third-party frontier models in one plan"
        ],
        "trade_offs": [
            "Pro search query rate limits apply on heavy continuous research sessions",
            "Not designed for autonomous multi-file software engineering or artifact compilation"
        ],
        "verdict_context": "The most reliable tool for factual online research, completely replacing traditional search engines with synthesized answers",
        "url": "https://perplexity.ai"
    },
    {
        "id": "deepseek",
        "name": "DeepSeek",
        "slug": "deepseek",
        "category": "LLM",
        "pricing_model": "Free & Open Source",
        "starting_price": "$0",
        "free_tier": True,
        "primary_audience": "Developers, AI researchers, and enterprises seeking open-weights reasoning parity at ultra-low inference costs",
        "platforms": ["Web", "iOS", "Android", "API", "Local Hardware"],
        "core_positioning": "Open-weight frontier model family (DeepSeek-V3 / DeepSeek-R1) delivering parity with top proprietary LLMs at 95% lower cost",
        "key_capabilities": [
            "DeepSeek-V3 671B MoE architecture with 37B active parameters for high inference efficiency",
            "DeepSeek-R1 open-weights reasoning model with explicit chain-of-thought verification",
            "Massive context processing (128k tokens) with ultra-affordable developer API rates ($0.14/M input)",
            "Completely open model weights allowing private on-premise enterprise hosting"
        ],
        "strengths": [
            "Phenomenal cost-to-performance ratio (over 90% cheaper than OpenAI/Anthropic APIs)",
            "DeepSeek-R1 matches OpenAI o1 reasoning and math benchmarks openly",
            "Free web and mobile chat interface with no mandatory subscription tier"
        ],
        "trade_offs": [
            "Cloud chat service occasionally experiences server congestion during viral peak traffic",
            "Running DeepSeek-R1 locally requires heavy cluster hardware (multi-GPU 80GB VRAM) unless heavily quantized"
        ],
        "verdict_context": "A disruptive open-weights breakthrough that brings frontier-class reasoning and coding to developers virtually for free",
        "url": "https://deepseek.com"
    },

    # -------------------------------------------------------------
    # 3. Image AI
    # -------------------------------------------------------------
    {
        "id": "midjourney",
        "name": "Midjourney v6",
        "slug": "midjourney",
        "category": "Image AI",
        "pricing_model": "Paid Only",
        "starting_price": "$10/mo",
        "free_tier": False,
        "primary_audience": "Concept artists, creative directors, and digital marketers demanding broadcast-ready visual aesthetics",
        "platforms": ["Web", "Discord"],
        "core_positioning": "State-of-the-art AI image generator renowned for distinct artistic aesthetics, cinematic lighting, and fine prompt fidelity",
        "key_capabilities": [
            "v6.1 photorealistic rendering engine with intricate skin, textile, and lighting textures",
            "Character Reference (--cref) and Style Reference (--sref) consistency tags",
            "Web interface canvas editor with brush inpainting and Pan/Zoom outpainting",
            "Advanced parameter steering (--stylize, --chaos, --weird, --ar)"
        ],
        "strengths": [
            "Unrivaled default artistic aesthetic and photorealistic composition",
            "Consistent character generation across diverse scenes using reference parameters",
            "Vibrant community showcase and curated prompt inspiration gallery"
        ],
        "trade_offs": [
            "No permanent free tier or trial credits available",
            "Discord-based legacy workflow can still feel cumbersome compared to pure web studios"
        ],
        "verdict_context": "The creative industry leader for cinematic realism, visual beauty, and artistic direction",
        "url": "https://midjourney.com"
    },
    {
        "id": "flux-1",
        "name": "FLUX.1 [dev/pro]",
        "slug": "flux-1",
        "category": "Image AI",
        "pricing_model": "Freemium",
        "starting_price": "$0",
        "free_tier": True,
        "primary_audience": "Technical artists, developers, and studios wanting open-weight control with commercial-grade fidelity",
        "platforms": ["Web", "API", "ComfyUI", "Local GPU"],
        "core_positioning": "12-billion-parameter open-weight rectified flow transformer setting the open-source image synthesis standard",
        "key_capabilities": [
            "12B parameter hybrid flow-transformer architecture developed by the original Stable Diffusion creators",
            "State-of-the-art anatomy rendering with flawless 5-finger hands and complex poses",
            "Exceptional typography and text rendering inside generated images",
            "Available across Schnell (open fast), Dev (non-commercial open), and Pro (commercial API) tiers"
        ],
        "strengths": [
            "Flawless text generation and complex spatial prompt adherence",
            "Open weights available for local execution with extensive ComfyUI LoRA ecosystem",
            "Matches or surpasses Midjourney v6 in anatomical realism and realistic skin textures"
        ],
        "trade_offs": [
            "Dev model requires significant GPU VRAM (16GB+ for optimal quantization)",
            "Official Pro API pricing can add up for high-volume commercial batch generation"
        ],
        "verdict_context": "The new open-weight standard, rivaling proprietary studio generators in photorealism and typographic precision",
        "url": "https://blackforestlabs.ai"
    },
    {
        "id": "ideogram",
        "name": "Ideogram 2.0",
        "slug": "ideogram",
        "category": "Image AI",
        "pricing_model": "Freemium",
        "starting_price": "$8/mo",
        "free_tier": True,
        "primary_audience": "Graphic designers, print-on-demand sellers, and marketers creating logos, typography, and promotional posters",
        "platforms": ["Web", "iOS", "Android", "API"],
        "core_positioning": "Industry benchmark image generator for typographic accuracy, graphic design, and T-shirt/logo creation",
        "key_capabilities": [
            "Flawless spelling and multiline graphic design typography rendering",
            "Realistic, Design, 3D, and Anime style rendering engines",
            "Color palette controls ensuring brand color consistency in generated graphics",
            "Daily recurring free credits for standard generation"
        ],
        "strengths": [
            "Best-in-class text and typography rendering inside posters, merchandise, and logos",
            "Deep understanding of graphic design layout principles and negative space",
            "Generous free tier with daily credit refreshes"
        ],
        "trade_offs": [
            "Photorealistic human skin textures can occasionally feel slightly smoothed compared to Midjourney v6",
            "Prompt adherence for non-English typography is less consistent"
        ],
        "verdict_context": "Unbeatable for typography, graphic posters, and apparel designs where text legibility is non-negotiable",
        "url": "https://ideogram.ai"
    },
    {
        "id": "recraft",
        "name": "Recraft",
        "slug": "recraft",
        "category": "Image AI",
        "pricing_model": "Freemium",
        "starting_price": "$20/mo",
        "free_tier": True,
        "primary_audience": "UI/UX designers, brand managers, and vector illustrators needing editable SVGs and icon systems",
        "platforms": ["Web", "Mac", "API"],
        "core_positioning": "Professional AI design canvas generating native vector art (SVG), 3D graphics, and brand-consistent design sets",
        "key_capabilities": [
            "Native infinite SVG vector export with clean bezier curves and editable paths",
            "Brand palette enforcement maintaining corporate color hex codes across generations",
            "Infinite 2D canvas with vector inpainting, background removal, and vectorization",
            "Style curation maintaining uniform icon and illustration sets for UI/UX"
        ],
        "strengths": [
            "Generates clean, production-ready SVG files that can be edited in Figma or Illustrator",
            "Brand color palette locking guarantees enterprise visual identity compliance",
            "Exceptional tool for web designers creating matching UI icon sets and isometric illustrations"
        ],
        "trade_offs": [
            "Not optimized for cinematic photorealism compared to Midjourney or FLUX.1",
            "Vector generation requires paid tiers for high-resolution commercial vector downloads"
        ],
        "verdict_context": "The indispensable design studio tool for native vector (SVG) generation and brand-consistent digital asset systems",
        "url": "https://recraft.ai"
    },

    # -------------------------------------------------------------
    # 4. Video & Animation AI
    # -------------------------------------------------------------
    {
        "id": "hailuo-ai",
        "name": "Hailuo AI / MiniMax",
        "slug": "hailuo-ai",
        "category": "Video AI",
        "pricing_model": "Freemium",
        "starting_price": "$10/mo",
        "free_tier": True,
        "primary_audience": "Cinematographers, VFX creators, and digital advertisers seeking peak physical motion realism",
        "platforms": ["Web", "API"],
        "core_positioning": "Breakthrough video generation model by MiniMax delivering cinematic photorealism and dynamic camera velocity",
        "key_capabilities": [
            "6-second 1080p video generation with natural lighting and cinematic camera sweeps",
            "High physical consistency preventing character anatomy distortion during rapid movement",
            "Image-to-Video and Text-to-Video with nuanced emotion expression",
            "Low prompt sensitivity (interprets natural descriptive prompts without complex tags)"
        ],
        "strengths": [
            "Produces some of the most lifelike human facial micro-expressions and movement fluidity in the industry",
            "Very high visual fidelity with minimal temporal warping or blur",
            "Generous free trial credits for rapid iteration"
        ],
        "trade_offs": [
            "Maximum single clip length is currently limited to 6 seconds per generation",
            "Server queue times can extend during peak global traffic periods"
        ],
        "verdict_context": "Sets the highest standard for facial motion realism and dynamic cinematic camera tracking in AI video",
        "url": "https://hailuoai.video"
    },
    {
        "id": "pika",
        "name": "Pika 2.0",
        "slug": "pika",
        "category": "Video AI",
        "pricing_model": "Freemium",
        "starting_price": "$10/mo",
        "free_tier": True,
        "primary_audience": "Social media creators, meme producers, and animators seeking creative physics effects and synchronized audio",
        "platforms": ["Web", "Discord"],
        "core_positioning": "Creative video ideation platform featuring Pikaffects physics modifications and synchronized sound effects",
        "key_capabilities": [
            "Pikaffects physical transformations (Melt, Inflate, Crush, Explode, Squish)",
            "Lip-sync and automated audio/sound effects generation synced to video actions",
            "Camera movement controls (pan, zoom, tilt) and regional inpainting (Modify Region)",
            "Video extension, canvas expansion, and seamless looping tools"
        ],
        "strengths": [
            "Viral special effects (Pikaffects) unlock creative possibilities unavailable in traditional video models",
            "Integrated audio and sound effects eliminate the need for separate audio sourcing",
            "Highly accessible intuitive web interface suited for rapid social media creation"
        ],
        "trade_offs": [
            "Realistic human skin and long-form narrative consistency lag behind Runway Gen-3 and Kling AI",
            "Credit consumption can be rapid when experimenting with physics effects"
        ],
        "verdict_context": "The most playful and creative AI video platform, perfect for physics effects, memes, and audio-reactive clips",
        "url": "https://pika.art"
    },
    {
        "id": "kling-ai",
        "name": "Kling AI",
        "slug": "kling-ai",
        "category": "Video AI",
        "pricing_model": "Freemium",
        "starting_price": "$10/mo",
        "free_tier": True,
        "primary_audience": "Video editors, digital marketers, and narrative filmmakers needing longer cinematic shots and physical realism",
        "platforms": ["Web", "API"],
        "core_positioning": "Cinematic video model capable of generating continuous 2-minute clips with complex physical simulation",
        "key_capabilities": [
            "Generates continuous video clips up to 2 minutes with strong narrative coherence",
            "1080p rendering at smooth 30fps with 3D Spatiotemporal Attention",
            "Camera trajectory control, motion brush, and start/end keyframe interpolation",
            "Lip-sync avatar generation and custom motion trajectory steering"
        ],
        "strengths": [
            "Industry-leading continuous clip length (up to 2 minutes vs 5-10s industry norm)",
            "Superior physical simulation handling complex object collisions and fluid dynamics",
            "Daily free check-in credits enable continuous experimentation"
        ],
        "trade_offs": [
            "High render queue times on free tier during peak hours",
            "Western payment methods can occasionally require specific card processors"
        ],
        "verdict_context": "The best choice for filmmakers requiring longer continuous scenes and realistic physical interaction",
        "url": "https://klingai.com"
    },

    # -------------------------------------------------------------
    # 5. Audio & Music AI
    # -------------------------------------------------------------
    {
        "id": "suno-ai",
        "name": "Suno v3.5",
        "slug": "suno-ai",
        "category": "Music AI",
        "pricing_model": "Freemium",
        "starting_price": "$8/mo",
        "free_tier": True,
        "primary_audience": "Content creators, songwriters, and marketing teams needing instant original broadcast music",
        "platforms": ["Web", "iOS", "Android", "Discord"],
        "core_positioning": "Breakthrough music model generating full commercial-quality songs with vocals, lyrics, and arrangements from text",
        "key_capabilities": [
            "v3.5 audio engine producing complete 2 to 4-minute structured songs in seconds",
            "Custom Mode for user-supplied lyrics, specific verse-chorus arrangements, and genre tags",
            "Audio Stem Separation to isolate vocal tracks, drums, and instrumental stems",
            "Song extension, style remixing, and audio crop editing tools"
        ],
        "strengths": [
            "Incredible melodic catchiness and vocal emotional expression across hundreds of genres",
            "Generates full multi-minute songs with complete song architecture in one pass",
            "Generous daily free credits renew continuously for personal creation"
        ],
        "trade_offs": [
            "Dense multi-instrument arrangements can exhibit subtle audio compression artifacts",
            "Commercial exploitation rights are restricted exclusively to active paid subscriptions"
        ],
        "verdict_context": "The ultimate 1-click full-song generation engine for radio-catchy hooks and vocal arrangements",
        "url": "https://suno.com"
    },
    {
        "id": "udio",
        "name": "Udio",
        "slug": "udio",
        "category": "Music AI",
        "pricing_model": "Freemium",
        "starting_price": "$10/mo",
        "free_tier": True,
        "primary_audience": "Music producers, sound designers, and musicians demanding pristine audio mixing and granular structural control",
        "platforms": ["Web"],
        "core_positioning": "Studio-grade generative music platform renowned for acoustic fidelity, stereo mixing, and granular stem inpainting",
        "key_capabilities": [
            "v1.5 high-definition audio synthesis with wide dynamic range and pristine acoustic depth",
            "Audio Inpainting for surgical replacement of specific vocal lines or instrumental bars",
            "Section-by-section arrangement builder (Intro, Verse, Chorus, Solo, Outro)",
            "Audio-to-Audio remixing and external sample upload extension"
        ],
        "strengths": [
            "Superior audio mastering clarity, stereo separation, and acoustic depth compared to competitors",
            "Audio inpainting provides granular control over individual measures and flawed notes",
            "Precise prompt handling for obscure micro-genres and BPM/key signatures"
        ],
        "trade_offs": [
            "Song creation requires a multi-step iterative extension workflow rather than instant 1-click generation",
            "Vocal styling can occasionally require multiple rerolls to match exact expectations"
        ],
        "verdict_context": "The producer's choice for studio-grade audio mastering, complex musical genres, and surgical measure editing",
        "url": "https://udio.com"
    },
    {
        "id": "cartesia-sonic",
        "name": "Cartesia Sonic",
        "slug": "cartesia-sonic",
        "category": "Voice AI",
        "pricing_model": "Freemium",
        "starting_price": "$5/mo",
        "free_tier": True,
        "primary_audience": "Developers and enterprise engineering teams building real-time conversational voice agents and low-latency phone bots",
        "platforms": ["Web", "API", "WebSocket", "Python SDK"],
        "core_positioning": "Ultra-low-latency state-space voice synthesis model delivering sub-100ms streaming text-to-speech",
        "key_capabilities": [
            "Proprietary State Space Model (SSM) architecture delivering ultra-fast ~100ms time-to-first-audio",
            "Multilingual natural voice generation across English, Spanish, French, German, and Japanese",
            "Low-latency WebSocket streaming API tailored for real-time conversational voice agents",
            "Instant voice cloning from clean audio samples under 10 seconds"
        ],
        "strengths": [
            "Sub-100ms latency makes it the fastest voice model for interactive AI call centers and agents",
            "Significantly lower compute overhead and streaming bandwidth than traditional diffusion voice models",
            "High emotional consistency and natural cadence during conversational interruptions"
        ],
        "trade_offs": [
            "Community voice library is more curated and smaller than ElevenLabs' massive marketplace",
            "Specialized voice acting and dramatic whispering effects are less extensive than ElevenLabs PVC"
        ],
        "verdict_context": "The fastest speech synthesis model on the market, engineered specifically for real-time conversational agents",
        "url": "https://cartesia.ai"
    }
]

# Merge logic:
# For each tool in UPDATED_AND_NEW_TOOLS:
# If exists in tools_by_id, update with new specs
# If new, add to tools_by_id
for item in UPDATED_AND_NEW_TOOLS:
    tool_id = item["id"]
    if tool_id in tools_by_id:
        # Merge, keeping existing fields if not overwritten, and ensuring new schema fields are present
        tools_by_id[tool_id].update(item)
    else:
        # New tool
        tools_by_id[tool_id] = item

# Ensure EVERY tool has both User Schema and Astro Schema fields
for tool in tools_by_id.values():
    # Align aliases
    if "primary_audience" not in tool and "best_for" in tool:
        tool["primary_audience"] = tool["best_for"]
    if "best_for" not in tool and "primary_audience" in tool:
        tool["best_for"] = tool["primary_audience"]

    if "platforms" not in tool and "supported_platforms" in tool:
        tool["platforms"] = tool["supported_platforms"]
    if "supported_platforms" not in tool and "platforms" in tool:
        tool["supported_platforms"] = tool["platforms"]

    if "core_positioning" not in tool and "tagline" in tool:
        tool["core_positioning"] = tool["tagline"]
    if "tagline" not in tool and "core_positioning" in tool:
        tool["tagline"] = tool["core_positioning"]

    if "key_capabilities" not in tool and "key_features" in tool:
        tool["key_capabilities"] = tool["key_features"]
    if "key_features" not in tool and "key_capabilities" in tool:
        tool["key_features"] = tool["key_capabilities"]

    if "strengths" not in tool and "pros" in tool:
        tool["strengths"] = tool["pros"]
    if "pros" not in tool and "strengths" in tool:
        tool["pros"] = tool["strengths"]

    if "trade_offs" not in tool and "cons" in tool:
        tool["trade_offs"] = tool["cons"]
    if "cons" not in tool and "trade_offs" in tool:
        tool["cons"] = tool["trade_offs"]

    if "verdict_context" not in tool:
        tool["verdict_context"] = f"Top-tier solution for {tool.get('best_for', 'modern AI workflows')}"

    if "url" not in tool and "affiliate_url" in tool:
        tool["url"] = tool["affiliate_url"]
    if "affiliate_url" not in tool and "url" in tool:
        tool["affiliate_url"] = tool["url"]

# Sort tools stably by category, then by id
final_tools = list(tools_by_id.values())
final_tools.sort(key=lambda t: (t.get("category", ""), t.get("id", "")))

print(f"Total tools after merge: {len(final_tools)}")

# Save to data/tools.json
data_tools_path.parent.mkdir(parents=True, exist_ok=True)
with open(data_tools_path, "w", encoding="utf-8") as f:
    json.dump(final_tools, f, indent=2, ensure_ascii=False)
print(f"Successfully wrote to {data_tools_path}")

# Save to src/data/tools.json
src_data_tools_path = project_root / "src" / "data" / "tools.json"
src_data_tools_path.parent.mkdir(parents=True, exist_ok=True)
with open(src_data_tools_path, "w", encoding="utf-8") as f:
    json.dump(final_tools, f, indent=2, ensure_ascii=False)
print(f"Successfully wrote to {src_data_tools_path}")
