import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useGetDocument, useUpdateDocument } from '@/hooks/useDocuments';
import { Button } from '@/components/ui/Button';
import { ArrowLeft, Download, FileText, Settings, Copy, Printer } from 'lucide-react';

export default function DocumentEditorPage() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const { data: document, isLoading } = useGetDocument(id || null);
  const { mutate: updateDocument, isPending: isSaving } = useUpdateDocument();
  
  const [content, setContent] = useState('');
  const [title, setTitle] = useState('');

  useEffect(() => {
    if (document) {
      setContent(document.content);
      setTitle(document.title);
    }
  }, [document]);

  // Auto-save logic
  useEffect(() => {
    if (!document || !id || isSaving) return;
    
    const handler = setTimeout(() => {
      if (content !== document.content || title !== document.title) {
        updateDocument({ id, params: { title, content } });
      }
    }, 2500);
    
    return () => clearTimeout(handler);
  }, [content, title, document, id, updateDocument, isSaving]);

  const handleCopy = () => {
    navigator.clipboard.writeText(content);
  };

  const handlePrint = () => {
    window.print();
  };

  if (isLoading) {
    return <div className="h-full flex items-center justify-center">Loading Document...</div>;
  }

  return (
    <div className="h-full flex flex-col pt-2 pb-6 print:p-0">
      {/* Top Bar - Hidden when printing */}
      <div className="mb-4 flex justify-between items-center print:hidden">
        <div className="flex items-center gap-4">
          <Button variant="outline" size="sm" onClick={() => navigate('/dashboard/documents')} className="gap-2">
            <ArrowLeft size={14} /> Back
          </Button>
          <div className="flex items-center gap-2 text-primary/60 text-sm">
            <FileText size={16} />
            <span className="uppercase tracking-wider font-medium">{document?.type}</span>
          </div>
        </div>
        
        <div className="flex items-center gap-3">
          <span className="text-xs text-primary/40 mr-2">
            {isSaving ? 'Saving...' : 'Saved to cloud'}
          </span>
          <Button variant="outline" size="sm" className="gap-2" onClick={handleCopy}>
            <Copy size={14} /> Copy
          </Button>
          <Button variant="outline" size="sm" className="gap-2" onClick={handlePrint}>
            <Printer size={14} /> Print PDF
          </Button>
          <Button size="sm" className="gap-2">
            <Download size={14} /> Export DOCX
          </Button>
        </div>
      </div>

      <div className="flex-1 min-h-0 flex gap-6 bg-surface/20 rounded-xl border border-border/50 p-2 print:border-none print:bg-white print:p-0">
        
        {/* Editor Wrapper */}
        <div className="flex-1 flex flex-col bg-background border border-border/50 rounded-lg overflow-hidden shadow-sm print:border-none print:shadow-none">
           {/* Document Title Header */}
           <div className="border-b border-border/50 px-8 py-4 bg-surface/30 print:hidden">
              <input
                type="text"
                value={title}
                onChange={(e) => setTitle(e.target.value)}
                className="w-full text-2xl font-bold bg-transparent outline-none placeholder:text-primary/30"
                placeholder="Document Title"
              />
           </div>
           
           {/* Raw Editor (Markdown text area simulating a rich editor for now) */}
           <div className="flex-1 overflow-y-auto p-8 print:p-0 print:overflow-visible">
              <textarea
                value={content}
                onChange={(e) => setContent(e.target.value)}
                className="w-full h-full min-h-[800px] resize-none bg-transparent outline-none text-base leading-relaxed print:text-black"
                placeholder="Start writing..."
                spellCheck="false"
              />
           </div>
        </div>

        {/* Right Settings Sidebar - Hidden when printing */}
        <div className="w-64 shrink-0 flex flex-col gap-4 overflow-y-auto pr-2 print:hidden">
          <div className="p-4 rounded-lg border border-border/50 bg-background h-full">
            <h3 className="font-semibold text-sm uppercase tracking-wider text-primary/60 mb-4 flex items-center gap-2">
              <Settings size={14} /> Document Settings
            </h3>
            
            <div className="space-y-4">
              <div>
                <label className="text-xs font-medium text-primary/60 mb-1.5 block">Status</label>
                <select className="w-full bg-surface border border-border/50 rounded-md p-2 text-sm outline-none focus:border-accent">
                  <option value="draft">Draft</option>
                  <option value="review">In Review</option>
                  <option value="sent">Sent to Client</option>
                  <option value="signed">Signed</option>
                </select>
              </div>
              
              <div className="pt-4 border-t border-border/50">
                <label className="text-xs font-medium text-primary/60 mb-1.5 block">Branding</label>
                <p className="text-xs text-primary/40 mb-3">Your default branding will be applied when exporting to PDF.</p>
                <Button variant="outline" size="sm" className="w-full text-xs">Edit Branding</Button>
              </div>
            </div>
          </div>
        </div>

      </div>
    </div>
  );
}
