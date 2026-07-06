import React, { useState, useRef, useCallback } from 'react';
import { Search, Zap, Clock, X } from 'lucide-react';
import {
  discoveryService,
} from '@/services/discoveryService';
import type {
  DiscoveredBusiness,
  ProviderStatus,
} from '@/services/discoveryService';
import { SearchProviderPanel } from '@/features/discovery/components/SearchProviderPanel';
import { SearchProgressCard } from '@/features/discovery/components/SearchProgressCard';
import { DiscoveryResultsTable } from '@/features/discovery/components/DiscoveryResultsTable';

type SearchStage = 'idle' | 'planning' | 'running' | 'merging' | 'completed';

export default function ScoutPage() {
  const [query, setQuery] = useState('');
  const [location, setLocation] = useState('');

  const [stage, setStage] = useState<SearchStage>('idle');
  const [progressMessage, setProgressMessage] = useState('');
  const [providers, setProviders] = useState<ProviderStatus[]>([]);
  const [results, setResults] = useState<DiscoveredBusiness[]>([]);
  const [duration, setDuration] = useState<number | undefined>();
  const [totalResults, setTotalResults] = useState(0);
  const [isCached, setIsCached] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const abortRef = useRef<(() => void) | null>(null);

  const isRunning = stage !== 'idle' && stage !== 'completed';

  const handleSearch = useCallback(() => {
    if (!query.trim() || isRunning) return;

    // Reset state
    setResults([]);
    setProviders([]);
    setDuration(undefined);
    setTotalResults(0);
    setIsCached(false);
    setError(null);
    setStage('planning');
    setProgressMessage('Planning search...');

    const abort = discoveryService.streamDiscover(query.trim(), location.trim() || undefined, {
      onProgress(message, stageStr, providerList) {
        setProgressMessage(message);
        setStage(stageStr as SearchStage);
        if (providerList && providerList.length > 0) {
          setProviders(providerList);
        }
      },
      onProvidersDone(providerStatuses) {
        setProviders(providerStatuses);
      },
      onResults(businesses) {
        setResults(businesses);
        setTotalResults(businesses.length);
      },
      onFinished(data) {
        setDuration(data.duration);
        setTotalResults(data.total);
        setIsCached(data.cached);
        setStage('completed');
        setProgressMessage(
          data.cached
            ? `Loaded ${data.total} results from cache`
            : `Discovered ${data.total} businesses in ${data.duration.toFixed(1)}s`
        );
        if (data.providers) {
          setProviders(data.providers);
        }
      },
      onError(msg) {
        setError(msg);
        setStage('completed');
      },
    });

    abortRef.current = abort;
  }, [query, location, isRunning]);

  const handleCancel = () => {
    abortRef.current?.();
    setStage('completed');
    setProgressMessage('Search cancelled');
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') handleSearch();
  };

  return (
    <div className="h-full flex flex-col pt-2 pb-8 space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold tracking-tight text-white">Scout</h1>
        <p className="text-white/50 mt-1 text-sm">
          Discover businesses from multiple sources using AI-powered parallel search.
        </p>
      </div>

      {/* Search Bar */}
      <div className="flex flex-col sm:flex-row gap-3">
        <div className="flex-1 relative">
          <Search className="absolute left-3.5 top-1/2 -translate-y-1/2 w-4 h-4 text-white/40" />
          <input
            id="discovery-query"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Find dentists in Chandigarh..."
            disabled={isRunning}
            className="w-full pl-10 pr-4 py-3 bg-white/8 border border-white/15 rounded-xl text-white placeholder-white/30 text-sm focus:outline-none focus:border-white/40 focus:bg-white/10 transition-all disabled:opacity-60"
          />
        </div>
        <div className="relative sm:w-48">
          <input
            id="discovery-location"
            value={location}
            onChange={(e) => setLocation(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Location (optional)"
            disabled={isRunning}
            className="w-full px-4 py-3 bg-white/8 border border-white/15 rounded-xl text-white placeholder-white/30 text-sm focus:outline-none focus:border-white/40 focus:bg-white/10 transition-all disabled:opacity-60"
          />
        </div>
        <div className="flex gap-2">
          <button
            id="discovery-search-btn"
            onClick={handleSearch}
            disabled={!query.trim() || isRunning}
            className="flex items-center gap-2 px-5 py-3 rounded-xl font-semibold text-sm bg-gradient-to-r from-blue-600 to-violet-600 hover:from-blue-500 hover:to-violet-500 text-white disabled:opacity-40 disabled:cursor-not-allowed transition-all"
          >
            <Zap className="w-4 h-4" />
            {isRunning ? 'Searching...' : 'Discover'}
          </button>
          {isRunning && (
            <button
              onClick={handleCancel}
              className="flex items-center gap-2 px-4 py-3 rounded-xl font-semibold text-sm bg-white/10 hover:bg-white/15 text-white/70 transition-all border border-white/15"
            >
              <X className="w-4 h-4" />
            </button>
          )}
        </div>
      </div>

      {/* Progress Section */}
      {stage !== 'idle' && (
        <div className="space-y-4">
          <SearchProgressCard
            stage={stage}
            message={progressMessage}
            totalResults={totalResults}
            duration={duration}
            isFinished={stage === 'completed'}
          />
          {providers.length > 0 && (
            <SearchProviderPanel providers={providers} isRunning={isRunning} />
          )}
        </div>
      )}

      {/* Error */}
      {error && (
        <div className="rounded-xl border border-red-500/30 bg-red-500/10 px-4 py-3 text-sm text-red-400">
          ⚠️ {error}
        </div>
      )}

      {/* Cached indicator */}
      {isCached && stage === 'completed' && (
        <div className="flex items-center gap-2 text-xs text-white/40">
          <Clock className="w-3.5 h-3.5" />
          <span>Results served from cache (15 min TTL)</span>
        </div>
      )}

      {/* Results */}
      {stage !== 'idle' && (
        <div className="flex-1 min-h-0">
          <div className="flex items-center justify-between mb-3">
            <h2 className="text-sm font-semibold text-white/70 uppercase tracking-wider">
              Results
            </h2>
            {results.length > 0 && (
              <span className="text-xs text-white/40">{results.length} businesses discovered</span>
            )}
          </div>
          <DiscoveryResultsTable
            businesses={results}
            isLoading={isRunning && results.length === 0}
          />
        </div>
      )}

      {/* Idle state */}
      {stage === 'idle' && (
        <div className="flex-1 flex flex-col items-center justify-center text-center text-white/25 py-20">
          <Zap className="w-12 h-12 mb-4 opacity-30" />
          <p className="text-base font-medium">Start a discovery search</p>
          <p className="text-sm mt-1">
            ScoutAI will query SearXNG, DuckDuckGo, Brave and more simultaneously
          </p>
        </div>
      )}
    </div>
  );
}
