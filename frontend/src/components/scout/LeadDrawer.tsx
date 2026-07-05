import { useState } from 'react';
import { useScoutStore } from '@/store/scoutStore';
import { useGetBusiness } from '@/hooks/useScout';
import { useGetBusinessAnalysis, useAnalyzeBusiness } from '@/hooks/useAI';
import { X, ExternalLink, Mail, Phone, MapPin, Building, Star, Globe, Briefcase, MessageSquare, Sparkles, TrendingUp, AlertCircle, Target, CheckCircle2, Zap } from 'lucide-react';
import { Button } from '@/components/ui/Button';
import { cn } from '@/utils/cn';
import { motion, AnimatePresence } from 'framer-motion';

export const LeadDrawer = () => {
  const { selectedLeadId, isDrawerOpen, setIsDrawerOpen, setSelectedLeadId } = useScoutStore();
  const { data: business, isLoading } = useGetBusiness(selectedLeadId);
  const { data: aiData } = useGetBusinessAnalysis(selectedLeadId);
  const analyzeMutation = useAnalyzeBusiness();
  const [activeTab, setActiveTab] = useState('overview');
  const [aiStatus, setAiStatus] = useState('');

  const handleAnalyze = () => {
    if (!selectedLeadId) return;
    setAiStatus('Analyzing Business...');
    setTimeout(() => setAiStatus('Understanding Website...'), 1500);
    setTimeout(() => setAiStatus('Generating Insights...'), 3500);
    setTimeout(() => setAiStatus('Almost Done...'), 6000);
    
    analyzeMutation.mutate(selectedLeadId, {
      onSettled: () => setAiStatus(''),
      onSuccess: () => setActiveTab('ai_analysis')
    });
  };

  const tabs = [
    { id: 'overview', label: 'Overview' },
    { id: 'contact', label: 'Contact' },
    { id: 'ai_analysis', label: 'AI Analysis' },
    { id: 'website', label: 'Website' },
    { id: 'social', label: 'Social' },
    { id: 'notes', label: 'Notes' },
    { id: 'history', label: 'History' },
    { id: 'discovery', label: 'Discovery Details' },
    { id: 'raw_source', label: 'Raw Source' },
  ];

  // Close drawer
  const closeDrawer = () => {
    setIsDrawerOpen(false);
    setTimeout(() => setSelectedLeadId(null), 300); // Wait for exit animation
  };

  return (
    <AnimatePresence>
      {isDrawerOpen && (
        <>
          {/* Backdrop */}
          <motion.div 
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 bg-background/80 backdrop-blur-sm z-50"
            onClick={closeDrawer}
          />
          
          {/* Drawer */}
          <motion.div 
            initial={{ x: '100%' }}
            animate={{ x: 0 }}
            exit={{ x: '100%' }}
            transition={{ type: "spring", bounce: 0, duration: 0.4 }}
            className="fixed inset-y-0 right-0 w-full max-w-md bg-background border-l border-border/50 shadow-2xl z-50 flex flex-col"
          >
            {/* Header */}
            <div className="p-6 border-b border-border/50 flex items-start justify-between bg-surface/30">
              <div className="flex-1 min-w-0 pr-4">
                {isLoading ? (
                  <div className="space-y-2">
                    <div className="h-6 bg-surface rounded animate-pulse w-2/3" />
                    <div className="h-4 bg-surface rounded animate-pulse w-1/3" />
                  </div>
                ) : (
                  <>
                    <div className="flex items-center gap-2 mb-1">
                      <h2 className="text-xl font-bold truncate">{business?.business_name}</h2>
                      {business?.website && (
                        <a href={`https://${business.website}`} target="_blank" rel="noreferrer" className="text-primary/40 hover:text-primary transition-colors">
                          <ExternalLink size={14} />
                        </a>
                      )}
                    </div>
                    <div className="flex items-center gap-2 text-sm text-primary/60">
                      <span className="uppercase text-[10px] tracking-wider font-medium bg-surface px-1.5 py-0.5 rounded text-primary">
                        {business?.category || 'Uncategorized'}
                      </span>
                      <span>•</span>
                      <span className="flex items-center gap-1"><MapPin size={12} /> {business?.city || 'Unknown Location'}</span>
                    </div>
                    {/* Quick AI Tags if analyzed */}
                    {aiData && (
                      <div className="flex flex-wrap gap-1.5 mt-2">
                        {aiData.ai_tags.map(tag => (
                          <span key={tag} className="text-[10px] font-medium bg-accent/10 text-accent px-1.5 py-0.5 rounded border border-accent/20">
                            {tag}
                          </span>
                        ))}
                      </div>
                    )}
                  </>
                )}
              </div>
              <button 
                onClick={closeDrawer}
                className="p-2 rounded-lg bg-surface/50 hover:bg-surface text-primary/60 hover:text-primary transition-colors"
              >
                <X size={16} />
              </button>
            </div>

            {/* Quick Actions */}
            <div className="px-6 py-3 border-b border-border/50 bg-background flex gap-2">
              <Button size="sm" className="flex-1 gap-2"><Briefcase size={14} /> Save Lead</Button>
              <Button size="sm" variant="outline" className="flex-1 gap-2"><MessageSquare size={14} /> Draft Email</Button>
            </div>

            {/* Tabs */}
            <div className="flex overflow-x-auto border-b border-border/50 px-6 scrollbar-hide">
              {tabs.map(tab => (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={cn(
                    "px-1 py-3 text-sm font-medium border-b-2 whitespace-nowrap mr-6 transition-colors flex items-center gap-1.5",
                    activeTab === tab.id ? "border-primary text-primary" : "border-transparent text-primary/50 hover:text-primary/80",
                    tab.id === 'ai_analysis' && "text-accent border-accent/50 hover:text-accent-hover"
                  )}
                >
                  {tab.id === 'ai_analysis' && <Sparkles size={14} />}
                  {tab.label}
                </button>
              ))}
            </div>

            {/* Content Area */}
            <div className="flex-1 overflow-y-auto p-6 bg-surface/10 relative">
              {analyzeMutation.isPending && (
                <div className="absolute inset-0 z-20 flex flex-col items-center justify-center bg-background/80 backdrop-blur-sm">
                  <div className="w-16 h-16 border-4 border-accent/20 border-t-accent rounded-full animate-spin mb-4" />
                  <p className="font-medium text-lg text-accent animate-pulse">{aiStatus}</p>
                </div>
              )}
              
              {isLoading ? (
                <div className="space-y-6">
                  {Array.from({ length: 3 }).map((_, i) => (
                    <div key={i} className="space-y-2">
                      <div className="h-4 bg-surface rounded animate-pulse w-1/4" />
                      <div className="h-16 bg-surface rounded animate-pulse w-full" />
                    </div>
                  ))}
                </div>
              ) : (
                <div className="space-y-8 pb-10">
                  {/* Overview Tab */}
                  <div className={cn("space-y-6", activeTab === 'overview' ? 'block' : 'hidden')}>
                    {!aiData ? (
                      <div className="p-6 rounded-xl bg-accent/5 border border-accent/20 relative overflow-hidden flex flex-col items-center text-center">
                        <div className="absolute -right-4 -top-4 w-32 h-32 bg-accent/10 rounded-full blur-2xl pointer-events-none" />
                        <div className="w-12 h-12 bg-accent/10 rounded-full flex items-center justify-center mb-3">
                          <Zap size={24} className="text-accent" />
                        </div>
                        <h4 className="font-semibold text-lg mb-1">Generate AI Insights</h4>
                        <p className="text-sm text-primary/60 mb-4 max-w-xs">
                          Let Scout Engine analyze this business to uncover strengths, weaknesses, and potential services you can offer.
                        </p>
                        <Button onClick={handleAnalyze} className="gap-2 bg-accent text-background hover:bg-accent-hover">
                          <Sparkles size={14} /> Analyze Business
                        </Button>
                      </div>
                    ) : (
                      <div className="p-5 rounded-xl bg-accent/5 border border-accent/20 cursor-pointer hover:bg-accent/10 transition-colors" onClick={() => setActiveTab('ai_analysis')}>
                        <div className="flex items-center justify-between mb-4">
                          <h4 className="text-xs font-semibold text-accent uppercase tracking-wider flex items-center gap-1.5">
                            <Star size={12} className="fill-accent text-accent" /> AI Overview Available
                          </h4>
                          <span className="text-xs text-primary/50">Click to view details</span>
                        </div>
                        <p className="text-sm text-primary/80 leading-relaxed font-medium">
                          {aiData.summary_short}
                        </p>
                      </div>
                    )}

                    <div className="grid grid-cols-2 gap-4">
                      <div className="p-3 rounded-lg border border-border/50 bg-background">
                        <p className="text-xs text-primary/50 mb-1">Google Rating</p>
                        <p className="font-semibold text-lg">{business?.google_rating || 'N/A'}</p>
                      </div>
                      <div className="p-3 rounded-lg border border-border/50 bg-background">
                        <p className="text-xs text-primary/50 mb-1">Reviews</p>
                        <p className="font-semibold text-lg">{business?.review_count || '0'}</p>
                      </div>
                    </div>
                  </div>

                  {/* AI Analysis Tab */}
                  <div className={cn("space-y-6", activeTab === 'ai_analysis' ? 'block' : 'hidden')}>
                    {!aiData && !analyzeMutation.isPending && (
                       <div className="text-center p-8">
                         <p className="text-primary/60 mb-4">No AI analysis available for this business yet.</p>
                         <Button onClick={handleAnalyze} className="gap-2 bg-accent text-background hover:bg-accent-hover">
                           <Sparkles size={14} /> Generate Analysis
                         </Button>
                       </div>
                    )}

                    {aiData && (
                      <>
                        <div className="grid grid-cols-2 gap-4">
                          <div className="p-4 rounded-xl border border-border/50 bg-background flex flex-col justify-between">
                            <p className="text-xs text-primary/50 uppercase tracking-wider font-semibold mb-2 flex items-center gap-1.5"><Target size={14} className="text-emerald-500" /> Opportunity Score</p>
                            <div className="flex items-end gap-2">
                              <span className={cn("text-4xl font-bold tracking-tighter", 
                                aiData.opportunity_score >= 80 ? 'text-emerald-500' : 
                                aiData.opportunity_score >= 50 ? 'text-yellow-500' : 'text-red-500'
                              )}>
                                {aiData.opportunity_score}
                              </span>
                              <span className="text-sm text-primary/40 mb-1">/ 100</span>
                            </div>
                          </div>
                          <div className="p-4 rounded-xl border border-border/50 bg-background flex flex-col justify-between">
                            <p className="text-xs text-primary/50 uppercase tracking-wider font-semibold mb-2 flex items-center gap-1.5"><TrendingUp size={14} className="text-blue-500" /> Est. Budget</p>
                            <span className="text-2xl font-bold tracking-tight">{aiData.estimated_budget}</span>
                          </div>
                        </div>

                        <div className="space-y-3">
                          <h3 className="font-semibold text-lg flex items-center gap-2"><Sparkles size={16} className="text-accent" /> AI Business Summary</h3>
                          <div className="p-4 rounded-lg border border-border/50 bg-background text-sm text-primary/80 leading-relaxed space-y-4">
                            <p>{aiData.summary_medium}</p>
                            <p className="text-primary/60">{aiData.summary_long}</p>
                          </div>
                        </div>

                        <div className="space-y-3">
                          <h3 className="font-semibold text-lg flex items-center gap-2"><CheckCircle2 size={16} className="text-emerald-500" /> Recommended Services</h3>
                          <div className="flex flex-wrap gap-2">
                            {aiData.recommended_services.map(service => (
                              <div key={service} className="px-3 py-1.5 rounded-lg border border-emerald-500/20 bg-emerald-500/5 text-emerald-500 text-sm font-medium">
                                {service}
                              </div>
                            ))}
                          </div>
                        </div>

                        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                          <div className="space-y-3">
                            <h3 className="font-semibold text-sm flex items-center gap-1.5 text-emerald-500"><TrendingUp size={14} /> Strengths & Opportunities</h3>
                            <div className="p-4 rounded-lg border border-emerald-500/20 bg-emerald-500/5 space-y-2">
                              {aiData.strengths.map((str, i) => (
                                <p key={i} className="text-sm flex items-start gap-2">
                                  <span className="text-emerald-500 mt-0.5">•</span> {str}
                                </p>
                              ))}
                              {aiData.opportunities.map((opp, i) => (
                                <p key={i} className="text-sm flex items-start gap-2">
                                  <span className="text-emerald-500 mt-0.5">•</span> {opp}
                                </p>
                              ))}
                            </div>
                          </div>
                          
                          <div className="space-y-3">
                            <h3 className="font-semibold text-sm flex items-center gap-1.5 text-red-500"><AlertCircle size={14} /> Weaknesses</h3>
                            <div className="p-4 rounded-lg border border-red-500/20 bg-red-500/5 space-y-2 h-full">
                              {aiData.weaknesses.map((wk, i) => (
                                <p key={i} className="text-sm flex items-start gap-2">
                                  <span className="text-red-500 mt-0.5">•</span> {wk}
                                </p>
                              ))}
                            </div>
                          </div>
                        </div>
                      </>
                    )}
                  </div>

                  {/* Contact Tab */}
                  <div className={cn("space-y-4", activeTab === 'contact' ? 'block' : 'hidden')}>
                    <div className="flex items-center gap-3 p-3 rounded-lg border border-border/50 bg-background">
                      <div className="w-8 h-8 rounded bg-surface flex items-center justify-center text-primary/60"><Mail size={14} /></div>
                      <div className="flex-1">
                        <p className="text-xs text-primary/50">Email Address</p>
                        <p className="text-sm font-medium">{business?.email || 'Not available'}</p>
                      </div>
                    </div>
                    <div className="flex items-center gap-3 p-3 rounded-lg border border-border/50 bg-background">
                      <div className="w-8 h-8 rounded bg-surface flex items-center justify-center text-primary/60"><Phone size={14} /></div>
                      <div className="flex-1">
                        <p className="text-xs text-primary/50">Phone Number</p>
                        <p className="text-sm font-medium">{business?.phone || 'Not available'}</p>
                      </div>
                    </div>
                    <div className="flex items-center gap-3 p-3 rounded-lg border border-border/50 bg-background">
                      <div className="w-8 h-8 rounded bg-surface flex items-center justify-center text-primary/60"><Building size={14} /></div>
                      <div className="flex-1">
                        <p className="text-xs text-primary/50">Address</p>
                        <p className="text-sm font-medium">
                          {[business?.city, business?.state, business?.country].filter(Boolean).join(', ') || 'Not available'}
                        </p>
                      </div>
                    </div>
                  </div>

                  {/* Discovery Details Tab */}
                  <div className={cn("space-y-4", activeTab === 'discovery' ? 'block' : 'hidden')}>
                    <div className="grid grid-cols-2 gap-4">
                      <div className="p-3 rounded-lg border border-border/50 bg-background">
                        <p className="text-xs text-primary/50 mb-1">Source Provider</p>
                        <p className="font-semibold text-sm capitalize">{business?.source || 'Manual Entry'}</p>
                      </div>
                      <div className="p-3 rounded-lg border border-border/50 bg-background">
                        <p className="text-xs text-primary/50 mb-1">Confidence Score</p>
                        <p className="font-semibold text-sm">{business?.confidence_score ? `${(business.confidence_score * 100).toFixed(0)}%` : 'N/A'}</p>
                      </div>
                    </div>
                    
                    <div className="p-3 rounded-lg border border-border/50 bg-background space-y-3">
                      <div className="flex justify-between items-center border-b border-border/50 pb-2">
                        <span className="text-sm text-primary/60">Website Status</span>
                        <span className={cn("text-xs px-2 py-1 rounded", business?.website_status === 'reachable' ? 'bg-emerald-500/10 text-emerald-500' : 'bg-surface text-primary/50')}>
                          {business?.website_status || 'Unknown'}
                        </span>
                      </div>
                      <div className="flex justify-between items-center">
                        <span className="text-sm text-primary/60">Last Checked</span>
                        <span className="text-sm">
                          {business?.last_checked ? new Date(business.last_checked).toLocaleDateString() : 'Never'}
                        </span>
                      </div>
                    </div>
                  </div>

                  {/* Raw Source Tab */}
                  <div className={cn("space-y-4", activeTab === 'raw_source' ? 'block' : 'hidden')}>
                    <div className="p-4 rounded-lg border border-border/50 bg-[#0d0d0f] overflow-x-auto">
                      <pre className="text-xs font-mono text-primary/70">
                        {JSON.stringify(business, null, 2)}
                      </pre>
                    </div>
                  </div>

                  {/* Other Tabs (Placeholders) */}
                  {['website', 'social', 'notes', 'history'].map(tab => (
                    <div key={tab} className={cn("flex flex-col items-center justify-center h-48 text-center text-primary/40", activeTab === tab ? 'block' : 'hidden')}>
                      <Globe size={32} className="mb-3 opacity-20" />
                      <p className="text-sm font-medium capitalize">{tab} information</p>
                      <p className="text-xs mt-1">This section will be implemented in future CRM phases.</p>
                    </div>
                  ))}

                </div>
              )}
            </div>
          </motion.div>
        </>
      )}
    </AnimatePresence>
  );
};
