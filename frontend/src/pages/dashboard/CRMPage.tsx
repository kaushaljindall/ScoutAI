import { useState } from 'react';
import { useGetSavedLeads } from '@/hooks/useScout';
import { useUpdateLeadStatus } from '@/hooks/useCRM';
import { Link } from 'react-router-dom';
import { cn } from '@/utils/cn';
import { Building, MapPin } from 'lucide-react';

const COLUMNS = [
  'New Lead', 'Contacted', 'Replied', 'Interested', 
  'Meeting Scheduled', 'Proposal Sent', 'Negotiation', 'Won', 'Lost'
];

export default function CRMPage() {
  const { data: leads, isLoading } = useGetSavedLeads();
  const { mutate: updateStatus } = useUpdateLeadStatus();
  
  const [draggedLead, setDraggedLead] = useState<string | null>(null);

  if (isLoading) {
    return <div className="h-full flex items-center justify-center">Loading Pipeline...</div>;
  }

  const handleDragStart = (e: React.DragEvent, leadId: string) => {
    setDraggedLead(leadId);
    e.dataTransfer.setData('text/plain', leadId);
    e.dataTransfer.effectAllowed = 'move';
  };

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
    e.dataTransfer.dropEffect = 'move';
  };

  const handleDrop = (e: React.DragEvent, status: string) => {
    e.preventDefault();
    const leadId = e.dataTransfer.getData('text/plain');
    if (leadId) {
      updateStatus({ leadId, status });
    }
    setDraggedLead(null);
  };

  const leadsByStatus = COLUMNS.reduce((acc, status) => {
    acc[status] = leads?.filter((l: any) => l.status === status) || [];
    return acc;
  }, {} as Record<string, any[]>);

  return (
    <div className="h-full flex flex-col pt-2 pb-6 relative overflow-hidden">
      <div className="mb-6 flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">CRM Pipeline</h1>
          <p className="text-primary/60 mt-1">Manage and track your deals.</p>
        </div>
      </div>

      <div className="flex-1 overflow-x-auto flex gap-4 pb-4 snap-x">
        {COLUMNS.map(column => (
          <div 
            key={column} 
            className="flex-none w-[320px] flex flex-col bg-surface/20 rounded-xl border border-border/50 snap-center"
            onDragOver={handleDragOver}
            onDrop={(e) => handleDrop(e, column)}
          >
            <div className="p-4 border-b border-border/50 flex justify-between items-center bg-surface/30 rounded-t-xl">
              <h3 className="font-semibold text-sm uppercase tracking-wider">{column}</h3>
              <span className="text-xs bg-surface px-2 py-0.5 rounded-full text-primary/60">
                {leadsByStatus[column].length}
              </span>
            </div>
            
            <div className="flex-1 p-3 overflow-y-auto space-y-3">
              {leadsByStatus[column].map((lead: any) => (
                <div
                  key={lead.id}
                  draggable
                  onDragStart={(e) => handleDragStart(e, lead.id)}
                  className={cn(
                    "p-4 bg-background border border-border/50 rounded-xl cursor-grab active:cursor-grabbing hover:border-primary/50 transition-colors group relative",
                    draggedLead === lead.id ? "opacity-50" : "opacity-100"
                  )}
                >
                  <Link to={`/dashboard/crm/${lead.id}`} className="absolute inset-0 z-10" />
                  
                  <div className="flex justify-between items-start mb-2 relative z-20 pointer-events-none">
                    <h4 className="font-semibold truncate pr-2 flex-1">{lead.business.business_name}</h4>
                  </div>
                  
                  <div className="text-xs text-primary/60 space-y-1 relative z-20 pointer-events-none">
                    <div className="flex items-center gap-1.5"><Building size={12} /> {lead.business.category || 'Unknown'}</div>
                    <div className="flex items-center gap-1.5"><MapPin size={12} /> {lead.business.city || 'Unknown'}</div>
                  </div>
                </div>
              ))}
              {leadsByStatus[column].length === 0 && (
                <div className="h-full min-h-[100px] flex items-center justify-center text-primary/30 text-sm border-2 border-dashed border-border/50 rounded-xl">
                  Drop here
                </div>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
