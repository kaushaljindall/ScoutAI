import { useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useGetBusiness } from '@/hooks/useScout';
import { useGetConversations, useGetTasks, useGetTimeline } from '@/hooks/useCRM';
import { useGenerateDocument } from '@/hooks/useDocuments';
import { crmService } from '@/services/crmService';
import { Button } from '@/components/ui/Button';
import { ArrowLeft, MessageSquare, CheckSquare, Calendar, Clock, Sparkles, Send, Copy, AlertCircle } from 'lucide-react';
import { cn } from '@/utils/cn';
import { useQueryClient } from '@tanstack/react-query';

export default function LeadCRMPage() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const queryClient = useQueryClient();
  
  const { data: business, isLoading: businessLoading } = useGetBusiness(id || null);
  const { data: conversations, isLoading: convLoading } = useGetConversations(id || null);
  const { data: tasks, isLoading: tasksLoading } = useGetTasks(id);
  const { data: timeline, isLoading: timelineLoading } = useGetTimeline(id || null);
  const { mutate: generateDocument, isPending: isGeneratingDoc } = useGenerateDocument();
  
  const [activeTab, setActiveTab] = useState<'conversations' | 'tasks' | 'timeline'>('conversations');
  const [newMessage, setNewMessage] = useState('');
  const [isGenerating, setIsGenerating] = useState(false);
  const [isAdding, setIsAdding] = useState(false);
  const [aiReplies, setAiReplies] = useState<any>(null);
  
  const handleAddConversation = async () => {
    if (!newMessage.trim() || !id) return;
    setIsAdding(true);
    try {
      await crmService.addConversation(id, { type: 'note', message: newMessage, sender: 'user' });
      setNewMessage('');
      queryClient.invalidateQueries({ queryKey: ['crm', 'conversations', id] });
      queryClient.invalidateQueries({ queryKey: ['crm', 'timeline', id] });
    } finally {
      setIsAdding(false);
    }
  };

  const handleGenerateReply = async () => {
    if (!newMessage.trim()) return;
    setIsGenerating(true);
    try {
      const result = await crmService.generateReply(newMessage);
      setAiReplies(result);
    } finally {
      setIsGenerating(false);
    }
  };

  if (businessLoading) return <div className="p-8 flex justify-center">Loading Lead Data...</div>;

  return (
    <div className="h-full flex flex-col pt-2 pb-6">
      <div className="mb-6 flex justify-between items-center">
        <div className="flex items-center gap-4">
          <Button variant="outline" size="sm" onClick={() => navigate('/dashboard/crm')} className="gap-2">
            <ArrowLeft size={14} /> Back to CRM
          </Button>
          <div>
            <h1 className="text-2xl font-bold tracking-tight">{business?.business_name}</h1>
            <p className="text-primary/60 text-sm mt-0.5">Manage interactions and history.</p>
          </div>
        </div>
        
        <div className="flex items-center gap-2">
           <Button 
             className="gap-2 bg-accent text-background hover:bg-accent-hover"
             disabled={isGeneratingDoc}
             onClick={() => {
               if(id) {
                 generateDocument({ lead_id: id, type: 'proposal' }, {
                   onSuccess: (data) => navigate(`/dashboard/documents/${data.id}`)
                 });
               }
             }}
           >
             <Sparkles size={16} /> 
             {isGeneratingDoc ? 'Generating Proposal...' : 'Generate Proposal'}
           </Button>
        </div>
      </div>

      <div className="flex gap-6 flex-1 min-h-0">
        {/* Main Panel */}
        <div className="flex-1 flex flex-col bg-surface/20 rounded-xl border border-border/50 overflow-hidden">
          {/* Tabs */}
          <div className="flex border-b border-border/50 bg-surface/30">
            <button 
              className={cn("flex-1 py-3 text-sm font-medium border-b-2 flex justify-center items-center gap-2", activeTab === 'conversations' ? "border-primary text-primary" : "border-transparent text-primary/60 hover:text-primary")}
              onClick={() => setActiveTab('conversations')}
            ><MessageSquare size={14} /> Conversations</button>
            <button 
              className={cn("flex-1 py-3 text-sm font-medium border-b-2 flex justify-center items-center gap-2", activeTab === 'tasks' ? "border-primary text-primary" : "border-transparent text-primary/60 hover:text-primary")}
              onClick={() => setActiveTab('tasks')}
            ><CheckSquare size={14} /> Tasks</button>
            <button 
              className={cn("flex-1 py-3 text-sm font-medium border-b-2 flex justify-center items-center gap-2", activeTab === 'timeline' ? "border-primary text-primary" : "border-transparent text-primary/60 hover:text-primary")}
              onClick={() => setActiveTab('timeline')}
            ><Clock size={14} /> Timeline</button>
          </div>

          {/* Content */}
          <div className="flex-1 overflow-y-auto p-6 relative">
            {activeTab === 'conversations' && (
              <div className="space-y-6">
                <div className="bg-background rounded-xl border border-border/50 p-4">
                  <textarea 
                    className="w-full bg-transparent resize-none outline-none text-sm min-h-[80px]"
                    placeholder="Log a conversation, note, or client reply..."
                    value={newMessage}
                    onChange={(e) => setNewMessage(e.target.value)}
                  />
                  <div className="flex justify-between items-center mt-3 pt-3 border-t border-border/50">
                    <Button variant="outline" size="sm" className="gap-2 text-accent border-accent/20 hover:bg-accent/10" onClick={handleGenerateReply} disabled={isGenerating || !newMessage.trim()}>
                      <Sparkles size={14} /> {isGenerating ? 'Generating...' : 'AI Reply'}
                    </Button>
                    <Button size="sm" className="gap-2" onClick={handleAddConversation} disabled={isAdding || !newMessage.trim()}>
                      <Send size={14} /> {isAdding ? 'Saving...' : 'Log Note'}
                    </Button>
                  </div>
                </div>

                {aiReplies && (
                  <div className="bg-accent/5 rounded-xl border border-accent/20 p-4 space-y-4">
                    <div className="flex justify-between items-center">
                      <h4 className="font-semibold text-accent flex items-center gap-2"><Sparkles size={14} /> AI Suggestions</h4>
                      <button onClick={() => setAiReplies(null)} className="text-xs text-primary/50 hover:text-primary">Dismiss</button>
                    </div>
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                      {aiReplies.replies.map((reply: string, i: number) => (
                        <div key={i} className="p-3 bg-background rounded-lg border border-border/50 text-sm relative group">
                          <p className="line-clamp-4">{reply}</p>
                          <button 
                            className="absolute top-2 right-2 p-1.5 bg-surface rounded opacity-0 group-hover:opacity-100 transition-opacity"
                            onClick={() => navigator.clipboard.writeText(reply)}
                          >
                            <Copy size={12} />
                          </button>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                <div className="space-y-4">
                  {convLoading ? <div className="text-center p-4">Loading...</div> : conversations?.map(conv => (
                    <div key={conv.id} className="p-4 bg-background rounded-xl border border-border/50">
                      <div className="flex justify-between items-center mb-2">
                        <span className="text-xs font-medium uppercase tracking-wider text-primary/60">{conv.type} • {conv.sender}</span>
                        <span className="text-xs text-primary/40">{new Date(conv.created_at).toLocaleString()}</span>
                      </div>
                      <p className="text-sm whitespace-pre-wrap">{conv.message}</p>
                      
                      {conv.analysis && (
                         <div className="mt-4 p-3 bg-accent/5 border border-accent/20 rounded-lg text-xs space-y-2">
                           <p className="font-semibold text-accent flex items-center gap-1.5"><Sparkles size={12}/> AI Analysis</p>
                           <p><span className="text-primary/50">Intent:</span> {conv.analysis.buying_intent}</p>
                           <p><span className="text-primary/50">Next Action:</span> {conv.analysis.next_action}</p>
                         </div>
                      )}
                    </div>
                  ))}
                </div>
              </div>
            )}

            {activeTab === 'timeline' && (
              <div className="space-y-6 relative before:absolute before:inset-0 before:ml-5 before:-translate-x-px md:before:mx-auto md:before:translate-x-0 before:h-full before:w-0.5 before:bg-gradient-to-b before:from-transparent before:via-border/50 before:to-transparent">
                {timelineLoading ? <div className="text-center">Loading...</div> : timeline?.map((event) => (
                   <div key={event.id} className="relative flex items-center justify-between md:justify-normal md:odd:flex-row-reverse group is-active">
                     <div className="flex items-center justify-center w-10 h-10 rounded-full border-4 border-background bg-surface/50 text-primary/60 shrink-0 md:order-1 md:group-odd:-translate-x-1/2 md:group-even:translate-x-1/2 z-10 shadow-sm">
                       <Clock size={14} />
                     </div>
                     <div className="w-[calc(100%-4rem)] md:w-[calc(50%-2.5rem)] p-4 rounded-xl border border-border/50 bg-background">
                       <div className="flex items-center justify-between space-x-2 mb-1">
                         <div className="font-bold text-sm text-primary">{event.event_type}</div>
                         <time className="font-mono text-xs text-primary/40">{new Date(event.created_at).toLocaleDateString()}</time>
                       </div>
                       <div className="text-sm text-primary/70">{event.description}</div>
                     </div>
                   </div>
                ))}
              </div>
            )}
            
            {activeTab === 'tasks' && (
              <div className="space-y-4">
                 {tasksLoading ? <div className="text-center p-4">Loading...</div> : tasks?.map(task => (
                   <div key={task.id} className="flex items-center justify-between p-4 bg-background rounded-xl border border-border/50">
                     <div className="flex items-center gap-3">
                       <div className={cn("w-5 h-5 rounded-full border flex items-center justify-center", task.completed ? "bg-emerald-500 border-emerald-500" : "border-border/50")}>
                         {task.completed && <CheckSquare size={12} className="text-background" />}
                       </div>
                       <div>
                         <p className={cn("text-sm font-medium", task.completed && "line-through text-primary/40")}>{task.title}</p>
                         {task.due_date && <p className="text-xs text-primary/50 mt-0.5">Due: {new Date(task.due_date).toLocaleDateString()}</p>}
                       </div>
                     </div>
                   </div>
                 ))}
                 <Button className="w-full gap-2 bg-surface hover:bg-surface/80" variant="secondary"><CheckSquare size={14} /> Add Task</Button>
              </div>
            )}
          </div>
        </div>

        {/* Right Sidebar (AI CRM Intelligence) */}
        <div className="w-80 flex flex-col gap-4 overflow-y-auto">
          <div className="p-4 rounded-xl border border-accent/20 bg-accent/5 h-full">
            <h3 className="font-semibold text-sm uppercase tracking-wider text-accent mb-4 flex items-center gap-2">
              <Sparkles size={14} /> Relationship IQ
            </h3>
            <div className="space-y-4">
              <div className="bg-background p-3 rounded-lg border border-border/50">
                <p className="text-xs text-primary/50 flex items-center gap-1.5"><AlertCircle size={12} className="text-yellow-500" /> Pending Action</p>
                <p className="text-sm font-medium mt-1">Follow up on Pricing</p>
              </div>
              <div className="bg-background p-3 rounded-lg border border-border/50 space-y-2">
                <p className="text-xs text-primary/50 flex items-center gap-1.5"><Calendar size={12} className="text-blue-500" /> Suggested Schedule</p>
                <p className="text-sm font-medium">Tomorrow, 10:00 AM</p>
                <Button size="sm" variant="outline" className="w-full text-xs">Create Task</Button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
