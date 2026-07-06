import React from 'react';
import type { ProviderStatus } from '@/services/discoveryService';

const PROVIDER_COLORS: Record<string, string> = {
  searxng: 'bg-blue-500',
  brave: 'bg-orange-500',
  duckduckgo: 'bg-red-400',
  google_places: 'bg-green-500',
  website_discovery: 'bg-purple-500',
};

const PROVIDER_ICONS: Record<string, string> = {
  searxng: '🔍',
  brave: '🦁',
  duckduckgo: '🦆',
  google_places: '📍',
  website_discovery: '🌐',
};

interface SearchProviderPanelProps {
  providers: ProviderStatus[];
  isRunning: boolean;
}

export const SearchProviderPanel: React.FC<SearchProviderPanelProps> = ({ providers }) => {
  if (providers.length === 0) return null;

  return (
    <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-3">
      {providers.map((p) => {
        const accentColor = PROVIDER_COLORS[p.name] || 'bg-gray-500';
        const icon = PROVIDER_ICONS[p.name] || '🔎';
        const isActive = p.status === 'running';
        const isDone = p.status === 'completed';
        const isFailed = p.status === 'failed';

        return (
          <div
            key={p.name}
            className={`
              relative overflow-hidden rounded-xl border p-3 transition-all duration-300
              ${isActive ? 'border-white/30 bg-white/10 scale-[1.02]' : 'border-white/10 bg-white/5'}
              ${isFailed ? 'border-red-500/30 bg-red-500/5' : ''}
              ${isDone ? 'border-green-500/20' : ''}
            `}
          >
            {/* Accent color strip */}
            <div className={`absolute top-0 left-0 right-0 h-0.5 ${accentColor} opacity-60`} />
            {/* Animated pulse for running state */}
            {isActive && (
              <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/5 to-transparent animate-shimmer" />
            )}

            <div className="flex items-start justify-between mb-2">
              <span className="text-lg">{icon}</span>
              <div className={`w-2 h-2 rounded-full mt-1 ${
                isActive ? 'bg-blue-400 animate-pulse' :
                isDone ? 'bg-green-400' :
                isFailed ? 'bg-red-400' :
                'bg-white/20'
              }`} />
            </div>

            <p className="text-xs font-semibold text-white truncate">{p.display_name}</p>

            {isDone && (
              <p className="text-xs text-green-400 mt-1">{p.count} results</p>
            )}
            {isActive && (
              <p className="text-xs text-blue-400 mt-1 animate-pulse">Searching...</p>
            )}
            {isFailed && (
              <p className="text-xs text-red-400 mt-1 truncate" title={p.error || ''}>Failed</p>
            )}
            {p.status === 'pending' && (
              <p className="text-xs text-white/30 mt-1">Pending</p>
            )}

            {p.duration != null && isDone && (
              <p className="text-xs text-white/30 mt-0.5">{p.duration.toFixed(1)}s</p>
            )}
          </div>
        );
      })}
    </div>
  );
};
