import { useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useGetBusiness } from '@/hooks/useScout';
import { useGetBusinessAnalysis } from '@/hooks/useAI';
import { useGenerateMessage } from '@/hooks/useOutreach';
import { type MessageVariation, type GenerateMessageRequest } from '@/services/outreachService';
import { Button } from '@/components/ui/Button';
import { ArrowLeft, Copy, Sparkles, RefreshCw, Bookmark, Clock, Zap, Target, TrendingUp, CheckCircle2, MessageSquare } from 'lucide-react';
import { cn } from '@/utils/cn';

export default function OutreachPage() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const { data: business, isLoading: businessLoading } = useGetBusiness(id || null);
  const { data: aiData, isLoading: aiLoading } = useGetBusinessAnalysis(id || null);
  const { mutate: generateMessage, isPending } = useGenerateMessage();
  
  const [params, setParams] = useState<GenerateMessageRequest>({
    message_type: 'Cold Email',
    tone: 'Professional',
    language: 'English',
    length: 'Medium',
    cta_style: 'Soft',
    personalization_level: 'Medium'
  });
  
  const [variations, setVariations] = useState<MessageVariation[]>([]);
  const [activeVersion, setActiveVersion] = useState<number>(0);
  const [statusText, setStatusText] = useState('');

  const handleGenerate = () => {
    if (!id) return;
    setStatusText('Reading Business Profile...');
    setTimeout(() => setStatusText('Understanding Website...'), 1500);
    setTimeout(() => setStatusText('Creating Personalized Message...'), 3000);
    setTimeout(() => setStatusText('Finalizing Outreach...'), 4500);
    
    generateMessage({ businessId: id, params }, {
      onSuccess: (data) => {
        setVariations(data.variations);
        setActiveVersion(0);
      }
    });
  };

  const handleCopy = (text: string) => {
    navigator.clipboard.writeText(text);
  };

  const isLoading = businessLoading || aiLoading;

  if (isLoading) {
    return <div className="h-full flex items-center justify-center">Loading...</div>;
  }

  const activeVariation = variations[activeVersion];

  return (
    <div className="h-full flex flex-col pt-2 pb-6">
      <div className="mb-6 flex items-center gap-4">
        <Button variant="outline" size="sm" onClick={() => navigate('/dashboard')} className="gap-2">
          <ArrowLeft size={14} /> Back
        </Button>
        <div>
          <h1 className="text-2xl font-bold tracking-tight flex items-center gap-2">
            AI Outreach <Sparkles className="text-accent" size={18} />
          </h1>
          <p className="text-primary/60 mt-1">Generate personalized messages for {business?.business_name}</p>
        </div>
      </div>

      <div className="flex-1 min-h-0 flex gap-6">
        {/* Left: Business Info & Controls */}
        <div className="w-80 flex flex-col gap-4 overflow-y-auto pr-2">
          <div className="p-4 rounded-xl border border-border/50 bg-background/50">
            <h3 className="font-semibold text-sm uppercase tracking-wider text-primary/50 mb-3">Target Profile</h3>
            <div className="space-y-3">
              <div>
                <p className="text-xs text-primary/50">Company</p>
                <p className="font-medium">{business?.business_name}</p>
              </div>
              <div>
                <p className="text-xs text-primary/50">Industry</p>
                <p className="font-medium text-sm">{business?.category}</p>
              </div>
              <div>
                <p className="text-xs text-primary/50">Opportunity Score</p>
                <p className={cn("font-bold", aiData?.opportunity_score ? "text-emerald-500" : "")}>
                  {aiData?.opportunity_score || 'N/A'}
                </p>
              </div>
            </div>
          </div>

          <div className="p-4 rounded-xl border border-border/50 bg-surface/30 flex-1">
            <h3 className="font-semibold text-sm uppercase tracking-wider text-primary/50 mb-4">Outreach Settings</h3>
            
            <div className="space-y-4">
              <div>
                <label className="text-xs font-medium mb-1.5 block">Channel</label>
                <select 
                  className="w-full bg-background border border-border/50 rounded-lg p-2 text-sm focus:border-primary outline-none"
                  value={params.message_type}
                  onChange={(e) => setParams({...params, message_type: e.target.value})}
                >
                  <option>Cold Email</option>
                  <option>LinkedIn Message</option>
                  <option>WhatsApp</option>
                  <option>Cold Call Script</option>
                  <option>Follow-up</option>
                </select>
              </div>
              
              <div>
                <label className="text-xs font-medium mb-1.5 block">Tone</label>
                <select 
                  className="w-full bg-background border border-border/50 rounded-lg p-2 text-sm focus:border-primary outline-none"
                  value={params.tone}
                  onChange={(e) => setParams({...params, tone: e.target.value})}
                >
                  <option>Professional</option>
                  <option>Friendly</option>
                  <option>Confident</option>
                  <option>Consultative</option>
                </select>
              </div>

              <div>
                <label className="text-xs font-medium mb-1.5 block">Personalization</label>
                <select 
                  className="w-full bg-background border border-border/50 rounded-lg p-2 text-sm focus:border-primary outline-none"
                  value={params.personalization_level}
                  onChange={(e) => setParams({...params, personalization_level: e.target.value})}
                >
                  <option>Basic</option>
                  <option>Medium</option>
                  <option>Deep</option>
                </select>
              </div>
              
              <Button 
                onClick={handleGenerate} 
                disabled={isPending}
                className="w-full gap-2 mt-4 bg-accent text-background hover:bg-accent-hover"
              >
                {isPending ? <RefreshCw size={16} className="animate-spin" /> : <Zap size={16} />}
                {variations.length > 0 ? 'Regenerate Options' : 'Generate Outreach'}
              </Button>
            </div>
          </div>
        </div>

        {/* Center: Generated Message */}
        <div className="flex-1 flex flex-col min-w-0 bg-background border border-border/50 rounded-xl overflow-hidden relative">
          {isPending && (
             <div className="absolute inset-0 z-20 flex flex-col items-center justify-center bg-background/80 backdrop-blur-sm">
               <div className="w-16 h-16 border-4 border-accent/20 border-t-accent rounded-full animate-spin mb-4" />
               <p className="font-medium text-lg text-accent animate-pulse">{statusText}</p>
             </div>
          )}

          {!variations.length && !isPending ? (
            <div className="flex-1 flex flex-col items-center justify-center text-primary/40 p-10 text-center">
              <MessageSquare size={48} className="mb-4 opacity-20" />
              <p className="font-medium text-lg text-primary/60">No Message Generated Yet</p>
              <p className="text-sm mt-2 max-w-sm">Configure your settings on the left and click Generate to create highly personalized outreach messages.</p>
            </div>
          ) : activeVariation ? (
            <>
              <div className="px-6 py-4 border-b border-border/50 bg-surface/30 flex justify-between items-center">
                <div className="flex gap-2">
                  {variations.map((v, i) => (
                    <button
                      key={i}
                      onClick={() => setActiveVersion(i)}
                      className={cn(
                        "px-4 py-1.5 rounded-lg text-sm font-medium transition-colors border",
                        activeVersion === i 
                          ? "bg-accent/10 border-accent/20 text-accent" 
                          : "bg-background border-border/50 text-primary/60 hover:text-primary"
                      )}
                    >
                      {v.version}
                    </button>
                  ))}
                </div>
                <div className="flex gap-2">
                  <Button variant="outline" size="sm" className="gap-2" onClick={() => handleCopy(activeVariation.full_message)}>
                    <Copy size={14} /> Copy
                  </Button>
                  <Button variant="outline" size="sm" className="gap-2">
                    <Bookmark size={14} /> Save Template
                  </Button>
                </div>
              </div>
              <div className="flex-1 overflow-y-auto p-6 relative">
                 <textarea 
                   className="w-full h-full min-h-[400px] bg-transparent resize-none outline-none leading-relaxed text-[15px]"
                   value={activeVariation.full_message}
                   readOnly
                 />
              </div>
            </>
          ) : null}
        </div>

        {/* Right: AI Suggestions */}
        <div className="w-80 flex flex-col gap-4 overflow-y-auto pl-2">
          <div className="p-4 rounded-xl border border-accent/20 bg-accent/5">
            <h3 className="font-semibold text-sm uppercase tracking-wider text-accent mb-4 flex items-center gap-2">
              <Sparkles size={14} /> AI Suggestions
            </h3>
            
            {!activeVariation ? (
              <p className="text-sm text-primary/40 text-center py-10">Generate a message to see AI strategy recommendations.</p>
            ) : (
              <div className="space-y-4">
                <div className="flex items-center gap-3 bg-background p-3 rounded-lg border border-border/50">
                  <Clock size={16} className="text-blue-500" />
                  <div>
                    <p className="text-xs text-primary/50">Best Time to Contact</p>
                    <p className="text-sm font-medium">{activeVariation.ai_suggestions?.best_time || 'Tuesday, 10 AM'}</p>
                  </div>
                </div>
                
                <div className="flex items-center gap-3 bg-background p-3 rounded-lg border border-border/50">
                  <Target size={16} className="text-emerald-500" />
                  <div>
                    <p className="text-xs text-primary/50">Recommended Channel</p>
                    <p className="text-sm font-medium">{activeVariation.ai_suggestions?.recommended_channel || 'Cold Email'}</p>
                  </div>
                </div>

                <div className="bg-background p-3 rounded-lg border border-border/50 space-y-2">
                  <p className="text-xs text-primary/50 flex items-center gap-1.5"><TrendingUp size={12} className="text-red-500" /> Likely Pain Points</p>
                  <div className="space-y-1">
                    {(activeVariation.ai_suggestions?.likely_pain_points || ['Lack of SEO', 'Outdated Website']).map((pp, i) => (
                      <p key={i} className="text-xs font-medium flex items-start gap-1.5">
                        <span className="text-accent mt-0.5">•</span> {pp}
                      </p>
                    ))}
                  </div>
                </div>

                <div className="flex items-center gap-3 bg-background p-3 rounded-lg border border-border/50">
                  <CheckCircle2 size={16} className="text-accent" />
                  <div>
                    <p className="text-xs text-primary/50">Reply Probability</p>
                    <p className="text-sm font-medium">{activeVariation.ai_suggestions?.reply_probability || 'High (65%)'}</p>
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
