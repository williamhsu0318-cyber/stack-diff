/**
 * src/utils/specEngine.ts
 * ============================================================================
 * StackDiff Spec & Comparison Engine
 * Bottom-of-Funnel (BOFU) data normalizer, structured schema provider,
 * and Pair-Specific Differentiator Engine ("Why the Difference Matters").
 * ============================================================================
 */

import type { ToolData } from '../types/tool';
export type { ToolData };

export interface ToolSpec {
  name: string;
  slug: string;
  logoUrl?: string;
  startingPrice: string;
  billingModel: string;
  affiliateUrl: string;
  officialPricingUrl: string;
  sourceUrl: string;
  lastCheckedAt: string;
  tiersSummary?: string;
  currentModels?: string[];
  telemetryPrivacy?: boolean;
  offlineSupport?: boolean;
  idealForBullets: string[];
  specs: {
    freeTier: string;
    byokSupport: boolean;
    openSource: boolean;
    contextOrModel: string;
    teamCollab: boolean;
    apiAvailable: boolean;
  };
  gotchas: string[];
}

export interface PairDifferentiator {
  coreBattle: string;
  whyItMatters: {
    title: string;
    description: string;
  }[];
  decisiveQuestion: string;
}

export interface ComparisonData {
  toolA: ToolSpec;
  toolB: ToolSpec;
  category: string;
  statusLabel: string;
  lastCheckedDate: string;
  differentiator: PairDifferentiator;
}

// Curated spec catalog for known tools in StackDiff ecosystem
const CURATED_SPECS: Record<string, Partial<ToolSpec>> = {
  cursor: {
    billingModel: 'Seat-based ($20/mo Pro)',
    officialPricingUrl: 'https://docs.cursor.com/getting-started/pricing',
    idealForBullets: [
      'You require autonomous multi-file Composer edits with instant accept/reject diffs',
      'You need complete VS Code extension, keybinding, and settings parity with zero friction',
    ],
    specs: {
      freeTier: 'Hobby plan: 14-day Pro trial + 50 slow requests/mo',
      byokSupport: true,
      openSource: false,
      contextOrModel: 'Claude 3.7 Sonnet, Claude 3.5 Sonnet, GPT-4o, OpenAI o1, Composer 2.5',
      teamCollab: true,
      apiAvailable: false,
    },
    gotchas: [
      'Pro plan includes 500 fast premium requests/mo; subsequent requests enter pool or incur optional $0.10/req usage fees.',
      'Requires running a standalone VS Code fork rather than a standard editor extension.',
      'BYOK usage bypasses fast request limits but incurs direct API billing from your model provider.',
    ],
  },
  'github-copilot': {
    billingModel: 'Seat-based ($10/mo Individual / $19/user Business)',
    officialPricingUrl: 'https://github.com/features/copilot#pricing',
    idealForBullets: [
      'Your organization requires centralized GitHub Enterprise billing and IP copyright indemnity',
      'You want unobtrusive inline ghost-text completions embedded across VS Code, JetBrains, or Neovim',
    ],
    specs: {
      freeTier: 'Copilot Free: 2,000 completions and 50 chat messages/mo; 30-day individual trial',
      byokSupport: false,
      openSource: false,
      contextOrModel: 'Claude 3.7 Sonnet, Claude 3.5 Sonnet, GPT-4o, OpenAI o1, Gemini 2.0 Flash',
      teamCollab: true,
      apiAvailable: true,
    },
    gotchas: [
      'Zero BYOK support; developers cannot connect external private API keys or unvetted local weights.',
      'Multi-file whole-codebase autonomous refactoring is significantly less integrated than dedicated agentic IDEs like Cursor.',
      'Copilot Free tier is limited to 50 chat prompts/mo and only operates within VS Code.',
    ],
  },
  windsurf: {
    billingModel: 'Seat-based ($15/mo Pro)',
    officialPricingUrl: 'https://codeium.com/pricing',
    idealForBullets: [
      'You want agentic flow state powered by Codeium\'s multi-file Cascade engine',
      'You need a modern AI-first IDE with unlimited completions at a lower price point than Cursor ($15 vs $20)',
    ],
    specs: {
      freeTier: 'Free tier with unlimited standard completions and basic Cascade chat',
      byokSupport: false,
      openSource: false,
      contextOrModel: 'Cascade Flow Engine, Claude 3.7 Sonnet, Claude 3.5 Sonnet, GPT-4o',
      teamCollab: true,
      apiAvailable: true,
    },
    gotchas: [
      'Cascade autonomous agent executions consume credit units that cap heavy daily workflows.',
      'Community extension ecosystem lags slightly behind the official VS Code marketplace.',
      'Does not offer open BYOK API key integration on the standard Pro tier.',
    ],
  },
  'v0-by-vercel': {
    billingModel: 'Credit/Usage subscription ($20/mo)',
    officialPricingUrl: 'https://v0.dev/pricing',
    idealForBullets: [
      'You need production-ready Next.js, React, and Tailwind UI components in seconds',
      'You want live interactive component previews and rapid image/Figma-to-code synthesis',
    ],
    specs: {
      freeTier: 'Free plan with 200 monthly credits and public creations',
      byokSupport: false,
      openSource: false,
      contextOrModel: 'v0 Component Engine, Claude 3.7 Sonnet, Specialized Tailwind LLM',
      teamCollab: true,
      apiAvailable: true,
    },
    gotchas: [
      'Credits burn rapidly during complex multi-turn visual design iterations.',
      'Generates frontend markup and CSS; backend business logic and database queries must be created manually.',
      'Paid credits do not roll over to subsequent billing cycles.',
    ],
  },
  lovable: {
    billingModel: 'Credit-based ($20/mo Starter)',
    officialPricingUrl: 'https://lovable.dev/pricing',
    idealForBullets: [
      'You want full-stack web applications generated from text prompts in under 60 seconds',
      'You require native Supabase authentication, database schema binding, and GitHub synchronization',
    ],
    specs: {
      freeTier: 'Free trial credits for initial workspace exploration',
      byokSupport: false,
      openSource: false,
      contextOrModel: 'Lovable Architect Engine, Claude 3.7 Sonnet, GPT-4o',
      teamCollab: true,
      apiAvailable: false,
    },
    gotchas: [
      'Autonomous generation steps consume credits at a rapid pace on complex full-stack apps.',
      'Advanced database relationships and custom SQL functions require manual Supabase adjustments.',
      'Requires active subscription to export clean production builds without platform branding.',
    ],
  },
  chatgpt: {
    billingModel: 'Seat-based ($20/mo Plus / $200/mo Pro)',
    officialPricingUrl: 'https://openai.com/chatgpt/pricing',
    idealForBullets: [
      'You need access to OpenAI\'s frontier reasoning models (o1, o3-mini) and Advanced Voice Mode',
      'You want built-in web browsing, Canvas interactive code workspace, and custom GPTs',
    ],
    specs: {
      freeTier: 'Free tier with GPT-4o mini and dynamic GPT-4o rate limits',
      byokSupport: false,
      openSource: false,
      contextOrModel: 'GPT-4o, OpenAI o1, OpenAI o3-mini, GPT-4o mini, Advanced Voice Mode',
      teamCollab: true,
      apiAvailable: true,
    },
    gotchas: [
      'Plus ($20/mo) has dynamic usage caps on OpenAI o1 reasoning model; heavy researchers require Pro ($200/mo) for unlimited reasoning.',
      'Web client and mobile app do not support BYOK (must use separate OpenAI Developer Platform API billing).',
      'Team plan requires minimum 2 seats billed annually or monthly.',
    ],
  },
  claude: {
    billingModel: 'Seat-based ($20/mo Pro / $25/user Team)',
    officialPricingUrl: 'https://www.anthropic.com/pricing',
    idealForBullets: [
      'You want benchmark-leading hybrid reasoning, nuanced prose, and live Artifacts prototyping',
      'You rely on interactive Artifacts for instant frontend rendering and 200k token Projects',
    ],
    specs: {
      freeTier: 'Free access with dynamic demand-based message limits',
      byokSupport: true,
      openSource: false,
      contextOrModel: 'Claude 3.7 Sonnet (Hybrid Reasoning), Claude 3.5 Sonnet, Claude 3.5 Haiku',
      teamCollab: true,
      apiAvailable: true,
    },
    gotchas: [
      'Message limits reset every 5 hours and can be exhausted within 20–30 long coding prompts.',
      'Does not offer native sandboxed Python terminal execution or image generation in the standard chat UI.',
      'Team plan requires a mandatory 5-user minimum commitment ($125/mo).',
    ],
  },
  gemini: {
    billingModel: 'Google One Bundle ($19.99/mo)',
    officialPricingUrl: 'https://one.google.com/about/plans',
    idealForBullets: [
      'You need a massive 1,000,000 to 2,000,000 token context window for full-repository ingestion',
      'You want deep Google Workspace integration (Docs, Gmail, Drive) and 2TB cloud storage included',
    ],
    specs: {
      freeTier: 'Free Gemini tier powered by Gemini 2.0 Flash and 1.5 Flash',
      byokSupport: false,
      openSource: false,
      contextOrModel: 'Gemini 2.0 Flash, Gemini 1.5 Pro (2M context), Gemini 1.5 Flash',
      teamCollab: true,
      apiAvailable: true,
    },
    gotchas: [
      'Billed strictly through Google One 2TB AI Premium; cannot purchase standalone without cloud storage bundle.',
      'Developer API credits are NOT included in the Google One AI Premium $19.99/mo bundle.',
      'Advanced reasoning responses can lean conservative on ambiguous non-technical creative queries.',
    ],
  },
  deepseek: {
    billingModel: 'Usage-based (Extremely low-cost API)',
    officialPricingUrl: 'https://platform.deepseek.com/api-docs/pricing',
    idealForBullets: [
      'You require state-of-the-art reasoning at 90%+ lower API cost than western frontier labs',
      'You want open weights (MIT license) for unencumbered self-hosted private deployments',
    ],
    specs: {
      freeTier: 'Free web chat access & 5M API tokens for new developer accounts',
      byokSupport: true,
      openSource: true,
      contextOrModel: 'DeepSeek-R1 (Reasoning), DeepSeek-V3 (Base 671B MoE)',
      teamCollab: false,
      apiAvailable: true,
    },
    gotchas: [
      'Public web interface encounters frequent peak-hour server capacity congestion.',
      'Native context window is 64k tokens, smaller than Gemini\'s 2M or Claude\'s 200k.',
      'Self-hosting full 671B model requires enterprise multi-GPU server clusters (8x H100).',
    ],
  },
  perplexity: {
    billingModel: 'Subscription ($20/mo Pro)',
    officialPricingUrl: 'https://www.perplexity.ai/pro',
    idealForBullets: [
      'You want real-time verified web citations and multi-model switching (Claude, GPT-4o, Sonar)',
      'You want deep multi-source research synthesis without ad clutter or SEO spam',
    ],
    specs: {
      freeTier: 'Free unlimited standard search + 5 Pro searches daily',
      byokSupport: false,
      openSource: false,
      contextOrModel: 'Sonar Reasoning, Claude 3.7 Sonnet, GPT-4o, DeepSeek-R1',
      teamCollab: true,
      apiAvailable: true,
    },
    gotchas: [
      'Engineered for search and intelligence discovery rather than interactive multi-file code editing.',
      'Pro plan includes 300+ Pro queries per day; heavy enterprise users may hit daily throttles.',
    ],
  },
  midjourney: {
    billingModel: 'Subscription GPU Hours ($10 - $120/mo)',
    officialPricingUrl: 'https://docs.midjourney.com/docs/plans',
    idealForBullets: [
      'You require photorealistic textures, cinematic lighting, and industry-benchmark aesthetic style',
      'You want standalone Web UI parameter controls alongside Discord server integration',
    ],
    specs: {
      freeTier: 'No permanent free trial; paid plan required',
      byokSupport: false,
      openSource: false,
      contextOrModel: 'Midjourney v6.1, Midjourney v7 Alpha, Niji 6',
      teamCollab: true,
      apiAvailable: false,
    },
    gotchas: [
      'Basic ($10/mo) and Standard ($30/mo) plans publicly post all your creations to the community gallery.',
      'Private image generation (Stealth Mode) is locked behind the $60/month Pro tier.',
      'No official public REST API; programmatic automation requires unofficial third-party wrappers.',
    ],
  },
  flux: {
    billingModel: 'Open weights / Pay-per-image API',
    officialPricingUrl: 'https://blackforestlabs.ai',
    idealForBullets: [
      'You need crisp legible typography, realistic human anatomy, and zero proprietary lock-in',
      'You want to run models locally on 16GB+ VRAM or via ultra-fast serverless APIs (Fal.ai, Replicate)',
    ],
    specs: {
      freeTier: 'FLUX.1 [schnell] is 100% Apache 2.0 open source',
      byokSupport: true,
      openSource: true,
      contextOrModel: 'FLUX.1 [pro], FLUX.1 [dev], FLUX.1 [schnell]',
      teamCollab: false,
      apiAvailable: true,
    },
    gotchas: [
      'Local execution of FLUX.1 [dev] requires high-end hardware (minimum 16GB–24GB VRAM).',
      'FLUX.1 [dev] license is strictly non-commercial; commercial usage requires [pro] API or custom licensing.',
      'Official platform does not offer an all-in-one web UI as polished as Midjourney web.',
    ],
  },
  recraft: {
    billingModel: 'Credit-based ($20/mo Basic)',
    officialPricingUrl: 'https://www.recraft.ai/pricing',
    idealForBullets: [
      'You need native clean vector graphics (SVG) with minimal anchor points and palette controls',
      'You want brand-consistent 3D icons, illustrations, and marketing art kits',
    ],
    specs: {
      freeTier: 'Free tier includes 50 daily credits with public generations',
      byokSupport: false,
      openSource: false,
      contextOrModel: 'Recraft V3 (Red_Panda), Recraft 20B Vector Engine',
      teamCollab: true,
      apiAvailable: true,
    },
    gotchas: [
      'Free tier creations are publicly displayed in the gallery and cannot be kept private.',
      'Vector editing tools consume fast credits rapidly during fine-grained path manipulation.',
    ],
  },
  ideogram: {
    billingModel: 'Subscription / Priority Credits ($8/mo Basic)',
    officialPricingUrl: 'https://ideogram.ai/pricing',
    idealForBullets: [
      'You need perfect in-image typography and complex graphic design posters',
      'You want Magic Prompt automatic expansion and granular HEX color palette enforcement',
    ],
    specs: {
      freeTier: 'Free tier with 10 slow credits per day (40 images/day)',
      byokSupport: false,
      openSource: false,
      contextOrModel: 'Ideogram 2.0, Ideogram 2.0 Turbo, Magic Fill',
      teamCollab: true,
      apiAvailable: true,
    },
    gotchas: [
      'Basic tier ($8/mo) generations remain public in community feed; private mode requires Plus ($20/mo).',
      'Photorealism on complex cinematic environmental scenes trails Midjourney v6.1 slightly.',
    ],
  },
  runway: {
    billingModel: 'Credit-based ($15/mo Standard)',
    officialPricingUrl: 'https://runwayml.com/pricing',
    idealForBullets: [
      'You need cinematic AI video generation powered by Gen-3 Alpha and Gen-3 Alpha Turbo',
      'You want Act-One facial performance capture transferring real expressions onto characters',
    ],
    specs: {
      freeTier: 'Free plan includes one-time 125 non-renewable generation credits',
      byokSupport: false,
      openSource: false,
      contextOrModel: 'Gen-3 Alpha, Gen-3 Alpha Turbo, Act-One',
      teamCollab: true,
      apiAvailable: true,
    },
    gotchas: [
      'Standard plan credits (625/mo) deplete quickly (Gen-3 Alpha costs 10 credits/sec of generated video).',
      'Credits do not roll over past subscription billing cycle caps.',
      'Watermarking is removed only on paid Standard ($15/mo) and Pro ($35/mo) tiers.',
    ],
  },
  kling: {
    billingModel: 'Credit-based ($10/mo Standard)',
    officialPricingUrl: 'https://klingai.com/pricing',
    idealForBullets: [
      'You need explosive human movement, realistic physics simulation, and 10-second continuous clips',
      'You want 66 free daily credits every single day without entering a credit card',
    ],
    specs: {
      freeTier: 'Free plan provides 66 renewable daily credits (~6 video generations/day)',
      byokSupport: false,
      openSource: false,
      contextOrModel: 'Kling 1.5 Pro, Kling 1.0 High-Performance',
      teamCollab: false,
      apiAvailable: true,
    },
    gotchas: [
      'Professional Mode generations take 3-8 minutes during peak global server queues.',
      'Free tier renders with watermark and limits video exports to 720p.',
    ],
  },
  luma: {
    billingModel: 'Credit-based ($9.99/mo Standard)',
    officialPricingUrl: 'https://lumalabs.ai/dream-machine/pricing',
    idealForBullets: [
      'You need rapid 3D camera orbits, crane shots, and spatial awareness in under 120 seconds',
      'You want keyframe-to-keyframe smooth interpolation for continuous storyboarding',
    ],
    specs: {
      freeTier: 'Free plan provides 30 monthly generations with standard queue priority',
      byokSupport: false,
      openSource: false,
      contextOrModel: 'Dream Machine 1.5, Photon Spatial Engine',
      teamCollab: false,
      apiAvailable: true,
    },
    gotchas: [
      'Free tier generations enter shared public queues that experience latency during peak periods.',
      'Commercial rights and unwatermarked exports require paid Standard ($9.99/mo) tier or higher.',
    ],
  },
  heygen: {
    billingModel: 'Credit-based ($29/mo Creator)',
    officialPricingUrl: 'https://heygen.com/pricing',
    idealForBullets: [
      'You require studio-grade digital avatars with natural micro-expressions and eye contact',
      'You want automated multi-language video translation with matching lip-sync dubbing',
    ],
    specs: {
      freeTier: 'Free trial includes 1 credit (1 minute of video) with HeyGen branding',
      byokSupport: false,
      openSource: false,
      contextOrModel: 'HeyGen Avatar 3.0, Video Translate Engine, Interactive Avatar API',
      teamCollab: true,
      apiAvailable: true,
    },
    gotchas: [
      'Creator plan ($29/mo) allocates only 15 minutes of total video per month ($1.93 per minute).',
      'Unused monthly credits on Creator tier do not roll over to subsequent months.',
    ],
  },
  elevenlabs: {
    billingModel: 'Character-based ($5/mo Starter)',
    officialPricingUrl: 'https://elevenlabs.io/pricing',
    idealForBullets: [
      'You require nuanced emotional inflection, whisper/laughter control, and 32+ language dubbing',
      'You want Instant and Professional Voice Cloning from 1-minute audio samples',
    ],
    specs: {
      freeTier: 'Free plan includes 10,000 characters/mo (approx. 10 mins of audio) with attribution',
      byokSupport: false,
      openSource: false,
      contextOrModel: 'Eleven Multilingual v2, Eleven Flash v2.5, Conversational AI 2.0',
      teamCollab: true,
      apiAvailable: true,
    },
    gotchas: [
      'Character usage counts spaces and punctuation; long scripts consume monthly allowances quickly.',
      'Free tier strictly mandates ElevenLabs attribution in published commercial projects.',
    ],
  },
  cartesia: {
    billingModel: 'Usage / Audio Seconds ($0.075/min)',
    officialPricingUrl: 'https://cartesia.ai/pricing',
    idealForBullets: [
      'You are building live conversational voicebots requiring sub-100ms streaming latency',
      'You want transparent pay-as-you-go per-second audio metering rather than character bundles',
    ],
    specs: {
      freeTier: 'Free tier includes $5 free API credits for sandbox development',
      byokSupport: true,
      openSource: false,
      contextOrModel: 'Sonic (State Space Model), Sonic Multilingual, Sonic Fast',
      teamCollab: true,
      apiAvailable: true,
    },
    gotchas: [
      'Focused strictly on developer API streaming; lacks an end-user timeline audio editing suite.',
      'Smaller pre-made voice library compared to ElevenLabs\' community voice marketplace.',
    ],
  },
  n8n: {
    billingModel: 'Free self-hosted / $20/mo Cloud',
    officialPricingUrl: 'https://n8n.io/pricing',
    idealForBullets: [
      'You want unlimited free automations running privately on your own Docker or Kubernetes server',
      'You need first-class LangChain AI Agent nodes with tool calling and vector memory',
    ],
    specs: {
      freeTier: '100% free forever when self-hosted on your own server or Docker container',
      byokSupport: true,
      openSource: true,
      contextOrModel: 'n8n AI Agent Framework, LangChain Connectors, Python & JS Nodes',
      teamCollab: true,
      apiAvailable: true,
    },
    gotchas: [
      'Self-hosting requires maintaining your own Docker container, PostgreSQL database, and SSL certificates.',
      'Cloud plans enforce monthly execution caps; high-frequency webhooks can exhaust tier quotas.',
    ],
  },
  make: {
    billingModel: 'Usage-based ($9/mo Core for 10k ops)',
    officialPricingUrl: 'https://www.make.com/en/pricing',
    idealForBullets: [
      'You need visual routers, iterators, and aggregators for multi-branch JSON data mapping',
      'You want cost efficiency with pay-per-operation pricing ($9/mo for 10,000 operations)',
    ],
    specs: {
      freeTier: 'Free plan includes 1,000 operations/mo and 2 active scenarios',
      byokSupport: true,
      openSource: false,
      contextOrModel: 'Make Scenario Engine v2, Native AI Assistant Modules, Webhook Connectors',
      teamCollab: true,
      apiAvailable: true,
    },
    gotchas: [
      'Every single module action and iteration counts as 1 operation; misconfigured loops can burn 10k ops in minutes.',
      'Free tier is restricted to 15-minute polling intervals on scheduled triggers.',
    ],
  },
  zapier: {
    billingModel: 'Usage-based ($19.99/mo Professional for 750 tasks)',
    officialPricingUrl: 'https://zapier.com/pricing',
    idealForBullets: [
      'You want zero-code integrations across 6,000+ certified SaaS enterprise applications',
      'You want Zapier Central autonomous AI agents executing tasks across your connected accounts',
    ],
    specs: {
      freeTier: 'Free tier includes 100 tasks/mo with 2-step single Zaps',
      byokSupport: true,
      openSource: false,
      contextOrModel: 'Zapier Central AI Engine, Zapier Tables & Interfaces, Code by Zapier',
      teamCollab: true,
      apiAvailable: true,
    },
    gotchas: [
      'Task-based pricing scales steeply on high-volume background pipelines compared to self-hosted alternatives.',
      'Free tier only permits simple 2-step Zaps; multi-step workflows require Professional ($19.99/mo).',
    ],
  },
};

// Backward compatibility alias bindings
CURATED_SPECS['claude-3-5-sonnet'] = CURATED_SPECS['claude'];
CURATED_SPECS['gemini-advanced'] = CURATED_SPECS['gemini'];
CURATED_SPECS['perplexity-ai'] = CURATED_SPECS['perplexity'];
CURATED_SPECS['flux-1'] = CURATED_SPECS['flux'];
CURATED_SPECS['runway-gen3'] = CURATED_SPECS['runway'];
CURATED_SPECS['kling-ai'] = CURATED_SPECS['kling'];
CURATED_SPECS['luma-dream-machine'] = CURATED_SPECS['luma'];
CURATED_SPECS['cartesia-sonic'] = CURATED_SPECS['cartesia'];

// ============================================================================
// PAIR-SPECIFIC DIFFERENTIATORS ("Why the Difference Matters")
// ============================================================================
const PAIR_DIFFERENTIATORS: Record<string, PairDifferentiator> = {
  'cursor-vs-windsurf': {
    coreBattle: 'Composer 2.5 Multi-File Agent vs. Cascade Collaborative Flow State',
    whyItMatters: [
      {
        title: 'Multi-File Editing Architecture',
        description: 'Cursor Composer directly modifies project files and presents an instant side-by-side diff review across multiple files simultaneously. Windsurf Cascade integrates terminal command execution and file edits in a unified conversational thread.',
      },
      {
        title: 'Pricing & Credit Economy',
        description: 'Cursor costs $20/mo and gives 500 fast premium requests before dropping to a slow queue or requiring BYOK. Windsurf costs $15/mo with 500 prompt credits but includes unlimited Supercomplete code completions.',
      },
      {
        title: 'BYOK API Flexibility',
        description: 'Cursor allows plugging in your own Anthropic or OpenAI API keys directly to bypass rate limits. Windsurf does not support BYOK on its standard tier.',
      },
    ],
    decisiveQuestion: 'Do you want full control over your models via BYOK and Composer diffs (Cursor), or an all-in-one flow state with unlimited autocomplete for $5/mo less (Windsurf)?',
  },

  'cursor-vs-github-copilot': {
    coreBattle: 'Autonomous Whole-Codebase Agent vs. Enterprise Inline Code Completion',
    whyItMatters: [
      {
        title: 'Editor Portability vs. Custom IDE Fork',
        description: 'Cursor requires switching to a standalone VS Code fork. GitHub Copilot works natively across VS Code, JetBrains (IntelliJ, PyCharm), Visual Studio, and Neovim.',
      },
      {
        title: 'Scope of Codebase Refactoring',
        description: 'Cursor semantic index (@codebase) indexes your whole repository to rewrite 10+ files autonomously in seconds. Copilot excels at inline ghost-text completions and localized Copilot Chat.',
      },
      {
        title: 'Enterprise Indemnity & Compliance',
        description: 'GitHub Copilot provides full IP copyright indemnity, SOC2 compliance, and centralized seat management. Cursor is favored by agile startups and individual power engineers.',
      },
    ],
    decisiveQuestion: 'Are you building solo or in a fast-moving team needing agentic multi-file refactoring (Cursor), or in an enterprise requiring strict IP protection across JetBrains/VS Code (Copilot)?',
  },

  'chatgpt-vs-claude': {
    coreBattle: 'OpenAI Frontier Reasoning (o1/o3-mini) & Multimodal Tools vs. Claude 3.7 Hybrid Reasoning & Live Artifacts',
    whyItMatters: [
      {
        title: 'Reasoning & Coding Benchmarks',
        description: 'Claude 3.7 Sonnet introduces toggleable hybrid reasoning and benchmark-leading coding architecture. OpenAI o1/o3-mini provides world-class mathematical proofs and multi-step algorithmic planning.',
      },
      {
        title: 'Interactive Prototyping vs. Sandboxed Tools',
        description: 'Claude features Artifacts to render live React components, SVG diagrams, and HTML web apps directly in chat. ChatGPT features sandboxed Python execution, Advanced Voice Mode, and image generation.',
      },
      {
        title: 'Context Window & Ingestion',
        description: 'Claude provides a reliable 200,000 token context window and Projects knowledge hubs. ChatGPT provides 128,000 tokens with custom GPT configuration.',
      },
    ],
    decisiveQuestion: 'Do you prioritize live UI artifact rendering, clean code architecture, and 200k context (Claude Pro), or Python execution, live voice conversations, and OpenAI reasoning (ChatGPT Plus)?',
  },

  'chatgpt-vs-gemini': {
    coreBattle: 'Tool-Dense Ecosystem & OpenAI Reasoning vs. 2,000,000 Token Context & Google Workspace Synergy',
    whyItMatters: [
      {
        title: 'Massive Context Window',
        description: 'Gemini Advanced provides an industry-leading 2M token context window—capable of analyzing 1 hour of video, 60,000 lines of code, or entire books in a single prompt. ChatGPT caps out at 128K tokens.',
      },
      {
        title: 'Ecosystem & Cloud Storage Bundle',
        description: 'Gemini Advanced ($19.99/mo) comes bundled with 2TB of Google One cloud storage and deep Docs/Gmail integration. ChatGPT Plus ($20/mo) focuses exclusively on standalone AI capabilities.',
      },
      {
        title: 'Coding & Algorithmic Precision',
        description: 'ChatGPT with o1 and GPT-4o provides sharper precision on dense coding and edge cases, whereas Gemini can be conservative with guardrails.',
      },
    ],
    decisiveQuestion: 'Do you need to ingest massive multi-megabyte repositories, audio, and video files inside Google Workspace (Gemini), or do you need precision reasoning models and custom GPTs (ChatGPT)?',
  },

  'chatgpt-vs-deepseek': {
    coreBattle: 'Turnkey Hosted Frontier Suite vs. 90% Cheaper Open-Weight Reasoning',
    whyItMatters: [
      {
        title: 'Cost & Economics',
        description: 'DeepSeek-R1 and V3 cost as little as $0.14-$0.55 per million tokens (and $0.014 with cache hits)—nearly 90-95% cheaper than OpenAI\'s commercial API. DeepSeek\'s web chat is completely free.',
      },
      {
        title: 'Open Weights vs. Proprietary Walled Garden',
        description: 'DeepSeek models are open-weights under the MIT license, allowing private on-premise hosting (via Ollama or vLLM). ChatGPT is completely proprietary.',
      },
      {
        title: 'Infrastructure Reliability & Multimodal',
        description: 'ChatGPT Plus offers rock-solid cloud uptime, Advanced Voice Mode, and DALL-E integration. DeepSeek\'s public web servers suffer from peak-hour traffic limits.',
      },
    ],
    decisiveQuestion: 'Do you want unencumbered open weights and near-zero API inference costs (DeepSeek), or a reliable, multimodal hosted platform with voice and Python sandboxes (ChatGPT)?',
  },

  'flux-vs-midjourney': {
    coreBattle: 'Open-Weight ComfyUI Control & Legible Text vs. Proprietary Cinematic Aesthetics',
    whyItMatters: [
      {
        title: 'Typography & In-Image Text',
        description: 'FLUX.1 is renowned for rendering perfectly spelled, crisp in-image text on posters, labels, and apparel. Midjourney handles short text well, but FLUX remains superior for typographic design.',
      },
      {
        title: 'Aesthetic Coherence & Skin Textures',
        description: 'Midjourney remains the gold standard for effortless photorealistic skin pores, cinematic cinematic lighting, and atmospheric artistic flair straight out of the box.',
      },
      {
        title: 'Licensing & Local Pipelines',
        description: 'FLUX.1 [schnell] is open-source (Apache 2.0) and can run locally on an RTX 3090/4090 with ControlNet/LoRA. Midjourney is strictly closed-source and Discord/Web hosted.',
      },
    ],
    decisiveQuestion: 'Do you want local GPU control, custom LoRA pipelines, and crisp typography (FLUX), or instant world-class cinematic photorealism with zero setup (Midjourney)?',
  },

  'kling-vs-runway': {
    coreBattle: 'High-Motion Dynamic Physics & Long Durations vs. Cinematic VFX Camera Controls & Facial Capture',
    whyItMatters: [
      {
        title: 'Motion Dynamism & Complex Physics',
        description: 'Kling 1.5 excels at dramatic human action, athletic movements, and complex physical interactions with realistic mass. Runway Gen-3 Alpha leans toward smoother cinematic camera pans.',
      },
      {
        title: 'Facial Performance & Acting',
        description: 'Runway\'s Act-One feature allows creators to record a webcam video of their face and map the performance directly onto generated characters. Kling lacks native facial motion transfer.',
      },
      {
        title: 'Clip Duration & Free Tier',
        description: 'Kling can generate up to 10-second continuous clips and provides 66 free daily credits. Runway limits standard generations to 5-10 seconds and consumes credits rapidly.',
      },
    ],
    decisiveQuestion: 'Do you need actor facial motion transfer and director-level camera steering (Runway), or explosive physical motion, 10-second clips, and generous free credits (Kling AI)?',
  },

  'cartesia-vs-elevenlabs': {
    coreBattle: 'Sub-100ms Streaming State Space Model vs. Rich Emotional Prosody & Voice Marketplace',
    whyItMatters: [
      {
        title: 'Streaming Latency',
        description: 'Cartesia Sonic uses a State Space Model (SSM) architecture delivering sub-100ms time-to-first-byte audio chunks—critical for real-time conversational telephony. ElevenLabs Flash operates around 75-150ms.',
      },
      {
        title: 'Emotional Range & Storytelling',
        description: 'ElevenLabs Multilingual v2 has peerless expressive prosody, dramatic whispers, laughter, and an enormous public voice library for audiobooks and media.',
      },
      {
        title: 'Pricing & Metering',
        description: 'Cartesia charges strictly per audio second ($0.075/min). ElevenLabs meters by character count (including spaces and punctuation).',
      },
    ],
    decisiveQuestion: 'Are you building live conversational call bots where every millisecond of latency counts (Cartesia), or producing high-production audiobooks, games, and videos needing rich emotion (ElevenLabs)?',
  },

  'make-vs-n8n': {
    coreBattle: 'Hosted Visual Integration Cloud vs. Self-Hosted Privacy & LangChain AI Agents',
    whyItMatters: [
      {
        title: 'Data Privacy & Deployment',
        description: 'n8n offers a free self-hosted edition (Fair-Code) that can run in private Docker/Kubernetes environments with zero data leakage. Make is strictly SaaS-hosted.',
      },
      {
        title: 'AI Agent & LangChain Nodes',
        description: 'n8n provides first-class AI Agent nodes, memory stores, and vector database integrations. Make uses native AI modules and HTTP webhooks.',
      },
      {
        title: 'Cost Scaling',
        description: 'Make charges per individual module operation ($9/mo for 10k ops). n8n Cloud charges per full workflow execution ($20/mo for 2.5k executions), making high-step workflows far cheaper on n8n.',
      },
    ],
    decisiveQuestion: 'Do you need self-hosted data compliance and complex AI agent workflows (n8n), or a polished cloud visual scenario builder for SaaS business operations (Make)?',
  },

  'make-vs-zapier': {
    coreBattle: 'Granular Multi-Branch Data Transformations vs. 6,000+ Turnkey Enterprise App Connectors',
    whyItMatters: [
      {
        title: 'Pricing & Billing Economics',
        description: 'Make gives you 10,000 operations for $9/mo. Zapier charges $19.99/mo for only 750 tasks. High-volume data synchronization can be 5x-10x cheaper on Make.',
      },
      {
        title: 'Visual Logic Complexity',
        description: 'Make\'s visual router/iterator canvas is vastly superior for complex nested JSON data mapping and error handling. Zapier\'s linear paths are easier for beginners.',
      },
      {
        title: 'Enterprise & App Ecosystem',
        description: 'Zapier integrates with over 6,000 SaaS apps—often with deeper pre-certified triggers—and features Zapier Central autonomous agents.',
      },
    ],
    decisiveQuestion: 'Do you need cost efficiency on high-volume multi-step data pipelines (Make), or zero-friction non-technical integrations across niche enterprise SaaS tools (Zapier)?',
  },
};

/**
 * Dynamic fallback generator for pairs not explicitly hardcoded.
 */
function generateDynamicDifferentiator(
  toolA: ToolSpec,
  toolB: ToolSpec,
  category: string
): PairDifferentiator {
  const whyItMatters = [
    {
      title: 'Commercial Tiers & Billing Structure',
      description: `${toolA.name} begins at ${toolA.startingPrice} (${toolA.billingModel}), while ${toolB.name} operates at ${toolB.startingPrice} (${toolB.billingModel}). Evaluate your team's monthly request volume against potential seat vs. usage scaling costs.`,
    },
    {
      title: 'BYOK & Infrastructure Control',
      description: `${toolA.name} is ${toolA.specs.byokSupport ? 'BYOK-compatible (bring your own API keys)' : 'a bundled proprietary environment'}, whereas ${toolB.name} is ${toolB.specs.byokSupport ? 'BYOK-compatible' : 'a bundled proprietary environment'}. This impacts rate limits and vendor lock-in.`,
    },
    {
      title: 'Model & Architecture Focus',
      description: `${toolA.name} leverages ${toolA.specs.contextOrModel}, compared to ${toolB.name}'s ${toolB.specs.contextOrModel}. Match this against your latency and reasoning needs in ${category}.`,
    },
  ];

  return {
    coreBattle: `${toolA.name} vs. ${toolB.name} Architectural & Pricing Differentiators`,
    whyItMatters,
    decisiveQuestion: `Do your workflows require ${toolA.name}'s specific ecosystem, or does ${toolB.name}'s pricing model and feature set offer better unit economics for your stack?`,
  };
}

/**
 * Resolves the pair differentiator for a given pairing.
 */
function resolvePairDifferentiator(
  toolA: ToolSpec,
  toolB: ToolSpec,
  category: string
): PairDifferentiator {
  const pairKey1 = `${toolA.slug}-vs-${toolB.slug}`;
  const pairKey2 = `${toolB.slug}-vs-${toolA.slug}`;

  if (PAIR_DIFFERENTIATORS[pairKey1]) {
    return PAIR_DIFFERENTIATORS[pairKey1];
  }
  if (PAIR_DIFFERENTIATORS[pairKey2]) {
    return PAIR_DIFFERENTIATORS[pairKey2];
  }

  return generateDynamicDifferentiator(toolA, toolB, category);
}

/**
 * Normalizes any raw tool object into a standard ToolSpec.
 */
export function normalizeToolSpec(raw: any): ToolSpec {
  if (!raw) {
    throw new Error('normalizeToolSpec received null or undefined raw tool data.');
  }

  const id = (raw.slug || raw.id || '').toLowerCase();
  const curated = CURATED_SPECS[id] || {};
  const techSpecs = raw.technical_specs || {};
  const pricing = raw.pricing || {};

  const startingPrice =
    pricing.starting_price ||
    raw.starting_price ||
    curated.startingPrice ||
    'Custom';

  const billingModel =
    pricing.billing_model ||
    raw.pricing_model ||
    curated.billingModel ||
    'Subscription';

  const tiersSummary =
    pricing.tiers_summary ||
    raw.tiers_summary ||
    curated.tiersSummary;

  const affiliateUrl =
    raw.affiliate_url ||
    raw.official_website ||
    raw.official_url ||
    raw.url ||
    '#';

  const officialPricingUrl =
    raw.official_pricing_url ||
    raw.pricing_url ||
    curated.officialPricingUrl ||
    raw.official_url ||
    raw.url ||
    raw.affiliate_url ||
    '#';

  const sourceUrl =
    raw.source_url ||
    (curated as any).sourceUrl ||
    officialPricingUrl;

  const lastCheckedAt =
    raw.last_checked_at ||
    (curated as any).lastCheckedAt ||
    '2026-09-30';

  const idealForBullets: string[] = raw.ideal_for_bullets || curated.idealForBullets || [
    raw.best_for ? `Best fit for ${raw.best_for.toLowerCase()}` : `Engineered specifically for modern ${raw.category} workflows`,
    (raw.strengths && raw.strengths[0]) || (raw.pros && raw.pros[0]) || 'Offers verified commercial reliability and active community support',
  ];

  const currentModels: string[] | undefined =
    techSpecs.current_models ||
    (curated as any).currentModels;

  const telemetryPrivacy: boolean | undefined =
    techSpecs.telemetry_privacy ??
    (curated as any).telemetryPrivacy;

  const offlineSupport: boolean | undefined =
    techSpecs.offline_support ??
    (curated as any).offlineSupport;

  const freeTier =
    pricing.free_tier_details ||
    raw.free_tier_details ||
    curated.specs?.freeTier ||
    (raw.free_tier ? 'Free tier / trial available' : 'Paid only (No permanent free tier)');

  const byokSupport =
    techSpecs.byok_support ??
    raw.byok_support ??
    curated.specs?.byokSupport ??
    (raw.category === 'Coding AI' || raw.category === 'Workflow AI' || id.includes('deepseek'));

  const openSource =
    techSpecs.open_source ??
    raw.open_source ??
    curated.specs?.openSource ??
    (id.includes('flux') || id.includes('stable-diffusion') || id.includes('n8n') || id.includes('deepseek') || id.includes('whisper'));

  const contextOrModel =
    (currentModels && currentModels.length > 0 ? currentModels.slice(0, 3).join(', ') : null) ||
    raw.context_or_model ||
    curated.specs?.contextOrModel ||
    (raw.key_capabilities && raw.key_capabilities[0]) ||
    (raw.key_features && raw.key_features[0]) ||
    'Frontier AI orchestration';

  const teamCollab = raw.team_collab ?? curated.specs?.teamCollab ?? true;
  const apiAvailable = raw.api_available ?? curated.specs?.apiAvailable ?? true;

  const rawGotchas = (raw.trade_offs || raw.cons || []).slice(0, 2);
  const gotchas: string[] =
    raw.gotchas ||
    raw.pricing_gotchas ||
    curated.gotchas ||
    [
      ...rawGotchas,
      `Advertised ${startingPrice} base pricing may scale upward depending on team seat tiers and heavy monthly usage.`,
    ];

  return {
    name: raw.name || id,
    slug: raw.slug || id,
    logoUrl: raw.logoUrl,
    startingPrice,
    billingModel,
    affiliateUrl,
    officialPricingUrl,
    sourceUrl,
    lastCheckedAt,
    tiersSummary,
    currentModels,
    telemetryPrivacy,
    offlineSupport,
    idealForBullets: idealForBullets.slice(0, 2),
    specs: {
      freeTier,
      byokSupport,
      openSource,
      contextOrModel,
      teamCollab,
      apiAvailable,
    },
    gotchas: gotchas.slice(0, 3),
  };
}

/**
 * Builds standard ComparisonData with Pair-Specific Differentiator.
 */
export function buildComparisonData(
  toolARaw: any,
  toolBRaw: any,
  category: string
): ComparisonData {
  const toolA = normalizeToolSpec(toolARaw);
  const toolB = normalizeToolSpec(toolBRaw);

  // Status label - objective data state
  const statusLabel = 'Specs Snapshot';
  const lastCheckedDate = toolA.lastCheckedAt || toolB.lastCheckedAt || '2026-09-30';

  const differentiator = resolvePairDifferentiator(toolA, toolB, category);

  return {
    toolA,
    toolB,
    category,
    statusLabel,
    lastCheckedDate,
    differentiator,
  };
}

/**
 * Computes all pairwise comparison static paths for Astro.
 */
export function getComparisonStaticPaths(toolsData: any[]) {
  const categoryMap = new Map<string, any[]>();
  for (const tool of toolsData) {
    if (!categoryMap.has(tool.category)) {
      categoryMap.set(tool.category, []);
    }
    categoryMap.get(tool.category)!.push(tool);
  }

  const paths = [];

  for (const [category, groupTools] of categoryMap.entries()) {
    if (groupTools.length < 2) continue;

    for (let i = 0; i < groupTools.length; i++) {
      for (let j = i + 1; j < groupTools.length; j++) {
        const item1 = groupTools[i];
        const item2 = groupTools[j];

        const [toolA, toolB] = [item1, item2].sort((a, b) =>
          a.slug.localeCompare(b.slug)
        );

        const slug = `${toolA.slug}-vs-${toolB.slug}`;

        const siblingTools = groupTools.filter(
          (t) => t.id !== toolA.id && t.id !== toolB.id
        );

        paths.push({
          params: { slug },
          props: {
            toolA,
            toolB,
            category,
            siblingTools,
            allCategoryTools: groupTools,
          },
        });
      }
    }
  }

  return paths;
}
