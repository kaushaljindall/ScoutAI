import { useState } from 'react';
import { useGetDocuments } from '@/hooks/useDocuments';
import { Button } from '@/components/ui/Button';
import { Link } from 'react-router-dom';
import { FileText, FileSignature, FileKey, MoreVertical, Plus, Filter, LayoutTemplate } from 'lucide-react';
import { cn } from '@/utils/cn';

export default function DocumentsPage() {
  const { data: documents, isLoading } = useGetDocuments();
  const [activeTab, setActiveTab] = useState('All');

  const getIconForType = (type: string) => {
    switch (type) {
      case 'proposal': return <FileText size={18} className="text-blue-500" />;
      case 'contract': return <FileSignature size={18} className="text-emerald-500" />;
      case 'scope': return <LayoutTemplate size={18} className="text-purple-500" />;
      default: return <FileKey size={18} className="text-primary/60" />;
    }
  };

  const filteredDocs = documents?.filter(d => activeTab === 'All' || d.type === activeTab.toLowerCase()) || [];

  return (
    <div className="h-full flex flex-col pt-2 pb-6 relative overflow-hidden">
      <div className="mb-6 flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Documents</h1>
          <p className="text-primary/60 mt-1">Manage and generate professional client documents.</p>
        </div>
        <Button className="gap-2">
          <Plus size={16} /> New Document
        </Button>
      </div>

      <div className="flex gap-2 mb-6 border-b border-border/50 pb-4">
        {['All', 'Proposal', 'Contract', 'Scope', 'Quotation'].map(tab => (
          <button
            key={tab}
            onClick={() => setActiveTab(tab)}
            className={cn(
              "px-4 py-2 rounded-lg text-sm font-medium transition-colors border",
              activeTab === tab 
                ? "bg-accent/10 border-accent/20 text-accent" 
                : "bg-surface/30 border-border/50 text-primary/60 hover:text-primary hover:bg-surface/50"
            )}
          >
            {tab}
          </button>
        ))}
        <div className="flex-1" />
        <Button variant="outline" size="sm" className="gap-2 text-primary/60">
          <Filter size={14} /> Filter
        </Button>
      </div>

      <div className="flex-1 overflow-y-auto">
        {isLoading ? (
          <div className="flex items-center justify-center h-40">Loading documents...</div>
        ) : filteredDocs.length === 0 ? (
          <div className="flex flex-col items-center justify-center h-64 text-center border-2 border-dashed border-border/50 rounded-xl bg-surface/10">
            <FileText size={48} className="text-primary/20 mb-4" />
            <h3 className="text-lg font-medium">No documents found</h3>
            <p className="text-sm text-primary/60 mt-2 max-w-sm">
              Generate your first AI-powered proposal directly from any Lead in your CRM.
            </p>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
            {filteredDocs.map(doc => (
              <Link 
                to={`/dashboard/documents/${doc.id}`}
                key={doc.id} 
                className="group flex flex-col bg-background border border-border/50 rounded-xl p-5 hover:border-accent/50 hover:shadow-[0_4px_20px_-4px_rgba(var(--accent),0.1)] transition-all cursor-pointer h-48"
              >
                <div className="flex justify-between items-start mb-4">
                  <div className="p-2.5 bg-surface rounded-lg shrink-0">
                    {getIconForType(doc.type)}
                  </div>
                  <button className="text-primary/40 hover:text-primary p-1">
                    <MoreVertical size={16} />
                  </button>
                </div>
                
                <h3 className="font-semibold text-lg line-clamp-2 leading-tight group-hover:text-accent transition-colors flex-1">
                  {doc.title}
                </h3>
                
                <div className="flex justify-between items-center mt-4 pt-4 border-t border-border/50 text-xs text-primary/50">
                  <span className="uppercase tracking-wider">{doc.type}</span>
                  <span>{new Date(doc.updated_at).toLocaleDateString()}</span>
                </div>
              </Link>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
