import { useState, useRef, useEffect } from 'react';
import { useCopilotChat, useGetCopilotHistory } from '@/hooks/useCopilot';
import { useScoutStore } from '@/store/scoutStore';
import { Sparkles, Send, Brain, Bot, User, Clock, Target, LayoutDashboard } from 'lucide-react';
import { cn } from '@/utils/cn';

interface Message {
  role: 'user' | 'assistant';
  content: string;
}

export default function CopilotPage() {
  const { selectedLeadId } = useScoutStore();
  const { data: history } = useGetCopilotHistory();
  const { mutate: sendChat, isPending } = useCopilotChat();
  
  const [messages, setMessages] = useState<Message[]>([
    { role: 'assistant', content: 'Hello! I am your ScoutAI Copilot. I understand your entire workspace, leads, and CRM status. How can I help you today?' }
  ]);
  const [input, setInput] = useState('');
  const [chatId, setChatId] = useState<string | undefined>(undefined);
  const [suggestions, setSuggestions] = useState<string[]>([
    "Find all businesses with Opportunity Score above 90.",
    "Show clients I forgot to follow up with.",
    "Summarize today's work."
  ]);
  
  const bottomRef = useRef<HTMLDivElement>(null);
  
  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, isPending]);

  const handleSend = (text: string) => {
    if (!text.trim() || isPending) return;
    
    const userMsg = text.trim();
    setMessages(prev => [...prev, { role: 'user', content: userMsg }]);
    setInput('');
    setSuggestions([]);
    
    sendChat({ 
      message: userMsg, 
      chat_id: chatId,
      current_context: selectedLeadId ? { lead_id: selectedLeadId } : undefined
    }, {
      onSuccess: (data) => {
        setChatId(data.chat_id);
        setMessages(prev => [...prev, { role: 'assistant', content: data.message.message }]);
        if (data.suggested_actions?.length > 0) {
          setSuggestions(data.suggested_actions);
        }
      }
    });
  };

  return (
    <div className="h-full flex flex-col pt-2 pb-6">
      <div className="mb-6 flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold tracking-tight flex items-center gap-2">
            <Bot className="text-accent" size={24} /> AI Copilot
          </h1>
          <p className="text-primary/60 mt-1">Your intelligent business assistant that understands your entire workspace.</p>
        </div>
      </div>

      <div className="flex-1 min-h-0 flex gap-6">
        {/* Left: Chat History */}
        <div className="w-64 flex flex-col gap-2 overflow-y-auto pr-2 border-r border-border/50">
          <h3 className="font-semibold text-sm uppercase tracking-wider text-primary/50 mb-2 px-2 flex items-center gap-2">
            <Clock size={14} /> Recent Chats
          </h3>
          {history?.map(chat => (
            <button key={chat.id} className="text-left px-3 py-2 rounded-lg hover:bg-surface/50 text-sm truncate text-primary/80 transition-colors">
              {chat.title}
            </button>
          ))}
          {!history?.length && <p className="text-xs text-primary/40 px-2">No previous chats.</p>}
        </div>

        {/* Center: Chat Area */}
        <div className="flex-1 flex flex-col min-w-0 bg-background border border-border/50 rounded-xl overflow-hidden relative">
          <div className="flex-1 overflow-y-auto p-6 space-y-6">
            {messages.map((msg, i) => (
              <div key={i} className={cn("flex gap-4 max-w-[85%]", msg.role === 'user' ? "ml-auto flex-row-reverse" : "")}>
                <div className={cn("w-8 h-8 rounded-full flex items-center justify-center shrink-0 mt-1", msg.role === 'user' ? "bg-primary text-background" : "bg-accent/10 text-accent")}>
                  {msg.role === 'user' ? <User size={14} /> : <Sparkles size={14} />}
                </div>
                <div className={cn("p-4 rounded-2xl", msg.role === 'user' ? "bg-surface/50" : "bg-accent/5 border border-accent/10")}>
                  <p className="text-sm whitespace-pre-wrap leading-relaxed">{msg.content}</p>
                </div>
              </div>
            ))}
            
            {isPending && (
              <div className="flex gap-4 max-w-[85%]">
                <div className="w-8 h-8 rounded-full bg-accent/10 text-accent flex items-center justify-center shrink-0 mt-1">
                  <Brain size={14} className="animate-pulse" />
                </div>
                <div className="p-4 rounded-2xl bg-accent/5 border border-accent/10 flex items-center gap-2">
                  <div className="flex gap-1">
                    <span className="w-1.5 h-1.5 rounded-full bg-accent animate-bounce" style={{ animationDelay: '0ms' }} />
                    <span className="w-1.5 h-1.5 rounded-full bg-accent animate-bounce" style={{ animationDelay: '150ms' }} />
                    <span className="w-1.5 h-1.5 rounded-full bg-accent animate-bounce" style={{ animationDelay: '300ms' }} />
                  </div>
                  <span className="text-xs font-medium text-accent ml-2">Collecting Context & Thinking...</span>
                </div>
              </div>
            )}
            <div ref={bottomRef} />
          </div>
          
          <div className="p-4 bg-surface/30 border-t border-border/50">
            {suggestions.length > 0 && (
              <div className="flex flex-wrap gap-2 mb-3">
                {suggestions.map((sug, i) => (
                  <button 
                    key={i} 
                    className="text-xs px-3 py-1.5 rounded-full border border-border hover:border-accent hover:text-accent bg-background transition-colors"
                    onClick={() => handleSend(sug)}
                  >
                    {sug}
                  </button>
                ))}
              </div>
            )}
            <div className="relative">
              <input 
                type="text"
                placeholder="Ask me anything about your business, leads, or tasks..."
                className="w-full bg-background border border-border/50 rounded-xl pl-4 pr-12 py-3 text-sm focus:border-accent outline-none"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={(e) => e.key === 'Enter' && handleSend(input)}
              />
              <button 
                className="absolute right-2 top-1/2 -translate-y-1/2 w-8 h-8 flex items-center justify-center rounded-lg bg-accent text-background hover:bg-accent-hover transition-colors disabled:opacity-50"
                onClick={() => handleSend(input)}
                disabled={!input.trim() || isPending}
              >
                <Send size={14} />
              </button>
            </div>
          </div>
        </div>

        {/* Right: Context Panel */}
        <div className="w-64 flex flex-col gap-4 overflow-y-auto pl-2">
          <div className="p-4 rounded-xl border border-accent/20 bg-accent/5 h-full">
            <h3 className="font-semibold text-sm uppercase tracking-wider text-accent mb-4 flex items-center gap-2">
              <Target size={14} /> Current AI Context
            </h3>
            
            <div className="space-y-4">
              <div className="bg-background p-3 rounded-lg border border-border/50">
                <p className="text-xs text-primary/50 flex items-center gap-1.5 mb-1"><LayoutDashboard size={12} /> Scope</p>
                <p className="text-sm font-medium">Global Workspace</p>
                <p className="text-xs text-primary/60 mt-1">AI has access to all CRM data, Timeline events, and Task history.</p>
              </div>
              
              {selectedLeadId && (
                <div className="bg-background p-3 rounded-lg border border-accent/30 shadow-[0_0_15px_-3px_rgba(var(--accent),0.1)]">
                  <p className="text-xs text-accent flex items-center gap-1.5 mb-1"><Target size={12} /> Active Focus</p>
                  <p className="text-sm font-medium">Selected Lead</p>
                  <p className="text-xs text-primary/60 mt-1">AI is prioritizing context for your currently selected business.</p>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
