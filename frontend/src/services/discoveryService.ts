// discoveryService.ts - Phase 5B Business Discovery

export interface DiscoveredBusiness {
  id: string;
  business_name: string;
  category?: string;
  website?: string;
  phone?: string;
  address?: string;
  city?: string;
  state?: string;
  country?: string;
  latitude?: number;
  longitude?: number;
  google_rating?: number;
  review_count?: number;
  provider: string;
  source_url?: string;
  provider_confidence: number;
  discovered_at: string;
}

export interface ProviderStatus {
  name: string;
  display_name: string;
  status: 'pending' | 'running' | 'completed' | 'failed';
  count?: number;
  duration?: number;
  error?: string;
}

export interface ProviderHealthStatus {
  name: string;
  display_name: string;
  priority: number;
  is_healthy: boolean;
  requires_key: boolean;
  key_configured: boolean;
}

export interface DiscoveryFinishedData {
  total: number;
  duration: number;
  cached: boolean;
  providers?: ProviderStatus[];
  errors?: Record<string, string>;
}

export type DiscoveryEventCallback = {
  onProgress?: (message: string, stage: string, providers?: ProviderStatus[]) => void;
  onProvidersDone?: (providers: ProviderStatus[]) => void;
  onResults?: (businesses: DiscoveredBusiness[]) => void;
  onFinished?: (data: DiscoveryFinishedData) => void;
  onError?: (message: string) => void;
};

const getToken = (): string => {
  try {
    const authStorage = localStorage.getItem('auth-storage');
    if (authStorage) {
      const parsed = JSON.parse(authStorage);
      return parsed.state?.accessToken || '';
    }
  } catch (e) {}
  return '';
};

const BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1';

export const discoveryService = {
  /**
   * Stream a discovery search — parses SSE events and fires callbacks.
   * Returns a cleanup function that can abort the stream.
   */
  streamDiscover(
    query: string,
    location: string | undefined,
    callbacks: DiscoveryEventCallback
  ): () => void {
    const controller = new AbortController();

    (async () => {
      try {
        const response = await fetch(`${BASE_URL}/search/discover`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            Authorization: `Bearer ${getToken()}`,
          },
          body: JSON.stringify({ query, location }),
          signal: controller.signal,
        });

        if (!response.ok || !response.body) {
          callbacks.onError?.(`HTTP ${response.status}`);
          return;
        }

        const reader = response.body.getReader();
        const decoder = new TextDecoder();
        let buffer = '';

        while (true) {
          const { value, done } = await reader.read();
          if (done) break;
          buffer += decoder.decode(value, { stream: true });

          const parts = buffer.split('\n\n');
          buffer = parts.pop() || '';

          for (const part of parts) {
            const line = part.trim();
            if (!line.startsWith('data: ')) continue;
            try {
              const payload = JSON.parse(line.substring(6));
              const { event, data } = payload;

              if (event === 'progress') {
                callbacks.onProgress?.(data.message, data.stage, data.providers);
              } else if (event === 'providers_done') {
                callbacks.onProvidersDone?.(data.providers);
              } else if (event === 'results') {
                callbacks.onResults?.(data);
              } else if (event === 'finished') {
                callbacks.onFinished?.(data);
              } else if (event === 'error') {
                callbacks.onError?.(data.message);
              }
            } catch (_) {}
          }
        }
      } catch (err: any) {
        if (err?.name !== 'AbortError') {
          callbacks.onError?.(err?.message || 'Stream failed');
        }
      }
    })();

    return () => controller.abort();
  },

  async getProviders(): Promise<ProviderHealthStatus[]> {
    const response = await fetch(`${BASE_URL}/search/providers`, {
      headers: { Authorization: `Bearer ${getToken()}` },
    });
    return response.json();
  },

  async getHistory(): Promise<{ history: Array<{ session_id: string; query: string; location?: string }> }> {
    const response = await fetch(`${BASE_URL}/search/history`, {
      headers: { Authorization: `Bearer ${getToken()}` },
    });
    return response.json();
  },
};
