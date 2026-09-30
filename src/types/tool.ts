/**
 * src/types/tool.ts
 * ============================================================================
 * Canonical Tool Schema for StackDiff
 * Grounded data structure with explicit sources, verification timestamps,
 * tiered pricing, and factual technical specifications.
 * ============================================================================
 */

export interface ToolPricing {
  starting_price: string;     // e.g. "$20/mo"
  billing_model: string;      // "Seat-based" | "Usage-based" | "Freemium" | "Subscription"
  free_tier_details: string;  // Detailed description of the free tier / trial quota
  tiers_summary?: string;     // e.g. "Pro $20 / Pro+ $60 / Ultra $200"
}

export interface ToolTechnicalSpecs {
  current_models: string[];   // Strictly verified current model list (prunes obsolete models)
  context_window?: string;    // e.g. "128K", "200K", "1M"
  byok_support: boolean;      // Bring Your Own Key support
  open_source: boolean;       // Open source weights / codebase
  telemetry_privacy: boolean; // Does the vendor refrain from training models on user data?
  offline_support: boolean;   // Can be run offline locally
}

export interface ToolData {
  slug: string;
  name: string;
  category: "Coding AI" | "LLM" | "Image AI" | "Video AI" | "Voice AI" | "Workflow AI" | string;
  official_website: string;
  official_pricing_url: string;
  source_url: string;           // Direct official documentation or pricing page source
  last_checked_at: string;      // YYYY-MM-DD
  pricing: ToolPricing;
  technical_specs: ToolTechnicalSpecs;
  gotchas: string[];            // Documented pricing limits, quotas, or gotchas

  // Backwards-compatibility & supplementary metadata
  id?: string;
  tagline?: string;
  core_positioning?: string;
  pricing_model?: string;
  starting_price?: string;
  free_tier?: boolean;
  best_for?: string;
  primary_audience?: string;
  key_features?: string[];
  key_capabilities?: string[];
  pros?: string[];
  strengths?: string[];
  cons?: string[];
  trade_offs?: string[];
  supported_platforms?: string[];
  platforms?: string[];
  affiliate_url?: string;
  url?: string;
  verdict_context?: string;
}
