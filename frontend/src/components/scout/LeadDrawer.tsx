import { useState } from 'react';
import { useScoutStore } from '@/store/scoutStore';
import { useGetBusiness } from '@/hooks/useScout';
import { X, ExternalLink, Mail, Phone, MapPin, Building, Star, Globe, Briefcase, MessageSquare } from 'lucide-react';
import { Button } from '@/components/ui/Button';
import { cn } from '@/utils/cn';
import { motion, AnimatePresence } from 'framer-motion';

export const LeadDrawer = () => {
  const { selectedLeadId, isDrawerOpen, setIsDrawerOpen, setSelectedLeadId } = useScoutStore();
  const { data: business, isLoading } = useGetBusiness(selectedLeadId);
  const [activeTab, setActiveTab] = useState('overview');

  const tabs = [
    { id: 'overview', label: 'Overview' },
    { id: 'contact', label: 'Contact' },
    { id: 'website', label: 'Website' },
    { id: 'social', label: 'Social' },
    { id: 'notes', label: 'Notes' },
    { id: 'history', label: 'History' },
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
                    "px-1 py-3 text-sm font-medium border-b-2 whitespace-nowrap mr-6 transition-colors",
                    activeTab === tab.id ? "border-primary text-primary" : "border-transparent text-primary/50 hover:text-primary/80"
                  )}
                >
                  {tab.label}
                </button>
              ))}
            </div>

            {/* Content Area */}
            <div className="flex-1 overflow-y-auto p-6 bg-surface/10">
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
                <div className="space-y-8">
                  {/* Overview Tab */}
                  <div className={cn("space-y-6", activeTab === 'overview' ? 'block' : 'hidden')}>
                    {/* Placeholder for AI Analysis */}
                    <div className="p-4 rounded-xl bg-accent/5 border border-accent/20 relative overflow-hidden">
                      <div className="absolute -right-4 -top-4 w-24 h-24 bg-accent/10 rounded-full blur-xl pointer-events-none" />
                      <h4 className="text-xs font-semibold text-accent uppercase tracking-wider mb-2 flex items-center gap-1.5">
                        <Star size={12} className="fill-accent text-accent" /> AI Overview
                      </h4>
                      <p className="text-sm text-primary/70 leading-relaxed font-mono">
                        Analysis pending... (This section will be powered by Scout Engine in Phase 3 to generate insights from website and social data).
                      </p>
                    </div>

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
