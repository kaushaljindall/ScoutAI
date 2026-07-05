
import { motion } from 'framer-motion';
import { Play, Sparkles, ChevronRight, BarChart3, Users, MessageSquare, ArrowUpRight } from 'lucide-react';

const DashboardPreview = () => {
  return (
    <div className="relative w-full aspect-[4/3] max-w-2xl mx-auto xl:mr-0 xl:ml-auto rounded-2xl glass-panel overflow-hidden shadow-2xl border-border/50 ring-1 ring-white/10 flex flex-col">
      {/* Header */}
      <div className="h-12 border-b border-border flex items-center px-4 justify-between bg-surface/30">
        <div className="flex gap-2">
          <div className="w-3 h-3 rounded-full bg-border"></div>
          <div className="w-3 h-3 rounded-full bg-border"></div>
          <div className="w-3 h-3 rounded-full bg-border"></div>
        </div>
        <div className="flex items-center gap-2 px-3 py-1 bg-background/50 rounded-md border border-border/50 text-xs text-primary/60">
          <Sparkles size={12} className="text-accent" />
          <span>AI Analyzing 124 leads</span>
        </div>
      </div>

      {/* Main Content */}
      <div className="flex-1 flex p-4 gap-4 bg-background/20">
        {/* Sidebar */}
        <div className="w-48 hidden sm:flex flex-col gap-2">
          <div className="px-3 py-2 rounded-md bg-accent/10 text-accent text-sm font-medium flex items-center gap-2">
            <Users size={16} /> Prospects
          </div>
          <div className="px-3 py-2 rounded-md text-primary/60 hover:bg-surface/50 text-sm font-medium flex items-center gap-2 transition-colors">
            <MessageSquare size={16} /> Outreach
          </div>
          <div className="px-3 py-2 rounded-md text-primary/60 hover:bg-surface/50 text-sm font-medium flex items-center gap-2 transition-colors">
            <BarChart3 size={16} /> Analytics
          </div>
          
          <div className="mt-auto glass-card p-3">
            <p className="text-xs text-primary/60 mb-2">Follow up required</p>
            <div className="flex items-center justify-between">
              <span className="text-sm font-semibold">Acme Corp</span>
              <span className="w-2 h-2 rounded-full bg-accent"></span>
            </div>
            <button className="mt-2 w-full text-[10px] bg-primary text-background py-1.5 rounded font-medium">Generate Reply</button>
          </div>
        </div>

        {/* Content Area */}
        <div className="flex-1 flex flex-col gap-4">
          {/* Top Widgets */}
          <div className="grid grid-cols-2 gap-4">
            <div className="glass-card p-3 flex flex-col gap-1">
              <span className="text-xs text-primary/60">Conversion Rate</span>
              <div className="flex items-end justify-between">
                <span className="text-xl font-semibold">12.4%</span>
                <span className="text-[10px] text-success flex items-center"><ArrowUpRight size={10} /> 2.1%</span>
              </div>
            </div>
            <div className="glass-card p-3 flex flex-col gap-1 relative overflow-hidden">
              <div className="absolute top-0 right-0 p-2 opacity-20"><Sparkles size={24} className="text-accent" /></div>
              <span className="text-xs text-primary/60">Avg AI Score</span>
              <div className="flex items-end justify-between">
                <span className="text-xl font-semibold text-gradient-accent">94/100</span>
                <span className="text-[10px] text-primary/40">Top tier</span>
              </div>
            </div>
          </div>

          {/* Table */}
          <div className="glass-card flex-1 p-0 overflow-hidden flex flex-col">
            <div className="px-4 py-3 border-b border-border/50 text-xs font-medium text-primary/60 grid grid-cols-12 gap-2">
              <div className="col-span-5">Company</div>
              <div className="col-span-3">Status</div>
              <div className="col-span-4">AI Score</div>
            </div>
            
            {[
              { name: 'Vercel', status: 'In Talks', score: 98, color: 'text-success', bg: 'bg-success/10' },
              { name: 'Stripe', status: 'Sent', score: 92, color: 'text-accent', bg: 'bg-accent/10' },
              { name: 'Linear', status: 'Drafting', score: 87, color: 'text-primary/60', bg: 'bg-surface' },
            ].map((row, i) => (
              <div key={i} className="px-4 py-3 border-b border-border/50 text-sm grid grid-cols-12 gap-2 items-center hover:bg-surface/30 transition-colors">
                <div className="col-span-5 font-medium">{row.name}</div>
                <div className="col-span-3">
                  <span className={`text-[10px] px-2 py-1 rounded-full ${row.bg} ${row.color}`}>{row.status}</span>
                </div>
                <div className="col-span-4 flex items-center gap-2">
                  <div className="h-1.5 w-full bg-surface rounded-full overflow-hidden">
                    <div className="h-full bg-gradient-to-r from-accent to-accent-secondary" style={{ width: `${row.score}%` }}></div>
                  </div>
                  <span className="text-xs text-primary/60 font-mono">{row.score}</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
      
      {/* Decorative gradients */}
      <div className="absolute top-0 right-0 -mr-20 -mt-20 w-64 h-64 bg-accent/20 rounded-full blur-[80px] pointer-events-none"></div>
      <div className="absolute bottom-0 left-0 -ml-20 -mb-20 w-64 h-64 bg-accent-secondary/10 rounded-full blur-[80px] pointer-events-none"></div>
    </div>
  );
};

const Hero = () => {
  return (
    <section className="relative pt-32 pb-20 md:pt-48 md:pb-32 overflow-hidden">
      <div className="max-w-7xl mx-auto px-6 md:px-12">
        <div className="flex flex-col xl:flex-row items-center gap-16">
          
          {/* Left Text */}
          <motion.div 
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, ease: "easeOut" }}
            className="flex-1 text-center xl:text-left max-w-2xl xl:max-w-none mx-auto"
          >
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full border border-border bg-surface/30 backdrop-blur-sm text-sm text-primary/80 mb-8 shadow-sm">
              <Sparkles size={14} className="text-accent" />
              <span>ScoutAI 2.0 is now live</span>
              <span className="w-px h-3 bg-border mx-1"></span>
              <a href="#" className="flex items-center hover:text-primary transition-colors font-medium">
                Read announcement <ChevronRight size={14} className="ml-0.5" />
              </a>
            </div>
            
            <h1 className="text-5xl md:text-7xl font-bold tracking-tight mb-6 leading-[1.1]">
              Discover Prospects.<br />
              <span className="text-gradient-accent">Automate Outreach.</span>
            </h1>
            
            <p className="text-lg md:text-xl text-primary/60 mb-10 max-w-lg mx-auto xl:mx-0 leading-relaxed">
              The AI-powered workspace that helps you find ideal clients, analyze their needs, and generate highly personalized campaigns that actually convert.
            </p>
            
            <div className="flex flex-col sm:flex-row items-center gap-4 justify-center xl:justify-start">
              <button className="w-full sm:w-auto px-8 py-4 bg-primary text-background hover:bg-primary/90 font-medium rounded-xl transition-all transform hover:scale-[1.02] active:scale-[0.98] shadow-[0_0_20px_rgba(255,255,255,0.1)]">
                Start Scouting
              </button>
              <button className="w-full sm:w-auto px-8 py-4 bg-surface hover:bg-surface-hover border border-border text-primary font-medium rounded-xl transition-all flex items-center justify-center gap-2 group">
                <Play size={18} className="text-primary/70 group-hover:text-primary transition-colors" />
                Watch Demo
              </button>
            </div>
            
            <p className="text-sm text-primary/40 mt-6">
              No credit card required. Free 14-day trial.
            </p>
          </motion.div>

          {/* Right Dashboard */}
          <motion.div 
            initial={{ opacity: 0, scale: 0.9, x: 20 }}
            animate={{ opacity: 1, scale: 1, x: 0 }}
            transition={{ duration: 1, delay: 0.2, ease: [0.16, 1, 0.3, 1] }}
            className="flex-1 w-full relative"
          >
            <DashboardPreview />
          </motion.div>
          
        </div>
      </div>
      
      {/* Background gradients */}
      <div className="absolute top-[-10%] left-[-10%] w-[40%] h-[40%] bg-accent/10 rounded-full blur-[120px] pointer-events-none -z-10"></div>
      <div className="absolute bottom-[-10%] right-[-10%] w-[30%] h-[40%] bg-accent-secondary/10 rounded-full blur-[120px] pointer-events-none -z-10"></div>
      
      {/* Grid Pattern */}
      <div className="absolute inset-0 bg-[url('data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNDAiIGhlaWdodD0iNDAiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+PGRlZnM+PHBhdHRlcm4gaWQ9ImdyaWQiIHdpZHRoPSI0MCIgaGVpZ2h0PSI0MCIgcGF0dGVyblVuaXRzPSJ1c2VyU3BhY2VPblVzZSI+PHBhdHRoIGQ9Ik0gNDAgMCBMIDAgMCAwIDQwIiBmaWxsPSJub25lIiBzdHJva2U9InJnYmEoMjU1LDI1NSwyNTUsMC4wMykiIHN0cm9rZS13aWR0aD0iMSIvPjwvcGF0dGVybj48L2RlZnM+PHJlY3Qgd2lkdGg9IjEwMCUiIGhlaWdodD0iMTAwJSIgZmlsbD0idXJsKCNncmlkKSIvPjwvc3ZnPg==')] opacity-[0.5] [mask-image:linear-gradient(to_bottom,white,transparent)] -z-10"></div>
    </section>
  );
};

export default Hero;
