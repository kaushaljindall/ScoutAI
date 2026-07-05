import { motion } from 'framer-motion';
import { Search, Bell, Settings, Filter, ChevronDown, Activity, Users, DollarSign, ArrowUpRight, MessageSquare, Target, CheckCircle2 } from 'lucide-react';
import { cn } from '@/utils/cn';

const DashboardShowcase = () => {
  return (
    <section className="py-24 relative overflow-hidden bg-background">
      <div className="max-w-7xl mx-auto px-6 md:px-12">
        <div className="text-center max-w-2xl mx-auto mb-16">
          <h2 className="text-3xl md:text-5xl font-bold tracking-tight mb-4">Command center for your growth.</h2>
          <p className="text-lg text-primary/60">Manage leads, track conversations, and analyze your pipeline from a single, powerful interface.</p>
        </div>

        <motion.div 
          initial={{ opacity: 0, y: 40 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, margin: "-100px" }}
          transition={{ duration: 0.8, ease: "easeOut" }}
          className="relative rounded-2xl border border-border/50 bg-surface/30 backdrop-blur-sm overflow-hidden shadow-2xl ring-1 ring-white/5"
        >
          {/* Top Navigation */}
          <div className="h-14 border-b border-border/50 flex items-center justify-between px-4 bg-background/50">
            <div className="flex items-center gap-4 w-64">
              <div className="w-8 h-8 rounded bg-accent/10 border border-accent/20 flex items-center justify-center text-accent">
                <Target size={16} />
              </div>
              <span className="font-semibold text-sm">Workspace</span>
            </div>
            
            <div className="flex-1 max-w-xl hidden md:flex items-center">
              <div className="relative w-full">
                <Search size={14} className="absolute left-3 top-1/2 -translate-y-1/2 text-primary/40" />
                <input 
                  type="text" 
                  placeholder="Search leads, campaigns, or messages..." 
                  className="w-full h-9 bg-surface border border-border/50 rounded-lg pl-9 pr-4 text-sm focus:outline-none focus:border-accent/50"
                  readOnly
                />
              </div>
            </div>

            <div className="flex items-center gap-4 justify-end w-64">
              <div className="flex items-center gap-3 text-primary/60">
                <Bell size={16} className="cursor-pointer hover:text-primary transition-colors" />
                <Settings size={16} className="cursor-pointer hover:text-primary transition-colors" />
              </div>
              <div className="w-px h-4 bg-border/50"></div>
              <div className="w-7 h-7 rounded-full bg-surface border border-border flex items-center justify-center text-xs font-medium">
                JS
              </div>
            </div>
          </div>

          <div className="flex h-[600px] overflow-hidden bg-background/20">
            {/* Sidebar */}
            <div className="w-64 border-r border-border/50 hidden md:flex flex-col bg-background/30">
              <div className="p-4 flex flex-col gap-1">
                {['Dashboard', 'Leads', 'Campaigns', 'Messages', 'Analytics'].map((item, i) => (
                  <div key={item} className={cn(
                    "px-3 py-2 rounded-lg text-sm font-medium flex items-center justify-between cursor-pointer transition-colors",
                    i === 1 ? "bg-accent text-white" : "text-primary/60 hover:bg-surface hover:text-primary"
                  )}>
                    <span>{item}</span>
                    {i === 1 && <span className="text-[10px] bg-white/20 px-1.5 py-0.5 rounded">24</span>}
                  </div>
                ))}
              </div>
              
              <div className="mt-auto p-4 border-t border-border/50">
                <div className="p-3 rounded-lg bg-surface/50 border border-border/50">
                  <div className="flex items-center gap-2 mb-2">
                    <Activity size={14} className="text-accent" />
                    <span className="text-xs font-medium">System Status</span>
                  </div>
                  <div className="text-[10px] text-primary/50 flex justify-between">
                    <span>AI Engine</span>
                    <span className="text-emerald-500">Online</span>
                  </div>
                </div>
              </div>
            </div>

            {/* Main Content Area */}
            <div className="flex-1 flex flex-col min-w-0">
              {/* Header & Filters */}
              <div className="p-6 pb-4 flex items-center justify-between">
                <h1 className="text-2xl font-bold">Leads Pipeline</h1>
                <div className="flex gap-2">
                  <button className="h-9 px-3 text-sm bg-surface border border-border/50 rounded-lg flex items-center gap-2 hover:bg-surface-hover transition-colors">
                    <Filter size={14} /> Filters <ChevronDown size={14} />
                  </button>
                  <button className="h-9 px-4 text-sm bg-primary text-background rounded-lg font-medium hover:bg-primary/90 transition-colors">
                    Add Leads
                  </button>
                </div>
              </div>

              {/* Analytics Cards */}
              <div className="px-6 pb-6 grid grid-cols-1 md:grid-cols-3 gap-4">
                {[
                  { label: "Total Leads", value: "1,248", change: "+12%", icon: Users },
                  { label: "Conversion Rate", value: "14.2%", change: "+2.4%", icon: Activity },
                  { label: "Pipeline Value", value: "$42,500", change: "+18%", icon: DollarSign },
                ].map((stat, i) => (
                  <div key={i} className="p-4 rounded-xl bg-surface/40 border border-border/50 flex flex-col gap-3">
                    <div className="flex items-center justify-between text-primary/60">
                      <span className="text-sm font-medium">{stat.label}</span>
                      <stat.icon size={16} />
                    </div>
                    <div className="flex items-end justify-between">
                      <span className="text-2xl font-bold">{stat.value}</span>
                      <span className="text-xs text-emerald-500 flex items-center gap-0.5 font-medium">
                        <ArrowUpRight size={12} /> {stat.change}
                      </span>
                    </div>
                  </div>
                ))}
              </div>

              {/* Layout for Table & Timeline */}
              <div className="flex-1 flex px-6 pb-6 gap-6 min-h-0">
                {/* Table */}
                <div className="flex-[2] rounded-xl border border-border/50 bg-background/50 flex flex-col overflow-hidden">
                  <div className="grid grid-cols-12 gap-4 px-4 py-3 border-b border-border/50 text-xs font-medium text-primary/50 bg-surface/30">
                    <div className="col-span-4">COMPANY</div>
                    <div className="col-span-3">STATUS</div>
                    <div className="col-span-3">AI SCORE</div>
                    <div className="col-span-2 text-right">ACTIVITY</div>
                  </div>
                  <div className="flex-1 overflow-y-auto">
                    {[
                      { company: "Vercel", domain: "vercel.com", status: "In Discussion", statusColor: "text-blue-400 bg-blue-400/10 border-blue-400/20", score: 98, time: "2h ago" },
                      { company: "Stripe", domain: "stripe.com", status: "Outreach Sent", statusColor: "text-purple-400 bg-purple-400/10 border-purple-400/20", score: 92, time: "5h ago" },
                      { company: "Linear", domain: "linear.app", status: "Analyzing", statusColor: "text-emerald-400 bg-emerald-400/10 border-emerald-400/20", score: 87, time: "1d ago" },
                      { company: "Notion", domain: "notion.so", status: "New", statusColor: "text-primary/60 bg-surface border-border", score: 85, time: "2d ago" },
                    ].map((row, i) => (
                      <div key={i} className="grid grid-cols-12 gap-4 px-4 py-3 border-b border-border/20 text-sm items-center hover:bg-surface/30 transition-colors cursor-pointer group">
                        <div className="col-span-4 flex flex-col">
                          <span className="font-medium">{row.company}</span>
                          <span className="text-xs text-primary/40">{row.domain}</span>
                        </div>
                        <div className="col-span-3">
                          <span className={cn("text-[10px] px-2 py-1 rounded-full border font-medium", row.statusColor)}>
                            {row.status}
                          </span>
                        </div>
                        <div className="col-span-3 flex items-center gap-2">
                          <div className="h-1.5 w-full max-w-[60px] bg-surface rounded-full overflow-hidden">
                            <div className="h-full bg-accent" style={{ width: `${row.score}%` }}></div>
                          </div>
                          <span className="text-xs text-primary/60 font-mono">{row.score}</span>
                        </div>
                        <div className="col-span-2 text-right text-xs text-primary/40">
                          {row.time}
                        </div>
                      </div>
                    ))}
                  </div>
                </div>

                {/* AI Timeline Panel */}
                <div className="flex-1 rounded-xl border border-border/50 bg-surface/30 flex flex-col overflow-hidden relative">
                  <div className="absolute top-0 right-0 p-32 bg-accent/5 rounded-full blur-3xl -z-10 pointer-events-none"></div>
                  
                  <div className="p-4 border-b border-border/50 flex items-center justify-between bg-surface/50">
                    <span className="font-medium text-sm">Vercel - Timeline</span>
                    <div className="px-2 py-0.5 rounded text-[10px] font-medium bg-accent/20 text-accent border border-accent/30 flex items-center gap-1">
                      <Target size={10} /> Hot Lead
                    </div>
                  </div>
                  
                  <div className="flex-1 p-4 flex flex-col gap-4 overflow-y-auto">
                    <div className="flex gap-3">
                      <div className="mt-1"><CheckCircle2 size={14} className="text-emerald-500" /></div>
                      <div>
                        <p className="text-sm font-medium">Website Analyzed</p>
                        <p className="text-xs text-primary/50 mt-0.5">Found Next.js, identified performance optimization opportunities.</p>
                      </div>
                    </div>
                    
                    <div className="flex gap-3">
                      <div className="mt-1"><MessageSquare size={14} className="text-accent" /></div>
                      <div>
                        <p className="text-sm font-medium">AI Outreach Drafted</p>
                        <div className="mt-2 p-3 rounded-lg bg-background/50 border border-border/50 text-xs text-primary/70 leading-relaxed font-mono">
                          "Hi team, noticed you're pushing boundaries with Next.js. I help SaaS companies optimize their edge networks..."
                        </div>
                      </div>
                    </div>
                    
                    <div className="flex gap-3">
                      <div className="mt-1 w-3.5 h-3.5 rounded-full border-2 border-border/50 bg-background"></div>
                      <div>
                        <p className="text-sm font-medium text-primary/60">Follow up suggested</p>
                        <p className="text-xs text-primary/40 mt-0.5">Scheduled for Tomorrow, 9:00 AM</p>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </motion.div>
      </div>
      
      {/* Decorative gradients */}
      <div className="absolute bottom-0 left-1/2 -translate-x-1/2 w-[800px] h-[400px] bg-accent/10 rounded-full blur-[120px] pointer-events-none -z-10"></div>
    </section>
  );
};

export default DashboardShowcase;
