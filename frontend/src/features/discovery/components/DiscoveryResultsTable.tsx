import React from 'react';
import type { DiscoveredBusiness } from '@/services/discoveryService';

const PROVIDER_BADGE_COLORS: Record<string, string> = {
  searxng: 'bg-blue-500/20 text-blue-400 border-blue-500/30',
  brave: 'bg-orange-500/20 text-orange-400 border-orange-500/30',
  duckduckgo: 'bg-red-500/20 text-red-400 border-red-500/30',
  google_places: 'bg-green-500/20 text-green-400 border-green-500/30',
  website_discovery: 'bg-purple-500/20 text-purple-400 border-purple-500/30',
};

interface DiscoveryResultsTableProps {
  businesses: DiscoveredBusiness[];
  isLoading?: boolean;
}

export const DiscoveryResultsTable: React.FC<DiscoveryResultsTableProps> = ({ businesses, isLoading }) => {
  if (isLoading) {
    return (
      <div className="space-y-2">
        {Array.from({ length: 6 }).map((_, i) => (
          <div key={i} className="h-14 rounded-xl bg-white/5 animate-pulse" />
        ))}
      </div>
    );
  }

  if (businesses.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center py-20 text-white/30">
        <span className="text-4xl mb-3">🔍</span>
        <p className="text-sm">No results yet. Run a search above.</p>
      </div>
    );
  }

  return (
    <div className="space-y-2">
      {businesses.map((biz, idx) => (
        <div
          key={biz.id}
          className="flex items-center gap-4 rounded-xl border border-white/8 bg-white/4 hover:bg-white/8 px-4 py-3 transition-all duration-200 group"
          style={{ animationDelay: `${idx * 30}ms` }}
        >
          {/* Confidence indicator */}
          <div className="w-1 h-10 rounded-full flex-shrink-0" style={{
            background: `hsl(${biz.provider_confidence * 120}, 70%, 55%)`,
          }} />

          {/* Name + address */}
          <div className="flex-1 min-w-0">
            <p className="text-sm font-semibold text-white truncate">{biz.business_name}</p>
            <p className="text-xs text-white/40 truncate">
              {[biz.address, biz.city, biz.country].filter(Boolean).join(' · ') || 'No address'}
            </p>
          </div>

          {/* Category */}
          {biz.category && (
            <span className="hidden md:inline text-xs text-white/50 bg-white/5 px-2 py-0.5 rounded-full border border-white/10 truncate max-w-[120px]">
              {biz.category}
            </span>
          )}

          {/* Rating */}
          {biz.google_rating != null && (
            <div className="hidden sm:flex items-center gap-1 text-xs text-yellow-400">
              <span>★</span>
              <span>{biz.google_rating.toFixed(1)}</span>
            </div>
          )}

          {/* Website */}
          {biz.website && (
            <a
              href={biz.website}
              target="_blank"
              rel="noopener noreferrer"
              className="text-xs text-blue-400/70 hover:text-blue-400 transition-colors hidden lg:block truncate max-w-[150px]"
              onClick={(e) => e.stopPropagation()}
            >
              {new URL(biz.website).hostname}
            </a>
          )}

          {/* Source badge */}
          <span className={`text-[10px] font-medium px-2 py-0.5 rounded-full border flex-shrink-0 ${
            PROVIDER_BADGE_COLORS[biz.provider] || 'bg-white/10 text-white/50 border-white/20'
          }`}>
            {biz.provider.replace('_', ' ')}
          </span>
        </div>
      ))}
    </div>
  );
};
