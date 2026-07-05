import { useState } from 'react';
import { useGetDashboardMetrics, useGetInsights } from '@/hooks/useAnalytics';
import { TrendingUp, Users, Target, CheckCircle, AlertTriangle, Lightbulb, Banknote, LineChart, Sparkles } from 'lucide-react';
import { cn } from '@/utils/cn';

export default function AnalyticsPage() {
  const { data: metrics, isLoading: isMetricsLoading } = useGetDashboardMetrics();
  const { data: insights, isLoading: isInsightsLoading } = useGetInsights();
  
  const [timeRange, setTimeRange] = useState('30 Days');

  if (isMetricsLoading) {
    return <div className="h-full flex items-center justify-center">Loading Analytics...</div>;
  }

  return (
    <div className="h-full flex flex-col pt-2 pb-6 overflow-y-auto">
      <div className="mb-6 flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Analytics</h1>
          <p className="text-primary/60 mt-1">Track performance, revenue, and get AI insights.</p>
        </div>
        
        <div className="flex bg-surface/30 p-1 rounded-lg border border-border/50">
          {['Today', '7 Days', '30 Days', '90 Days'].map(range => (
             <button
               key={range}
               onClick={() => setTimeRange(range)}
               className={cn(
                 "px-4 py-1.5 rounded-md text-sm font-medium transition-colors",
                 timeRange === range 
                   ? "bg-background shadow-sm text-primary" 
                   : "text-primary/60 hover:text-primary"
               )}
             >
               {range}
             </button>
          ))}
        </div>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
        <div className="p-5 bg-background rounded-xl border border-border/50 shadow-sm relative overflow-hidden group">
          <div className="flex justify-between items-start">
            <div>
              <p className="text-primary/60 text-sm font-medium">Total Pipeline Leads</p>
              <h3 className="text-3xl font-bold mt-1">{metrics?.total_leads || 0}</h3>
            </div>
            <div className="p-3 bg-blue-500/10 text-blue-500 rounded-lg"><Users size={20} /></div>
          </div>
          <div className="mt-4 flex items-center text-xs">
            <TrendingUp size={14} className="text-emerald-500 mr-1" />
            <span className="text-emerald-500 font-medium">12%</span>
            <span className="text-primary/40 ml-1">vs last {timeRange.toLowerCase()}</span>
          </div>
        </div>

        <div className="p-5 bg-background rounded-xl border border-border/50 shadow-sm relative overflow-hidden">
          <div className="flex justify-between items-start">
            <div>
              <p className="text-primary/60 text-sm font-medium">Conversion Rate</p>
              <h3 className="text-3xl font-bold mt-1">{metrics?.conversion_rate || 0}%</h3>
            </div>
            <div className="p-3 bg-emerald-500/10 text-emerald-500 rounded-lg"><Target size={20} /></div>
          </div>
          <div className="mt-4 flex items-center text-xs">
            <TrendingUp size={14} className="text-emerald-500 mr-1" />
            <span className="text-emerald-500 font-medium">4.2%</span>
            <span className="text-primary/40 ml-1">vs last {timeRange.toLowerCase()}</span>
          </div>
        </div>

        <div className="p-5 bg-background rounded-xl border border-border/50 shadow-sm relative overflow-hidden">
          <div className="flex justify-between items-start">
            <div>
              <p className="text-primary/60 text-sm font-medium">Closed Revenue</p>
              <h3 className="text-3xl font-bold mt-1">${(metrics?.closed_revenue || 0).toLocaleString()}</h3>
            </div>
            <div className="p-3 bg-purple-500/10 text-purple-500 rounded-lg"><Banknote size={20} /></div>
          </div>
          <div className="w-full bg-surface h-1.5 rounded-full mt-4 overflow-hidden">
             <div className="bg-purple-500 h-full rounded-full" style={{ width: '65%' }}></div>
          </div>
        </div>

        <div className="p-5 bg-background rounded-xl border border-border/50 shadow-sm relative overflow-hidden">
          <div className="flex justify-between items-start">
            <div>
              <p className="text-primary/60 text-sm font-medium">Deals Won</p>
              <h3 className="text-3xl font-bold mt-1">{metrics?.deals_won || 0}</h3>
            </div>
            <div className="p-3 bg-amber-500/10 text-amber-500 rounded-lg"><CheckCircle size={20} /></div>
          </div>
          <p className="text-xs text-primary/40 mt-4">{metrics?.proposals_sent || 0} proposals pending review</p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Main Charts Area */}
        <div className="col-span-2 space-y-6">
          
          {/* Funnel Chart via CSS */}
          <div className="bg-background rounded-xl border border-border/50 p-6 shadow-sm">
             <div className="flex justify-between items-center mb-6">
               <h3 className="font-semibold flex items-center gap-2"><LineChart size={18} className="text-accent" /> Sales Funnel</h3>
             </div>
             
             <div className="space-y-4">
               {[
                 { label: 'Total Discovery', val: metrics?.total_leads || 0, max: metrics?.total_leads || 1 },
                 { label: 'Contacted', val: metrics?.contacted || 0, max: metrics?.total_leads || 1 },
                 { label: 'Replies', val: metrics?.replies || 0, max: metrics?.total_leads || 1 },
                 { label: 'Proposals', val: metrics?.proposals_sent || 0, max: metrics?.total_leads || 1 },
                 { label: 'Won Deals', val: metrics?.deals_won || 0, max: metrics?.total_leads || 1 },
               ].map((step, i) => (
                 <div key={i} className="flex items-center gap-4">
                   <span className="w-28 text-sm font-medium text-primary/70 text-right">{step.label}</span>
                   <div className="flex-1 h-8 bg-surface rounded-md overflow-hidden flex items-center">
                     <div 
                       className="h-full bg-accent transition-all duration-1000 ease-out flex items-center px-3"
                       style={{ width: `${Math.max(5, (step.val / step.max) * 100)}%` }}
                     >
                        <span className="text-xs text-background font-bold">{step.val}</span>
                     </div>
                   </div>
                 </div>
               ))}
             </div>
          </div>

        </div>

        {/* AI Insights Sidebar */}
        <div className="space-y-4">
           <div className="bg-accent/5 rounded-xl border border-accent/20 p-5 h-full">
             <h3 className="font-semibold text-accent flex items-center gap-2 mb-4">
               <Sparkles size={18} /> AI Business Insights
             </h3>
             
             {isInsightsLoading ? (
               <div className="space-y-4 animate-pulse">
                 <div className="h-24 bg-surface rounded-lg"></div>
                 <div className="h-24 bg-surface rounded-lg"></div>
               </div>
             ) : (
               <div className="space-y-4">
                 {insights?.map((insight, i) => (
                   <div key={i} className="bg-background p-4 rounded-lg border border-border/50 relative overflow-hidden">
                      <div className={cn("absolute top-0 left-0 w-1 h-full", 
                        insight.action_type === 'success' ? 'bg-emerald-500' : 
                        insight.action_type === 'warning' ? 'bg-amber-500' : 'bg-blue-500'
                      )}></div>
                      <div className="flex gap-3">
                        <div className="mt-1 shrink-0">
                           {insight.action_type === 'success' && <CheckCircle size={16} className="text-emerald-500" />}
                           {insight.action_type === 'warning' && <AlertTriangle size={16} className="text-amber-500" />}
                           {insight.action_type === 'info' && <Lightbulb size={16} className="text-blue-500" />}
                        </div>
                        <div>
                          <p className="text-sm font-medium leading-snug">{insight.insight}</p>
                          <p className="text-xs text-primary/60 mt-1.5">{insight.explanation}</p>
                        </div>
                      </div>
                   </div>
                 ))}
                 
                 {!insights && (
                   <div className="text-center p-6 border-2 border-dashed border-accent/20 rounded-lg">
                      <p className="text-sm text-accent/70">Connect your Gemini API to receive intelligent insights.</p>
                   </div>
                 )}
               </div>
             )}
           </div>
        </div>
      </div>
    </div>
  );
}
