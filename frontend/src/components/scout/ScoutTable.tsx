import { 
  useReactTable, 
  getCoreRowModel, 
  flexRender, 
  createColumnHelper,
} from '@tanstack/react-table';
import type { Business } from '@/services/scoutService';
import { useScoutStore } from '@/store/scoutStore';
import { Button } from '@/components/ui/Button';
import { Globe, Phone, Mail, Camera, Briefcase, Star, Download, BookmarkPlus, Trash2 } from 'lucide-react';

interface ScoutTableProps {
  data: Business[];
  isLoading: boolean;
}

const columnHelper = createColumnHelper<Business>();

export const ScoutTable = ({ data, isLoading }: ScoutTableProps) => {
  const { selectedRows, setSelectedRows, setSelectedLeadId } = useScoutStore();

  const columns = [
    columnHelper.display({
      id: 'select',
      header: ({ table }) => (
        <input
          type="checkbox"
          className="rounded border-border bg-surface/50 text-accent focus:ring-accent"
          checked={table.getIsAllRowsSelected()}
          onChange={table.getToggleAllRowsSelectedHandler()}
        />
      ),
      cell: ({ row }) => (
        <input
          type="checkbox"
          className="rounded border-border bg-surface/50 text-accent focus:ring-accent"
          checked={row.getIsSelected()}
          onChange={row.getToggleSelectedHandler()}
          onClick={(e) => e.stopPropagation()}
        />
      ),
      size: 40,
    }),
    columnHelper.accessor('business_name', {
      header: 'Business Name',
      cell: info => (
        <div className="flex flex-col">
          <span className="font-medium">{info.getValue()}</span>
          <span className="text-[10px] text-primary/40 uppercase">{info.row.original.category}</span>
        </div>
      ),
      size: 250,
    }),
    columnHelper.accessor('city', {
      header: 'Location',
      cell: info => <span className="text-sm text-primary/60">{info.getValue() || '-'}</span>,
      size: 150,
    }),
    columnHelper.display({
      id: 'contact',
      header: 'Contact',
      cell: ({ row }) => (
        <div className="flex items-center gap-2 text-primary/40">
          {row.original.phone ? <Phone size={14} className="text-primary/70" /> : <Phone size={14} className="opacity-20" />}
          {row.original.email ? <Mail size={14} className="text-primary/70" /> : <Mail size={14} className="opacity-20" />}
          {row.original.website ? <Globe size={14} className="text-primary/70" /> : <Globe size={14} className="opacity-20" />}
        </div>
      ),
      size: 100,
    }),
    columnHelper.display({
      id: 'social',
      header: 'Social',
      cell: ({ row }) => (
        <div className="flex items-center gap-2 text-primary/40">
          {row.original.instagram ? <Camera size={14} className="text-pink-500/70" /> : <Camera size={14} className="opacity-20" />}
          {row.original.linkedin ? <Briefcase size={14} className="text-blue-500/70" /> : <Briefcase size={14} className="opacity-20" />}
        </div>
      ),
      size: 100,
    }),
    columnHelper.accessor('google_rating', {
      header: 'Rating',
      cell: info => (
        <div className="flex items-center gap-1.5">
          <Star size={12} className="text-yellow-500 fill-yellow-500" />
          <span className="text-sm font-medium">{info.getValue() || '-'}</span>
          <span className="text-xs text-primary/40">({info.row.original.review_count})</span>
        </div>
      ),
      size: 120,
    }),
  ];

  const table = useReactTable({
    data,
    columns,
    state: {
      rowSelection: selectedRows,
    },
    onRowSelectionChange: setSelectedRows,
    getCoreRowModel: getCoreRowModel(),
    getRowId: row => row.id,
  });

  const selectedCount = Object.keys(selectedRows).length;

  return (
    <div className="flex flex-col h-full overflow-hidden border border-border/50 rounded-xl bg-background/50">
      {/* Bulk Actions Bar */}
      {selectedCount > 0 && (
        <div className="bg-accent/10 border-b border-accent/20 px-4 py-2 flex items-center justify-between animate-in fade-in slide-in-from-top-2">
          <span className="text-sm font-medium text-accent">{selectedCount} businesses selected</span>
          <div className="flex items-center gap-2">
            <Button variant="outline" size="sm" className="h-7 text-xs gap-1 border-accent/30 text-accent hover:bg-accent/20">
              <BookmarkPlus size={12} /> Save Leads
            </Button>
            <Button variant="outline" size="sm" className="h-7 text-xs gap-1">
              <Download size={12} /> Export CSV
            </Button>
            <Button variant="outline" size="sm" className="h-7 text-xs gap-1 text-red-500 hover:text-red-600 hover:bg-red-500/10">
              <Trash2 size={12} /> Delete
            </Button>
          </div>
        </div>
      )}

      {/* Table Area */}
      <div className="flex-1 overflow-auto">
        <table className="w-full text-left border-collapse min-w-[800px]">
          <thead className="sticky top-0 bg-surface/80 backdrop-blur-md z-10">
            {table.getHeaderGroups().map(headerGroup => (
              <tr key={headerGroup.id}>
                {headerGroup.headers.map(header => (
                  <th key={header.id} className="h-10 px-4 align-middle text-xs font-medium text-primary/50 border-b border-border/50 uppercase tracking-wider">
                    {flexRender(
                      header.column.columnDef.header,
                      header.getContext()
                    )}
                  </th>
                ))}
              </tr>
            ))}
          </thead>
          <tbody>
            {isLoading ? (
              // Skeleton Loading
              Array.from({ length: 10 }).map((_, i) => (
                <tr key={i} className="border-b border-border/20">
                  {columns.map((_, j) => (
                    <td key={j} className="p-4">
                      <div className="h-4 bg-surface rounded animate-pulse w-full max-w-[80%]" />
                    </td>
                  ))}
                </tr>
              ))
            ) : data.length === 0 ? (
              // Empty State
              <tr>
                <td colSpan={columns.length} className="h-[400px] text-center">
                  <div className="flex flex-col items-center justify-center text-primary/40">
                    <div className="w-12 h-12 rounded-full bg-surface mb-3 flex items-center justify-center">
                      <Globe size={24} className="opacity-50" />
                    </div>
                    <p className="text-sm font-medium">No businesses found.</p>
                    <p className="text-xs mt-1">Try adjusting your filters or search query.</p>
                  </div>
                </td>
              </tr>
            ) : (
              // Data Rows
              table.getRowModel().rows.map(row => (
                <tr 
                  key={row.id} 
                  className="border-b border-border/20 hover:bg-surface/30 transition-colors cursor-pointer"
                  onClick={() => {
                    setSelectedLeadId(row.id);
                    useScoutStore.getState().setIsDrawerOpen(true);
                  }}
                >
                  {row.getVisibleCells().map(cell => (
                    <td key={cell.id} className="p-4 align-middle text-sm">
                      {flexRender(cell.column.columnDef.cell, cell.getContext())}
                    </td>
                  ))}
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
};
