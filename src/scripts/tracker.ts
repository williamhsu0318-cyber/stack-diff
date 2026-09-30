/**
 * src/scripts/tracker.ts
 * ============================================================================
 * StackDiff Client-Side Outbound & Affiliate Click Tracker
 * Captures user intent and outbound CTR for comparison cards and diff matrices.
 * Stores telemetry in localStorage and dispatches beacons for analytics.
 * ============================================================================
 */

export interface ClickRecord {
  toolSlug: string;
  pair?: string;
  linkType: 'affiliate' | 'official_pricing' | 'outbound';
  href: string;
  pathname: string;
  referrer: string;
  timestamp: string;
}

export function initStackDiffTracker() {
  if (typeof window === 'undefined' || typeof document === 'undefined') return;

  // Global helper for user/developer inspecting clicks in browser console
  (window as any).getStackDiffClicks = (): ClickRecord[] => {
    try {
      return JSON.parse(localStorage.getItem('stackdiff_clicks') || '[]');
    } catch {
      return [];
    }
  };

  (window as any).clearStackDiffClicks = (): void => {
    localStorage.removeItem('stackdiff_clicks');
    console.info('[StackDiff Tracker] Click history cleared.');
  };

  document.addEventListener('click', (event: MouseEvent) => {
    const target = event.target as HTMLElement | null;
    if (!target) return;

    // Find the closest anchor tag with tracking data
    const anchor = target.closest('a') as HTMLAnchorElement | null;
    if (!anchor) return;

    const toolSlug = anchor.getAttribute('data-tool-slug');
    const pair = anchor.getAttribute('data-pair') || undefined;
    const isPricingLink = anchor.textContent?.includes('Official Pricing') || anchor.getAttribute('rel')?.includes('nofollow');
    const isAffiliate = anchor.getAttribute('rel')?.includes('sponsored');

    // Only track outbound tool or pricing clicks
    if (!toolSlug && !isPricingLink && !isAffiliate) return;

    const linkType: ClickRecord['linkType'] = isAffiliate
      ? 'affiliate'
      : isPricingLink
      ? 'official_pricing'
      : 'outbound';

    const record: ClickRecord = {
      toolSlug: toolSlug || 'unknown',
      pair,
      linkType,
      href: anchor.href,
      pathname: window.location.pathname,
      referrer: document.referrer || '',
      timestamp: new Date().toISOString(),
    };

    // 1. Record to localStorage
    try {
      const history: ClickRecord[] = JSON.parse(localStorage.getItem('stackdiff_clicks') || '[]');
      history.push(record);
      // Keep most recent 200 events
      if (history.length > 200) history.shift();
      localStorage.setItem('stackdiff_clicks', JSON.stringify(history));
    } catch (err) {
      console.warn('[StackDiff Tracker] Failed to save to localStorage:', err);
    }

    // 2. Dispatch custom event for external analytics (Google Analytics, Plausible, etc.)
    try {
      const customEvent = new CustomEvent('stackdiff:outbound_click', { detail: record });
      window.dispatchEvent(customEvent);

      if (typeof (window as any).gtag === 'function') {
        (window as any).gtag('event', 'outbound_click', {
          event_category: linkType,
          event_label: toolSlug,
          pair_comparison: pair,
          destination_url: anchor.href,
        });
      }
    } catch {
      // Ignore analytics dispatch errors
    }

    // Console logging for verification
    if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
      console.log(`[StackDiff Tracker] ${linkType.toUpperCase()} Click:`, record);
    }
  });
}
