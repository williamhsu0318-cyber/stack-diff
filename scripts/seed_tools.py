"""
seed_tools.py
-------------
Seed dataset generator for StackDiff pSEO comparison engine.
Populates and validates 20 top-tier AI tools across multiple categories.
Outputs formatted data to data/tools.json.
"""

import json
from pathlib import Path
from typing import List
from models import AITool


# Complete seed dataset for 20 high-volume global AI tools
RAW_TOOLS_DATA = [
    # 1. ElevenLabs (Voice AI)
    {
        "id": "elevenlabs",
        "name": "ElevenLabs",
        "slug": "elevenlabs",
        "category": "Voice AI",
        "tagline": "Industry-leading AI voice generator, voice cloning, and multilingual speech synthesis platform",
        "pricing_model": "Freemium",
        "starting_price": "$5/mo",
        "free_tier": True,
        "best_for": "Creators, game studios, and developers requiring emotionally rich, hyper-realistic voiceovers",
        "key_features": [
            "Instant and Professional Voice Cloning (PVC)",
            "Multilingual Text-to-Speech across 32+ languages",
            "Automated AI Video Dubbing and Translation",
            "Text-to-Sound Effects Generator (SFX)",
            "Low-latency real-time streaming Conversational AI WebSocket API"
        ],
        "pros": [
            "Unrivaled emotional depth, pacing nuance, and vocal naturalness",
            "Vast community voice library with monetization sharing",
            "Developer-friendly REST and WebSocket APIs with rich SDKs"
        ],
        "cons": [
            "Character generation quotas can deplete fast on long-form audio",
            "Occasional accent artifacts when synthesizing niche non-English dialects"
        ],
        "supported_platforms": ["Web", "API", "iOS", "Android", "Python SDK"],
        "affiliate_url": "https://elevenlabs.io/?via=stackdiff"
    },

    # 2. Edge-TTS (Voice AI)
    {
        "id": "edge-tts",
        "name": "Edge-TTS",
        "slug": "edge-tts",
        "category": "Voice AI",
        "tagline": "Open-source Python library and CLI accessing Microsoft Edge's neural text-to-speech without API keys",
        "pricing_model": "Free & Open Source",
        "starting_price": "$0",
        "free_tier": True,
        "best_for": "Developers, hobbyists, and automation builders looking for 100% free, high-quality multilingual TTS",
        "key_features": [
            "Zero API key, billing account, or Microsoft Azure registration required",
            "Access to hundreds of Microsoft Azure Neural voice models",
            "Precise subtitle, word boundary, and timing metadata generation",
            "Asynchronous Python API alongside an ergonomic CLI tool",
            "Custom pitch, rate, and volume SSML parameter controls"
        ],
        "pros": [
            "Completely free with no credit limits or recurring subscription fees",
            "High synthesis quality powered by Microsoft neural voice models",
            "Lightweight and trivial to integrate into automated backend pipelines"
        ],
        "cons": [
            "Relies on an undocumented reverse-engineered protocol with potential rate limits",
            "Lacks custom voice cloning and advanced emotion-steering sliders"
        ],
        "supported_platforms": ["CLI", "Python Library", "Linux", "Windows", "Mac"],
        "affiliate_url": "https://github.com/rany2/edge-tts"
    },

    # 3. Runway Gen-3 (Video AI)
    {
        "id": "runway-gen3",
        "name": "Runway Gen-3",
        "slug": "runway-gen3",
        "category": "Video AI",
        "tagline": "Pioneering generative video model delivering photorealistic cinematic text-to-video and image-to-video",
        "pricing_model": "Freemium",
        "starting_price": "$12/mo",
        "free_tier": True,
        "best_for": "Filmmakers, VFX artists, and creative agencies producing broadcast-ready cinematic video assets",
        "key_features": [
            "High-fidelity Text-to-Video and Image-to-Video generation (Gen-3 Alpha)",
            "Granular Camera Control (pan, tilt, zoom, orbit, roll)",
            "Motion Brush tool for animating selective regions of static images",
            "Director Mode for fine-tuning camera velocities and motion paths",
            "Keyframe prompting to steer structural narrative transitions"
        ],
        "pros": [
            "Industry-leading temporal consistency and cinematic lighting fidelity",
            "Comprehensive creative suite including inpainting and motion tracking",
            "Precise camera and brush-guided motion steering"
        ],
        "cons": [
            "High credit consumption per second of high-resolution video",
            "Short duration limits per single generation clip"
        ],
        "supported_platforms": ["Web", "iOS", "API"],
        "affiliate_url": "https://runwayml.com"
    },

    # 4. Kling AI (Video AI)
    {
        "id": "kling-ai",
        "name": "Kling AI",
        "slug": "kling-ai",
        "category": "Video AI",
        "tagline": "State-of-the-art video generation model renowned for long cinematic clips and realistic physical motion",
        "pricing_model": "Freemium",
        "starting_price": "$10/mo",
        "free_tier": True,
        "best_for": "Digital marketers, YouTubers, and VFX animators seeking extended video durations and dynamic motion",
        "key_features": [
            "Generates continuous video clips up to 2 minutes with narrative consistency",
            "1080p high-definition rendering at smooth 30fps playback",
            "3D Spatiotemporal Joint Attention mechanism for accurate physical simulation",
            "Image-to-Video with customizable end-frame keyframing",
            "Camera motion controls and motion brush trajectory steering"
        ],
        "pros": [
            "Superb physical dynamics and complex motion simulation without warping",
            "Supports significantly longer continuous generation than western rivals",
            "Generous daily check-in free credits for regular experimentation"
        ],
        "cons": [
            "Server rendering queues can experience delays during peak hours",
            "International payment processing can occasionally require specific cards"
        ],
        "supported_platforms": ["Web", "API"],
        "affiliate_url": "https://klingai.com"
    },

    # 5. Luma Dream Machine (Video AI)
    {
        "id": "luma-dream-machine",
        "name": "Luma Dream Machine",
        "slug": "luma-dream-machine",
        "category": "Video AI",
        "tagline": "Ultra-fast generative video model producing physics-accurate, high-frame-rate cinematic shots",
        "pricing_model": "Freemium",
        "starting_price": "$29.99/mo",
        "free_tier": True,
        "best_for": "Storytellers, animators, and social video creators who prioritize rapid turnaround and fluid motion",
        "key_features": [
            "Rapid 120-frame synthesis in approximately 120 seconds",
            "Direct transformer architecture trained on multimodal video tokens",
            "Keyframe extension for smooth video looping and continuous scene building",
            "Character and object consistency across dynamic camera movements",
            "Custom camera path trajectory prompts and Image-to-Video start frames"
        ],
        "pros": [
            "Extremely fast generation speed compared to legacy diffusion architectures",
            "Smooth natural lighting and realistic physical object interactions",
            "Intuitive prompting without requiring complex technical syntax"
        ],
        "cons": [
            "Rapid character morphing can occasionally occur in chaotic scenes",
            "Higher tier subscription pricing is steep for casual creators"
        ],
        "supported_platforms": ["Web", "API"],
        "affiliate_url": "https://lumalabs.ai/dream-machine"
    },

    # 6. Midjourney (Image AI)
    {
        "id": "midjourney",
        "name": "Midjourney",
        "slug": "midjourney",
        "category": "Image AI",
        "tagline": "State-of-the-art AI image generator renowned for distinct artistic aesthetic and photo-realism",
        "pricing_model": "Paid Only",
        "starting_price": "$10/mo",
        "free_tier": False,
        "best_for": "Concept artists, art directors, UI designers, and marketers needing premium aesthetic visual assets",
        "key_features": [
            "v6 / v6.1 photorealistic rendering engine with intricate texture rendering",
            "Character Reference (--cref) and Style Reference (--sref) consistency tags",
            "Inpainting (Vary Region) and Pan/Zoom Outpainting capabilities",
            "Web interface canvas editor with brush mask selection",
            "Style tuning and personalized aesthetic model profile training"
        ],
        "pros": [
            "Unrivaled aesthetic quality, lighting composition, and artistic flair",
            "Exceptional natural language prompt comprehension",
            "Powerful parameter modifiers for aspect ratio, stylize, and consistency"
        ],
        "cons": [
            "No permanent free tier or free trial credits available",
            "Discord-based workflow can feel clunky for traditional non-technical users"
        ],
        "supported_platforms": ["Web", "Discord"],
        "affiliate_url": "https://midjourney.com"
    },

    # 7. Stable Diffusion (Image AI)
    {
        "id": "stable-diffusion",
        "name": "Stable Diffusion",
        "slug": "stable-diffusion",
        "category": "Image AI",
        "tagline": "The open-source benchmark for local image generation, offering complete pipeline customization and data privacy",
        "pricing_model": "Free & Open Source",
        "starting_price": "$0",
        "free_tier": True,
        "best_for": "Developers, AI researchers, and technical artists who need local offline execution and custom LoRA models",
        "key_features": [
            "Open weights model family (SD 1.5, SDXL, SD 3.5 Large/Medium)",
            "ControlNet integration for precise pose, depth, canny edge, and line art guidance",
            "LoRA and Checkpoint fine-tuning ecosystem for custom character/style training",
            "ComfyUI node-based visual workflow orchestrator and Automatic1111 web UI",
            "Zero cloud telemetry and 100% offline local inference execution"
        ],
        "pros": [
            "Completely free to run locally with zero recurring subscription fees",
            "Infinite extensibility with thousands of community checkpoints and LoRAs",
            "Total privacy for proprietary enterprise and personal creative assets"
        ],
        "cons": [
            "Requires modern dedicated GPU hardware (NVIDIA RTX with ample VRAM)",
            "Steep learning curve for node-based setups and hyperparameter tuning"
        ],
        "supported_platforms": ["Windows", "Linux", "Mac", "API", "Local Hardware"],
        "affiliate_url": "https://stability.ai"
    },

    # 8. ChatGPT (LLM)
    {
        "id": "chatgpt",
        "name": "ChatGPT",
        "slug": "chatgpt",
        "category": "LLM",
        "tagline": "OpenAI's flagship conversational AI assistant featuring advanced multi-step reasoning and multimodal tools",
        "pricing_model": "Freemium",
        "starting_price": "$20/mo",
        "free_tier": True,
        "best_for": "Knowledge workers, software developers, and general consumers needing an all-round versatile AI assistant",
        "key_features": [
            "Access to OpenAI o1 reasoning model and GPT-4o multimodal engine",
            "Advanced Voice Mode with real-time conversational interruption and emotion",
            "Integrated DALL-E 3 image generator and live web browsing capabilities",
            "Code Interpreter / Advanced Data Analysis with sandboxed Python execution",
            "Custom GPT marketplace and memory persistence across conversations"
        ],
        "pros": [
            "Best-in-class multi-modal tool integration in a unified polished interface",
            "Massive ecosystem of custom GPT assistants and community plugins",
            "Fast, reliable mobile and desktop native client apps"
        ],
        "cons": [
            "Usage message caps on flagship reasoning models (o1 and GPT-4o)",
            "Standard conversational tone can feel boilerplate without custom instructions"
        ],
        "supported_platforms": ["Web", "iOS", "Android", "Mac", "Windows", "API"],
        "affiliate_url": "https://chatgpt.com"
    },

    # 9. Claude 3.5 Sonnet (LLM)
    {
        "id": "claude-3-5-sonnet",
        "name": "Claude 3.5 Sonnet",
        "slug": "claude-3-5-sonnet",
        "category": "LLM",
        "tagline": "Anthropic's frontier AI model renowned for superior code generation, nuanced reasoning, and Artifacts workspace",
        "pricing_model": "Freemium",
        "starting_price": "$20/mo",
        "free_tier": True,
        "best_for": "Software engineers, analysts, and writers demanding natural prose and elite coding benchmarks",
        "key_features": [
            "200,000 token context window for ingesting full codebases and books",
            "Artifacts interactive workspace for live React, SVG, HTML, and diagram rendering",
            "Industry-leading code generation, refactoring, and debugging benchmarks",
            "Advanced visual reasoning for interpreting charts, UI mocks, and dense technical PDFs",
            "Projects workspace for organizing persistent context and reference documents"
        ],
        "pros": [
            "Exceptional natural writing cadence and unmatched coding precision",
            "Interactive Artifacts UI revolutionizes front-end and component prototyping",
            "Superior long-context adherence with minimal needle-in-haystack hallucination"
        ],
        "cons": [
            "Free tier enforces strict dynamic hourly message volume limits",
            "Lacks native image generation and real-time web browsing in standard UI"
        ],
        "supported_platforms": ["Web", "iOS", "Android", "Mac", "Windows", "API"],
        "affiliate_url": "https://claude.ai"
    },

    # 10. Cursor (Coding AI)
    {
        "id": "cursor",
        "name": "Cursor",
        "slug": "cursor",
        "category": "Coding AI",
        "tagline": "AI-first code editor fork of VS Code engineered for whole-codebase indexing and autonomous multi-file editing",
        "pricing_model": "Freemium",
        "starting_price": "$20/mo",
        "free_tier": True,
        "best_for": "Software engineers and indie developers wanting autonomous multi-file generation and instant diff reviews",
        "key_features": [
            "Composer multi-file autonomous code generation and automatic diff application",
            "Full codebase semantic indexing and symbol-aware contextual search (@codebase)",
            "Copilot++ intelligent multi-line autocomplete predicting your next edit",
            "Seamless model switching (Claude 3.5 Sonnet, GPT-4o, OpenAI o1)",
            "1-click migration importing all VS Code extensions, keybindings, and settings"
        ],
        "pros": [
            "Effortless multi-file refactoring with clear visual diff accept/reject toggles",
            "Zero learning curve for existing VS Code users",
            "State-of-the-art model orchestration specifically tuned for developer workflows"
        ],
        "cons": [
            "Fast request quotas can deplete quickly during heavy Composer refactors",
            "Requires adopting a standalone IDE application instead of a lightweight plugin"
        ],
        "supported_platforms": ["Mac", "Windows", "Linux"],
        "affiliate_url": "https://cursor.com"
    },

    # 11. GitHub Copilot (Coding AI)
    {
        "id": "github-copilot",
        "name": "GitHub Copilot",
        "slug": "github-copilot",
        "category": "Coding AI",
        "tagline": "The enterprise-standard AI pair programmer seamlessly embedded across all major development IDEs",
        "pricing_model": "Paid Only",
        "starting_price": "$10/mo",
        "free_tier": False,
        "best_for": "Enterprise developers, engineering teams, and JetBrains/Visual Studio users wanting integrated completions",
        "key_features": [
            "Real-time inline ghost-text code completions as you type",
            "Copilot Chat with workspace symbol awareness and explanation features",
            "GitHub.com integration for pull request summaries and code review assistance",
            "Copilot CLI for shell command explanation and generation",
            "Multi-IDE plugin support (VS Code, JetBrains IDEs, Visual Studio, Neovim)"
        ],
        "pros": [
            "Direct native integration in virtually every mainstream IDE without migration",
            "Enterprise-grade security controls, audit logs, and IP copyright indemnity",
            "Low-latency inline completions that blend invisibly into existing typing workflows"
        ],
        "cons": [
            "Whole-codebase autonomous multi-file editing is less agile than Cursor",
            "No free tier for standard users (free only for verified open-source maintainers/students)"
        ],
        "supported_platforms": ["VS Code", "JetBrains", "Visual Studio", "Neovim", "CLI"],
        "affiliate_url": "https://github.com/features/copilot"
    },

    # 12. Perplexity AI (LLM)
    {
        "id": "perplexity-ai",
        "name": "Perplexity AI",
        "slug": "perplexity-ai",
        "category": "LLM",
        "tagline": "Conversational AI search engine delivering cited, real-time web research and synthesized answers",
        "pricing_model": "Freemium",
        "starting_price": "$20/mo",
        "free_tier": True,
        "best_for": "Researchers, students, and executives who need transparent, source-backed answers to complex inquiries",
        "key_features": [
            "Real-time web indexing with direct inline numeric citation links",
            "Pro Search multi-step query decomposition and automated source synthesis",
            "Collections workspace for organizing project research topics and uploading PDFs",
            "Multi-model switching (Claude 3.5 Sonnet, GPT-4o, Sonar Large)",
            "Focus filters (Academic papers, YouTube, Reddit, Writing, Web)"
        ],
        "pros": [
            "Drastically reduces web search time by synthesizing answers instead of blue links",
            "Every statement is backed by verifiable clickable citations to curb hallucinations",
            "Flexible model routing allows leveraging the best LLM for specific research tasks"
        ],
        "cons": [
            "Pro Search queries are restricted on the free tier with a rolling reset",
            "Not optimized for iterative code authoring or sandbox execution"
        ],
        "supported_platforms": ["Web", "iOS", "Android", "Mac", "Chrome Extension", "API"],
        "affiliate_url": "https://perplexity.ai"
    },

    # 13. Descript (Video AI)
    {
        "id": "descript",
        "name": "Descript",
        "slug": "descript",
        "category": "Video AI",
        "tagline": "All-in-one AI audio and video editor that transforms media production into editing a text document",
        "pricing_model": "Freemium",
        "starting_price": "$12/mo",
        "free_tier": True,
        "best_for": "Podcasters, YouTubers, educators, and marketing teams looking to edit video through automated transcripts",
        "key_features": [
            "Transcript-based video and audio editing (delete text to cut video clip)",
            "Studio Sound AI one-click background noise reduction and voice enhancement",
            "AI Eye Contact redirection correcting gaze toward the camera lens",
            "Overdub voice cloning for correcting spoken mistakes by typing text",
            "Automated filler word removal (eradicates 'um', 'uh', and awkward pauses)"
        ],
        "pros": [
            "Revolutionary text-based editing workflow cuts editing hours by over 60%",
            "Studio Sound transforms budget laptop microphones into broadcast-quality audio",
            "Comprehensive built-in screen recorder and 1-click video hosting integration"
        ],
        "cons": [
            "Occasional transcription errors can alter intended cut boundaries",
            "Desktop application can be resource-intensive on older computers"
        ],
        "supported_platforms": ["Mac", "Windows", "Web"],
        "affiliate_url": "https://descript.com"
    },

    # 14. HeyGen (Video AI)
    {
        "id": "heygen",
        "name": "HeyGen",
        "slug": "heygen",
        "category": "Video AI",
        "tagline": "AI video generation platform for producing studio-quality talking avatar videos with automated localization",
        "pricing_model": "Freemium",
        "starting_price": "$29/mo",
        "free_tier": True,
        "best_for": "Sales teams, corporate trainers, and global marketers creating personalized avatar presentations at scale",
        "key_features": [
            "100+ photorealistic Studio and Instant digital human avatars",
            "AI Video Translation with automatic voice cloning and precise lip-sync in 40+ languages",
            "Text-to-Video scene builder with customizable templates and brand kits",
            "Streaming Interactive Avatar API for real-time web customer service",
            "Personal avatar creation from a 2-minute smartphone video recording"
        ],
        "pros": [
            "Natural facial expressions and lip-sync accuracy across multiple languages",
            "Eliminates expensive studio rentals, cameras, and recurring actor fees",
            "Robust REST API allows programmatic batch video generation for marketing campaigns"
        ],
        "cons": [
            "Free tier video render credits are very limited",
            "Complex hand gestures and active physical movements can look static"
        ],
        "supported_platforms": ["Web", "API", "Zapier Integration"],
        "affiliate_url": "https://heygen.com"
    },

    # 15. Suno AI (Music AI)
    {
        "id": "suno-ai",
        "name": "Suno AI",
        "slug": "suno-ai",
        "category": "Music AI",
        "tagline": "Breakthrough generative music model creating full vocal songs, instruments, and commercial tracks from text",
        "pricing_model": "Freemium",
        "starting_price": "$8/mo",
        "free_tier": True,
        "best_for": "Content creators, songwriters, and casual music enthusiasts looking to generate full radio-ready songs",
        "key_features": [
            "v3 / v3.5 audio model synthesizing 2-4 minute complete songs in seconds",
            "Generates full vocals, harmonies, lyrics, and multi-instrument arrangements",
            "Custom Mode allowing user-supplied lyrics, genre tags, and song structures",
            "Audio Stem separation to extract isolated vocals and instrumental backing tracks",
            "Extend and Crop tools for continuing songs or creating seamless remixes"
        ],
        "pros": [
            "Remarkable melodic catchiness and vocal emotional expression across genres",
            "Creates full radio-quality songs with verses, bridges, and choruses in seconds",
            "Generous daily free credits renew continuously for non-commercial experimentation"
        ],
        "cons": [
            "Audio compression artifacts can appear in dense multi-instrument drops",
            "Commercial rights and ownership are restricted exclusively to paid tiers"
        ],
        "supported_platforms": ["Web", "iOS", "Android", "Discord"],
        "affiliate_url": "https://suno.com"
    },

    # 16. Udio (Music AI)
    {
        "id": "udio",
        "name": "Udio",
        "slug": "udio",
        "category": "Music AI",
        "tagline": "High-fidelity generative music platform renowned for studio-grade audio mastering and granular stem control",
        "pricing_model": "Freemium",
        "starting_price": "$10/mo",
        "free_tier": True,
        "best_for": "Music producers, sound designers, and artists seeking pristine audio mixing and granular section editing",
        "key_features": [
            "v1.5 high-definition audio synthesis with wide dynamic frequency range",
            "Audio Inpainting to regenerate specific vocal phrases or instrument segments",
            "Granular Section Extensions (Intro, Verse, Chorus, Solo, Outro)",
            "Audio-to-Audio remixing and external sample upload extension",
            "Advanced prompt descriptors supporting BPM, key signatures, and micro-genres"
        ],
        "pros": [
            "Superior audio mastering clarity, stereo separation, and acoustic depth",
            "Audio inpainting provides surgical repair of individual measures",
            "Flexible musical arrangement control across complex multi-part compositions"
        ],
        "cons": [
            "Full song construction requires an iterative section-by-section workflow",
            "Vocal styling can occasionally require multiple generation rerolls"
        ],
        "supported_platforms": ["Web"],
        "affiliate_url": "https://udio.com"
    },

    # 17. Notion AI (Workflow AI)
    {
        "id": "notion-ai",
        "name": "Notion AI",
        "slug": "notion-ai",
        "category": "Workflow AI",
        "tagline": "Integrated AI assistant embedded directly inside your workspace docs, relational databases, and knowledge wikis",
        "pricing_model": "Paid Only",
        "starting_price": "$10/mo",
        "free_tier": False,
        "best_for": "Teams, project managers, and power note-takers wanting AI-driven writing, database autofill, and enterprise search",
        "key_features": [
            "Q&A enterprise search indexing all connected Notion pages, Slack, and Google Drive",
            "AI Autofill properties automatically extracting metadata into database columns",
            "In-line writing assistant for summarizing, translating, and drafting copy",
            "Automated meeting notes summarization with instant action-item generation",
            "Brainstorming and research synthesis inside private team workspaces"
        ],
        "pros": [
            "Deep native synergy with existing workspace documents, tables, and team wikis",
            "Database Autofill dramatically streamlines repetitive manual data entry",
            "Zero context switching between third-party chat tools and actual workspace documents"
        ],
        "cons": [
            "Requires an existing Notion workspace and costs an extra $10/user/mo add-on",
            "Model parameters are tailored for workplace documents rather than deep code generation"
        ],
        "supported_platforms": ["Web", "Mac", "Windows", "iOS", "Android"],
        "affiliate_url": "https://notion.so"
    },

    # 18. Make (Workflow AI)
    {
        "id": "make",
        "name": "Make",
        "slug": "make",
        "category": "Workflow AI",
        "tagline": "Visual workflow automation platform featuring native AI modules and advanced logic branching",
        "pricing_model": "Freemium",
        "starting_price": "$9/mo",
        "free_tier": True,
        "best_for": "No-code builders, operations managers, and developers orchestrating multi-step AI pipelines and integrations",
        "key_features": [
            "Infinite visual canvas for designing multi-branch workflows with routers",
            "Native OpenAI, Anthropic, and generic REST AI API connectors",
            "Advanced data parsing, array iteration, JSON aggregation, and filtering",
            "Real-time webhook triggers, cron schedules, and custom error handling paths",
            "Execution history inspector with detailed step-by-step payload replay"
        ],
        "pros": [
            "Highly visual drag-and-drop builder handles complex branching with ease",
            "Substantially more cost-effective per operation than traditional competitors",
            "Fine-grained data transformation and error-handling capabilities"
        ],
        "cons": [
            "Slightly steeper initial learning curve than basic single-step automation tools",
            "Complex enterprise scenarios require understanding basic JSON data structures"
        ],
        "supported_platforms": ["Web", "API"],
        "affiliate_url": "https://make.com"
    },

    # 19. Zapier (Workflow AI)
    {
        "id": "zapier",
        "name": "Zapier",
        "slug": "zapier",
        "category": "Workflow AI",
        "tagline": "The market-leading cloud automation platform connecting 6,000+ business apps with built-in AI agents",
        "pricing_model": "Freemium",
        "starting_price": "$19.99/mo",
        "free_tier": True,
        "best_for": "Businesses, marketing teams, and non-technical staff needing instant, no-code integrations across SaaS tools",
        "key_features": [
            "Massive integration ecosystem supporting over 6,000+ cloud applications",
            "Zapier Central autonomous AI agents performing multi-step workspace tasks",
            "AI Copilot for generating end-to-end Zaps from plain English prompts",
            "Zapier Tables and Interfaces for creating custom AI-driven mini-apps",
            "Webhooks, filters, paths, and JavaScript/Python code step execution"
        ],
        "pros": [
            "Unmatched third-party app catalog ensures compatibility with every SaaS tool",
            "Natural language Zap builder allows non-technical users to build automations in seconds",
            "Enterprise-grade reliability, uptime, and SOC2 compliance standards"
        ],
        "cons": [
            "Higher starting price point and costly per-task volume tier upgrades",
            "Multi-step branching and conditional logic require paid tier subscriptions"
        ],
        "supported_platforms": ["Web", "Chrome Extension", "API"],
        "affiliate_url": "https://zapier.com"
    },

    # 20. Whisper (Voice AI)
    {
        "id": "whisper",
        "name": "Whisper",
        "slug": "whisper",
        "category": "Voice AI",
        "tagline": "OpenAI's benchmark open-source automatic speech recognition (ASR) model for robust multilingual transcription",
        "pricing_model": "Free & Open Source",
        "starting_price": "$0",
        "free_tier": True,
        "best_for": "Developers, audio engineers, and privacy-conscious enterprises building offline transcription and subtitle systems",
        "key_features": [
            "Trained on 680,000 hours of multilingual and multitask supervised audio data",
            "Multilingual speech recognition, English translation, and word-level timestamp alignment",
            "Multiple model weight tiers (tiny, base, small, medium, large-v3, large-v3-turbo)",
            "High-performance optimized inference runtimes (faster-whisper, whisper.cpp)",
            "100% offline local inference execution with zero external network calls"
        ],
        "pros": [
            "Industry-leading accuracy even with technical terminology, diverse accents, and background noise",
            "Completely open-source with zero recurring API costs or billing limits",
            "Lightweight C++ and GPU runtimes enable high-throughput real-time transcription"
        ],
        "cons": [
            "Base Python implementation requires GPU acceleration for fast processing",
            "Does not provide real-time multi-speaker diarization out of the box"
        ],
        "supported_platforms": ["Python Library", "CLI", "Windows", "Mac", "Linux", "API"],
        "affiliate_url": "https://github.com/openai/whisper"
    }
]


def seed_and_validate_tools(output_path: Path) -> List[AITool]:
    """
    Validates all raw tool definitions against the Pydantic AITool model
    and serializes the validated dataset into formatted JSON.
    """
    validated_tools: List[AITool] = []

    print("=" * 60)
    print("StackDiff pSEO Engine - Seed Data Generation & Validation")
    print("=" * 60)

    for index, raw_item in enumerate(RAW_TOOLS_DATA, start=1):
        try:
            tool = AITool(**raw_item)
            validated_tools.append(tool)
            print(f"[{index:02d}/20] [VALID] {tool.name:<22} ({tool.category}) -> {tool.slug}")
        except Exception as e:
            print(f"[{index:02d}/20] [ERROR] Failed validating '{raw_item.get('name', 'UNKNOWN')}': {e}")
            raise e

    # Ensure target output directory exists
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Convert Pydantic models to dict and serialize to formatted JSON
    tools_dict_list = [tool.model_dump() for tool in validated_tools]

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(tools_dict_list, f, indent=2, ensure_ascii=False)

    print("\n" + "-" * 60)
    print(f"Successfully validated and saved {len(validated_tools)} AI tools to:")
    print(f"  {output_path.resolve()}")
    print("-" * 60)

    # Print Category Breakdown
    categories = {}
    for t in validated_tools:
        categories[t.category] = categories.get(t.category, 0) + 1

    print("Category Breakdown:")
    for cat, count in sorted(categories.items()):
        print(f"  * {cat:<18}: {count} tools")
    print("=" * 60)

    return validated_tools


if __name__ == "__main__":
    current_dir = Path(__file__).resolve().parent
    project_root = current_dir.parent
    target_json_path = project_root / "data" / "tools.json"

    seed_and_validate_tools(target_json_path)
