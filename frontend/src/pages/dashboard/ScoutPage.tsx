import { useSearchBusinesses } from '@/hooks/useScout';
import { useScoutStore } from '@/store/scoutStore';
import { ScoutFilters } from '@/components/scout/ScoutFilters';
import { ScoutTable } from '@/components/scout/ScoutTable';
import { LeadDrawer } from '@/components/scout/LeadDrawer';

export default function ScoutPage() {
  const { filters } = useScoutStore();
  const { data, isLoading, isError } = useSearchBusinesses(filters);

  return (
    <div className="h-full flex flex-col pt-2 pb-6">
      <div className="mb-6">
        <h1 className="text-3xl font-bold tracking-tight">Scout</h1>
        <p className="text-primary/60 mt-1">Discover, analyze and organize your potential clients.</p>
      </div>

      <ScoutFilters />

      <div className="flex-1 min-h-0 relative">
        {isError ? (
          <div className="flex flex-col items-center justify-center h-[400px] text-center text-red-500 bg-red-500/5 rounded-xl border border-red-500/20">
            <p className="font-medium">Failed to load businesses</p>
            <p className="text-sm opacity-80 mt-1">Please try again later.</p>
          </div>
        ) : (
          <ScoutTable data={data?.items || []} isLoading={isLoading} />
        )}
      </div>

      {/* Pagination Controls */}
      {data && data.pages > 1 && (
        <div className="flex items-center justify-between mt-4 text-sm">
          <span className="text-primary/60">
            Showing <span className="font-medium text-primary">{(data.page - 1) * data.size + 1}</span> to <span className="font-medium text-primary">{Math.min(data.page * data.size, data.total)}</span> of <span className="font-medium text-primary">{data.total}</span> results
          </span>
          <div className="flex items-center gap-2">
            <button 
              disabled={data.page === 1}
              className="px-3 py-1.5 rounded-lg border border-border/50 bg-surface disabled:opacity-50 hover:bg-surface-hover transition-colors"
            >
              Previous
            </button>
            <button 
              disabled={data.page === data.pages}
              className="px-3 py-1.5 rounded-lg border border-border/50 bg-surface disabled:opacity-50 hover:bg-surface-hover transition-colors"
            >
              Next
            </button>
          </div>
        </div>
      )}

      <LeadDrawer />
    </div>
  );
}
