import { useScoutStore } from '@/store/scoutStore';
import { useDiscoverBusinesses } from '@/hooks/useScout';
import { Search, Filter, X, Sparkles } from 'lucide-react';
import { Button } from '@/components/ui/Button';

import { useQueryClient } from '@tanstack/react-query';
import { scoutService } from '@/services/scoutService';

const smartFiltersOptions = [
  { id: 'high_opportunity', label: '⭐ High Opportunity' },
  { id: 'instagram_active', label: '📱 Instagram Active' },
  { id: 'website_missing', label: '🌐 Website Missing' },
  { id: 'email_available', label: '📧 Email Available' },
  { id: 'phone_available', label: '☎ Phone Available' },
  { id: 'verified', label: '🏢 Verified Business' },
  { id: 'ai_recommended', label: '🤖 AI Recommended' },
  { id: 'recently_added', label: '🔥 Recently Added' },
];

const industries = ['Healthcare', 'Restaurants', 'Real Estate', 'Education', 'Manufacturing', 'Agencies', 'Startups', 'Custom'];

export const ScoutFilters = () => {
  const { filters, setFilters, resetFilters, setIsDiscovering, setDiscoveryStatus } = useScoutStore();
  const discoverMutation = useDiscoverBusinesses();
  
  const queryClient = useQueryClient();

  const handleDiscover = async () => {
    if (!filters.q) return;
    setIsDiscovering(true);
    setDiscoveryStatus('Starting Agent...');

    try {
      const stream = scoutService.discoverStream(filters.q);
      for await (const event of stream) {
        if (event.status === 'progress') {
          setDiscoveryStatus(event.message);
        } else if (event.status === 'completed') {
          setDiscoveryStatus('Completed!');
          break;
        } else if (event.status === 'error') {
          setDiscoveryStatus(`Error: ${event.message}`);
          break;
        }
      }
      
      // Invalidate to refresh the table
      setTimeout(() => {
        queryClient.invalidateQueries({ queryKey: ['scout'] });
        setIsDiscovering(false);
        setDiscoveryStatus('');
      }, 1000);
      
    } catch (err) {
      console.error(err);
      setIsDiscovering(false);
      setDiscoveryStatus('');
    }
  };

  const toggleSmartFilter = (id: string) => {
    const current = filters.smartFilters;
    const updated = current.includes(id) 
      ? current.filter(f => f !== id)
      : [...current, id];
    setFilters({ smartFilters: updated });
  };

  return (
    <div className="flex flex-col gap-4 mb-6">
      {/* Search Bar & Primary Actions */}
      <div className="flex items-center gap-3">
        <div className="relative flex-1">
          <Search size={16} className="absolute left-3 top-1/2 -translate-y-1/2 text-primary/40" />
          <input
            type="text"
            placeholder="Discover businesses (e.g. Dentists in Chandler)..."
            className="w-full h-10 bg-surface/50 border border-border/50 rounded-lg pl-9 pr-4 text-sm focus:outline-none focus:border-accent/50 focus:ring-1 focus:ring-accent/50 transition-all"
            value={filters.q}
            onChange={(e) => setFilters({ q: e.target.value })}
            onKeyDown={(e) => {
              if (e.key === 'Enter') handleDiscover();
            }}
          />
        </div>
        <Button onClick={handleDiscover} isLoading={discoverMutation.isPending} className="gap-2 bg-accent text-background hover:bg-accent-hover">
          <Sparkles size={14} /> Discover
        </Button>
        <Button variant="outline" className="gap-2">
          <Filter size={14} /> Filters
        </Button>
      </div>

      {/* Tabs / Categories */}
      <div className="flex items-center gap-1 overflow-x-auto pb-2 scrollbar-hide">
        <button
          className={`px-3 py-1.5 rounded-full text-sm font-medium whitespace-nowrap transition-colors ${
            !filters.category ? 'bg-primary text-background' : 'bg-surface/50 text-primary/60 hover:text-primary hover:bg-surface'
          }`}
          onClick={() => setFilters({ category: '' })}
        >
          All Businesses
        </button>
        {industries.map(ind => (
          <button
            key={ind}
            className={`px-3 py-1.5 rounded-full text-sm font-medium whitespace-nowrap transition-colors ${
              filters.category === ind ? 'bg-primary text-background' : 'bg-surface/50 text-primary/60 hover:text-primary hover:bg-surface'
            }`}
            onClick={() => setFilters({ category: ind })}
          >
            {ind}
          </button>
        ))}
      </div>

      {/* Smart Filters Chips */}
      <div className="flex flex-wrap items-center gap-2">
        {smartFiltersOptions.map(option => (
          <button
            key={option.id}
            onClick={() => toggleSmartFilter(option.id)}
            className={`px-3 py-1.5 rounded-lg text-xs font-medium border transition-colors flex items-center gap-1.5 ${
              filters.smartFilters.includes(option.id)
                ? 'bg-accent/10 border-accent/30 text-accent'
                : 'bg-surface/30 border-border/50 text-primary/60 hover:bg-surface hover:text-primary'
            }`}
          >
            {option.label}
          </button>
        ))}
        
        {(filters.q || filters.category || filters.smartFilters.length > 0) && (
          <button
            onClick={resetFilters}
            className="px-2 py-1.5 rounded-lg text-xs font-medium text-red-500 hover:bg-red-500/10 transition-colors flex items-center gap-1 ml-auto"
          >
            <X size={12} /> Clear all
          </button>
        )}
      </div>
    </div>
  );
};
