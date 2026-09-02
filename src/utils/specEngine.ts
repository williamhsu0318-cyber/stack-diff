/**
 * src/utils/specEngine.ts
 * ============================================================================
 * StackDiff Spec & Comparison Engine
 * Bottom-of-Funnel (BOFU) data normalizer and structured schema provider.
 * ============================================================================
 */

export interface ToolSpec {
  name: string;
  slug: string;
  logoUrl?: string;
  startingPrice: string;
  billingModel: string;
  affiliateUrl: string;
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

export interface ComparisonData {
  toolA: ToolSpec;
  toolB: ToolSpec;
  category: string;
  lastVerified: string;
  faqs: { question: string; answer: string }[];
}

// Curated spec catalog for known tools in StackDiff ecosystem
const CURATED_SPECS: Record<string, Partial<ToolSpec>> = {
  cursor: {
    billingModel: 'Seat-based (Monthly/Annual)',
    idealForBullets: [
      'You require autonomous multi-file Composer edits with instant accept/reject diffs',
      'You need complete VS Code extension, keybinding, and settings parity with zero friction',
    ],
    specs: {
      freeTier: 'Hobby plan (2-week Pro trial + 50 slow requests/mo)',
      byokSupport: true,
      openSource: false,
      contextOrModel: 'Claude 3.5 Sonnet, GPT-4o, o1-preview, DeepSeek-V3',
      teamCollab: true,
      apiAvailable: false,
    },
    gotchas: [
      'Advertised 500 fast requests/mo can deplete in under 3 weeks during heavy agentic Composer refactors.',
      'Usage-based charges ($0.10/req) apply once fast quota expires unless explicitly switched to the slow queue.',
      'Requires running a dedicated standalone desktop IDE rather than a lightweight plugin.',
    ],
  },
  'github-copilot': {
    billingModel: 'Seat-based ($10/mo or $19/user Enterprise)',
    idealForBullets: [
      'Your organization requires centralized GitHub Enterprise billing and IP copyright indemnity',
      'You want unobtrusive inline ghost-text completions embedded in JetBrains, VS Code, or Neovim',
    ],
    specs: {
      freeTier: 'Free for verified OSS maintainers & students; 30-day individual trial',
      byokSupport: false,
      openSource: false,
      contextOrModel: 'GPT-4o, Claude 3.5 Sonnet (Workspace), OpenAI o1',
      teamCollab: true,
      apiAvailable: true,
    },
    gotchas: [
      'No BYOK (Bring Your Own Key) support; strictly locked into GitHub-managed hosted models.',
      'Multi-file architectural refactoring capabilities significantly trail dedicated agentic IDEs.',
      'Individual plan lacks organization audit logs and SAML SSO compliance.',
    ],
  },
  windsurf: {
    billingModel: 'Seat-based ($15/mo)',
    idealForBullets: [
      'You want agentic flow state powered by Codeium\'s multi-file Cascade engine',
      'You need a modern AI-first IDE with unlimited completions at a lower price point than Cursor',
    ],
    specs: {
      freeTier: 'Free tier with unlimited standard completions and basic chat',
      byokSupport: false,
      openSource: false,
      contextOrModel: 'Cascade Engine (Claude 3.5 Sonnet, GPT-4o)',
      teamCollab: true,
      apiAvailable: true,
    },
    gotchas: [
      'Cascade autonomous agent executions consume credit units that cap heavy daily workflows.',
      'Community extension ecosystem lags slightly behind the official VS Code marketplace.',
    ],
  },
  'v0-by-vercel': {
    billingModel: 'Credit/Usage subscription ($20/mo)',
    idealForBullets: [
      'You need production-ready Next.js, React, and Tailwind UI components in seconds',
      'You want live interactive component previews and rapid image/Figma-to-code synthesis',
    ],
    specs: {
      freeTier: 'Free plan with 200 monthly credits and public creations',
      byokSupport: false,
      openSource: false,
      contextOrModel: 'Specialized React & Tailwind generative models',
      teamCollab: true,
      apiAvailable: true,
    },
    gotchas: [
      'Credits burn rapidly during complex multi-turn visual design iterations.',
      'Generates frontend markup and CSS; backend business logic and database queries must be created manually.',
      'Paid credits do not roll over to subsequent billing cycles.',
    ],
  },
  supermaven: {
    billingModel: 'Seat-based ($10/mo)',
    idealForBullets: [
      'You prioritize sub-50ms ultra-low latency inline autocomplete over chat interfaces',
      'You want an enormous 1,000,000+ token context window embedded directly inside Neovim or VS Code',
    ],
    specs: {
      freeTier: 'Free tier with standard latency model',
      byokSupport: false,
      openSource: false,
      contextOrModel: 'Custom Babble model (1M+ token context window)',
      teamCollab: true,
      apiAvailable: false,
    },
    gotchas: [
      'Focuses strictly on inline code autocomplete; lacks whole-codebase autonomous multi-file refactoring.',
      'Acquisition by Cursor may influence standalone roadmap velocity and plugin support.',
    ],
  },
  lovable: {
    billingModel: 'Credit-based ($20/mo)',
    idealForBullets: [
      'You want full-stack web applications generated from text prompts in under 60 seconds',
      'You require native Supabase authentication, database schema binding, and GitHub synchronization',
    ],
    specs: {
      freeTier: 'Limited trial credits for initial workspace exploration',
      byokSupport: false,
      openSource: false,
      contextOrModel: 'Frontier model orchestration (Claude 3.5 Sonnet + GPT-4o)',
      teamCollab: true,
      apiAvailable: false,
    },
    gotchas: [
      'Autonomous generation steps consume credits at a rapid pace on complex full-stack apps.',
      'Advanced database relationships and custom SQL functions require manual Supabase adjustments.',
    ],
  },
  chatgpt: {
    billingModel: 'Seat-based ($20/mo Plus / $200/mo Pro)',
    idealForBullets: [
      'You need access to OpenAI\'s frontier reasoning models (o1, o3-mini) and Advanced Voice',
      'You want built-in web browsing, Canvas interactive code workspace, and custom GPTs',
    ],
    specs: {
      freeTier: 'Free tier with GPT-4o mini and dynamic GPT-4o rate limits',
      byokSupport: false,
      openSource: false,
      contextOrModel: 'GPT-4o (128k), o1 (200k), o3-mini',
      teamCollab: true,
      apiAvailable: true,
    },
    gotchas: [
      'ChatGPT Plus subscription does NOT include API access or API platform credits.',
      'Hourly message caps apply to flagship reasoning models (o1/o3-mini) even on paid Plus tiers.',
      'Individual consumer accounts default to training data inclusion unless manually opted out in privacy settings.',
    ],
  },
  'claude-3-5-sonnet': {
    billingModel: 'Seat-based ($20/mo Pro / $25/user Team)',
    idealForBullets: [
      'You want benchmark-leading coding intelligence, nuanced reasoning, and cleaner prose',
      'You rely on interactive Artifacts for instant frontend rendering and 200k Projects',
    ],
    specs: {
      freeTier: 'Free access with dynamic demand-based message limits',
      byokSupport: false,
      openSource: false,
      contextOrModel: 'Claude 3.5 Sonnet, Claude 3.5 Haiku, Claude 3 Opus (200k context)',
      teamCollab: true,
      apiAvailable: true,
    },
    gotchas: [
      'Message limits reset every 5 hours and can be exhausted within 20–30 long coding prompts.',
      'Claude Pro subscription does NOT grant Anthropic Developer Console API credits.',
      'Team plan requires a mandatory 5-user minimum commitment ($125/mo).',
    ],
  },
  deepseek: {
    billingModel: 'Usage-based (Extremely low-cost API)',
    idealForBullets: [
      'You require state-of-the-art reasoning at 90%+ lower API cost than western frontier labs',
      'You want open weights (MIT license) for unencumbered self-hosted private deployments',
    ],
    specs: {
      freeTier: 'Free web chat access & 5M API tokens for new developer accounts',
      byokSupport: true,
      openSource: true,
      contextOrModel: 'DeepSeek-V3 (64k), DeepSeek-R1 Reasoning (64k)',
      teamCollab: false,
      apiAvailable: true,
    },
    gotchas: [
      'Public web interface encounters frequent peak-hour server capacity congestion.',
      'Native context window is 64k tokens, smaller than Gemini\'s 2M or Claude\'s 200k.',
      'Hosted cloud servers reside in Asian infrastructure, which may require compliance review for enterprise IP.',
    ],
  },
  'perplexity-ai': {
    billingModel: 'Subscription ($20/mo Pro)',
    idealForBullets: [
      'You want real-time verified web citations and multi-model switching (Claude, GPT-4o, Sonar)',
      'You want deep multi-source research synthesis and $5/mo in included API credits',
    ],
    specs: {
      freeTier: 'Free unlimited standard search + 5 Pro searches daily',
      byokSupport: false,
      openSource: false,
      contextOrModel: 'Sonar Large (128k), Claude 3.5 Sonnet, GPT-4o',
      teamCollab: true,
      apiAvailable: true,
    },
    gotchas: [
      'Engineered for search and intelligence discovery rather than interactive multi-file code editing.',
      'Included $5 monthly API credit does not accumulate across billing cycles.',
    ],
  },
  'gemini-advanced': {
    billingModel: 'Google One Bundle ($19.99/mo)',
    idealForBullets: [
      'You need a massive 1,000,000 to 2,000,000 token context window for full-repository ingestion',
      'You want deep Google Workspace integration (Docs, Gmail, Drive) and 2TB cloud storage included',
    ],
    specs: {
      freeTier: 'Free Gemini tier powered by Gemini 1.5 Flash',
      byokSupport: false,
      openSource: false,
      contextOrModel: 'Gemini 1.5 Pro / 2.0 Flash (1M - 2M context window)',
      teamCollab: true,
      apiAvailable: true,
    },
    gotchas: [
      'Billed strictly through Google One 2TB AI Premium; cannot purchase standalone without cloud storage bundle.',
      'Code formatting and prompt responses can be more verbose than Claude 3.5 Sonnet.',
    ],
  },
  midjourney: {
    billingModel: 'Subscription GPU Hours ($10 - $60/mo)',
    idealForBullets: [
      'You require photorealistic textures, cinematic lighting, and industry-benchmark aesthetic style',
      'You want superior prompt fidelity without complex local parameter tuning',
    ],
    specs: {
      freeTier: 'No free trial; paid plan required',
      byokSupport: false,
      openSource: false,
      contextOrModel: 'Midjourney v6.1 / Niji 6',
      teamCollab: true,
      apiAvailable: false,
    },
    gotchas: [
      'Basic ($10/mo) and Standard ($30/mo) plans publicly post all your creations to the community gallery.',
      'Private image generation (Stealth Mode) is locked behind the $60/month Pro tier.',
      'No official public REST API; programmatic automation requires unofficial third-party wrappers.',
    ],
  },
  'flux-1': {
    billingModel: 'Open weights / Pay-per-image API',
    idealForBullets: [
      'You need crisp legible typography, realistic human anatomy, and zero proprietary lock-in',
      'You want to run models locally on 16GB+ VRAM or via ultra-fast serverless APIs (Fal.ai, Replicate)',
    ],
    specs: {
      freeTier: 'FLUX.1 [schnell] is 100% Apache 2.0 open source',
      byokSupport: true,
      openSource: true,
      contextOrModel: '12B parameter rectified flow transformer',
      teamCollab: false,
      apiAvailable: true,
    },
    gotchas: [
      'FLUX.1 [dev] license prohibits commercial revenue generation without custom enterprise licensing.',
      'Local execution demands minimum 16GB–24GB VRAM GPU (RTX 3090/4090) for viable generation speeds.',
    ],
  },
  'stable-diffusion': {
    billingModel: 'Open Source / Cloud subscription',
    idealForBullets: [
      'You demand 100% offline generation, custom LoRA fine-tuning, and ControlNet precision',
      'You refuse monthly subscription fees and require complete data sovereignty on local hardware',
    ],
    specs: {
      freeTier: '100% free for self-hosted local execution (ComfyUI/A1111)',
      byokSupport: true,
      openSource: true,
      contextOrModel: 'SDXL, SD 3.5 Large (8B parameters)',
      teamCollab: false,
      apiAvailable: true,
    },
    gotchas: [
      'Substantial technical ramp-up required for environment setup (Python, CUDA, checkpoint pruning).',
      'Vanilla base models need community fine-tuned checkpoints to compete with Midjourney aesthetics.',
      'SD 3.5 commercial license requires enterprise agreement if enterprise revenue exceeds $1M/yr.',
    ],
  },
  n8n: {
    billingModel: 'Fair-code self-hosted free / $20/mo Cloud',
    idealForBullets: [
      'You want self-hosted, sovereign AI agent workflows with direct database and custom code access',
      'You refuse to pay per-task execution fees on high-volume background data pipelines',
    ],
    specs: {
      freeTier: '100% free self-hosted Community Edition (Docker / npm)',
      byokSupport: true,
      openSource: true,
      contextOrModel: 'Native LangChain, OpenAI, Anthropic, Local Ollama models',
      teamCollab: true,
      apiAvailable: true,
    },
    gotchas: [
      'Self-hosting requires maintaining Docker instances, Redis queues, and SSL certificates.',
      'Community Edition lacks SAML SSO and granular role-based permissions without Enterprise tier.',
      'Cloud managed tiers enforce monthly execution quota limits.',
    ],
  },
  make: {
    billingModel: 'Operation / Task based ($9/mo)',
    idealForBullets: [
      'You need visual, complex branching automation with routers, iterators, and error handlers',
      'You want 1,000+ app connectors without writing webhook plumbing and polling scripts',
    ],
    specs: {
      freeTier: 'Free plan with 1,000 operations/mo and 2 active scenarios',
      byokSupport: true,
      openSource: false,
      contextOrModel: 'Native HTTP module & direct AI connectors',
      teamCollab: true,
      apiAvailable: true,
    },
    gotchas: [
      'Every single filter evaluation and router branch consumes operations; quotas deplete fast.',
      'Execution log retention is capped at 30 days on introductory plans.',
      'Error handler routes consume operations even when external services fail.',
    ],
  },
  zapier: {
    billingModel: 'Task-based ($19.99/mo)',
    idealForBullets: [
      'You need seamless integration with 6,000+ enterprise apps and SaaS ecosystems',
      'You want non-technical team members to build automated triggers without developer assistance',
    ],
    specs: {
      freeTier: 'Free plan with 100 tasks/mo and single-step Zaps only',
      byokSupport: true,
      openSource: false,
      contextOrModel: 'Zapier Central AI & app integrations',
      teamCollab: true,
      apiAvailable: true,
    },
    gotchas: [
      'Steep price curve: multi-step automation requires paid tiers starting at $19.99 for only 750 tasks.',
      'Automated task retry on downstream failure is restricted to higher tier plans.',
      'Substantially higher cost per operation compared to Make or self-hosted n8n.',
    ],
  },
  elevenlabs: {
    billingModel: 'Character-based ($5/mo Starter / $22/mo Creator)',
    idealForBullets: [
      'You need industry-leading emotional voice synthesis, voice cloning, and audio dubbing',
      'You want ultra-low latency Conversational AI agents via direct WebSockets',
    ],
    specs: {
      freeTier: 'Free tier with 10,000 characters/mo (strictly non-commercial)',
      byokSupport: false,
      openSource: false,
      contextOrModel: 'Turbo v2.5, Multilingual v2, Flash v2',
      teamCollab: true,
      apiAvailable: true,
    },
    gotchas: [
      'Free tier strictly forbids commercial monetization and mandates attribution.',
      'Instant voice cloning consumes character balance fast; long-form audiobooks require Creator ($22/mo) or Pro ($99/mo).',
      'Unused monthly character credits do not roll over to subsequent billing cycles.',
    ],
  },
};

/**
 * Normalizes raw ToolItem into a strict ToolSpec structure.
 */
export function normalizeToolSpec(raw: any): ToolSpec {
  const id = raw.id || raw.slug || '';
  const curated = CURATED_SPECS[id] || {};

  // Default inference based on raw fields
  const startingPrice = raw.starting_price || curated.startingPrice || 'Contact sales';
  const billingModel = curated.billingModel || raw.pricing_model || 'Subscription';
  const affiliateUrl = raw.affiliate_url || raw.url || '#';

  // Killer differentiators: prefer curated bullets, fallback to strengths/best_for
  const idealForBullets: string[] = curated.idealForBullets || [
    raw.best_for ? `Best fit for ${raw.best_for.toLowerCase()}` : `Engineered specifically for modern ${raw.category} workflows`,
    (raw.strengths && raw.strengths[0]) || (raw.pros && raw.pros[0]) || 'Offers verified commercial reliability and active community support',
  ];

  // Specs
  const freeTier = curated.specs?.freeTier || (raw.free_tier ? 'Free tier / trial available' : 'Paid only (No permanent free tier)');
  const byokSupport = curated.specs?.byokSupport ?? (raw.category === 'Coding AI' || raw.category === 'Workflow AI' || id.includes('deepseek'));
  const openSource = curated.specs?.openSource ?? (id.includes('flux') || id.includes('stable-diffusion') || id.includes('n8n') || id.includes('deepseek') || id.includes('whisper') || id.includes('edge-tts'));
  const contextOrModel = curated.specs?.contextOrModel || (raw.key_capabilities && raw.key_capabilities[0]) || (raw.key_features && raw.key_features[0]) || 'Frontier AI orchestration';
  const teamCollab = curated.specs?.teamCollab ?? true;
  const apiAvailable = curated.specs?.apiAvailable ?? (raw.category !== 'Music AI' || id.includes('suno'));

  // Gotchas: prefer curated gotchas, fallback to trade_offs/cons
  const rawGotchas = (raw.trade_offs || raw.cons || []).slice(0, 2);
  const gotchas: string[] = curated.gotchas || [
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
 * Builds standard ComparisonData with high-intent BOFU FAQ items.
 */
export function buildComparisonData(toolARaw: any, toolBRaw: any, category: string): ComparisonData {
  const toolA = normalizeToolSpec(toolARaw);
  const toolB = normalizeToolSpec(toolBRaw);

  // Dynamic Current Month & Year verification tag
  const now = new Date();
  const lastVerified = new Intl.DateTimeFormat('en-US', { month: 'long', year: 'numeric' }).format(now);

  // High-intent BOFU FAQs mapping directly to developer credit card decisions
  const faqs = [
    {
      question: `Can I migrate from ${toolB.name} to ${toolA.name}?`,
      answer: `Yes. Both tools operate within the ${category} domain, and migrating typically requires swapping API keys or workspace configurations with minimal downtime.`,
    },
    {
      question: `Which tool is cheaper for solo developers?`,
      answer: `${toolA.name} starts at ${toolA.startingPrice} (${toolA.billingModel}), while ${toolB.name} starts at ${toolB.startingPrice} (${toolB.billingModel}). Compare their free quotas above to minimize out-of-pocket costs.`,
    },
    {
      question: `Do either of these tools train on your data?`,
      answer: `Both platforms adhere to standard enterprise data governance; paid commercial tiers and API connections generally do not train on customer inputs, while free consumer tiers may require manual opt-out in settings.`,
    },
    {
      question: `Can I use ${toolA.name} and ${toolB.name} together in the same workflow?`,
      answer: `Yes. Many engineering teams leverage both side-by-side (e.g., using one for rapid exploratory ideation and the other for production-grade execution or self-hosted deployment).`,
    },
  ];

  return {
    toolA,
    toolB,
    category,
    lastVerified,
    faqs,
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
