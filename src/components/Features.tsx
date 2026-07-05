
import { motion } from 'framer-motion';
import { Target, Globe, PenTool } from 'lucide-react';

const features = [
  {
    id: 'lead-discovery',
    label: 'AI Lead Discovery',
    title: 'Find prospects that match your exact criteria.',
    description: 'Stop manually searching for clients. Our AI scans millions of businesses and surfaces the ones that perfectly match your ideal customer profile.',
    icon: Target,
    preview: (
      <div className="w-full h-full glass-card p-6 flex flex-col gap-4">
        <div className="flex items-center gap-3 mb-2">
          <div className="flex-1 h-8 bg-surface rounded-md border border-border flex items-center px-3">
            <span className="text-xs text-primary/40">"SaaS companies in NY using React"</span>
          </div>
          <button className="h-8 px-4 bg-accent text-white rounded-md text-xs font-medium">Search</button>
        </div>
        <div className="flex-1 flex flex-col gap-2">
          {[1, 2, 3].map((i) => (
            <div key={i} className="bg-background/50 border border-border/50 rounded-lg p-3 flex justify-between items-center">
              <div className="flex flex-col gap-1">
                <div className="h-3 w-24 bg-primary/20 rounded"></div>
                <div className="h-2 w-16 bg-primary/10 rounded"></div>
              </div>
              <div className="h-6 w-16 bg-accent/20 rounded-full flex items-center justify-center">
                <span className="text-[10px] text-accent font-medium">9{8-i}% Match</span>
              </div>
            </div>
          ))}
        </div>
      </div>
    )
  },
  {
    id: 'website-analysis',
    label: 'Website Analysis',
    title: 'Understand their business before you even say hello.',
    description: 'We automatically scrape and analyze your prospect\'s website, pulling out key pain points, technologies used, and recent news to give you the perfect angle.',
    icon: Globe,
    preview: (
      <div className="w-full h-full glass-card overflow-hidden flex flex-col">
        <div className="h-10 border-b border-border bg-surface/30 flex items-center px-4 gap-2">
          <Globe size={14} className="text-primary/40" />
          <span className="text-xs text-primary/60 font-mono">acme-corp.com/about</span>
        </div>
        <div className="p-5 flex-1 flex flex-col gap-4">
          <div className="flex gap-2">
            <span className="px-2 py-1 bg-surface border border-border rounded text-[10px] text-primary/70">Next.js</span>
            <span className="px-2 py-1 bg-surface border border-border rounded text-[10px] text-primary/70">Stripe</span>
          </div>
          <div className="bg-accent/10 border border-accent/20 rounded-lg p-3 flex gap-3 items-start">
            <div className="mt-0.5"><SparklesIcon /></div>
            <div>
              <p className="text-xs text-accent font-medium mb-1">AI Insight</p>
              <p className="text-[11px] text-primary/70 leading-relaxed">Their current site has significant CLS issues on mobile. Good angle for a performance optimization pitch.</p>
            </div>
          </div>
        </div>
      </div>
    )
  },
  {
    id: 'personalized-outreach',
    label: 'Personalized Outreach',
    title: 'Messages that read like you spent hours writing them.',
    description: 'Generate hyper-personalized emails and LinkedIn messages based on the AI\'s analysis of their company, role, and recent achievements.',
    icon: PenTool,
    preview: (
      <div className="w-full h-full glass-card p-5 flex flex-col gap-3">
        <div className="flex justify-between items-center border-b border-border pb-2">
          <span className="text-xs font-medium text-primary/60">New Message</span>
          <div className="flex gap-1">
            <div className="w-2 h-2 rounded-full bg-border"></div>
            <div className="w-2 h-2 rounded-full bg-border"></div>
          </div>
        </div>
        <div className="text-[11px] text-primary/50">To: <span className="text-primary/90">sarah@acme.com</span></div>
        <div className="text-[11px] text-primary/50">Subject: <span className="text-primary/90">Quick question about your React rewrite</span></div>
        <div className="flex-1 bg-surface/30 rounded border border-border/50 p-3 mt-1">
          <p className="text-[11px] text-primary/80 leading-relaxed font-mono">
            Hi Sarah,<br/><br/>
            Noticed Acme just migrated to Next.js - love the new speed! 
            However, I saw your mobile navigation still has some CLS issues.<br/><br/>
            I help SaaS companies fix exactly these edge cases...
          </p>
        </div>
        <div className="flex justify-end mt-2">
          <button className="bg-primary text-background px-3 py-1.5 rounded-md text-[10px] font-medium">Send Sequence</button>
        </div>
      </div>
    )
  }
];

function SparklesIcon() {
  return (
    <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="text-accent"><path d="m12 3-1.912 5.813a2 2 0 0 1-1.275 1.275L3 12l5.813 1.912a2 2 0 0 1 1.275 1.275L12 21l1.912-5.813a2 2 0 0 1 1.275-1.275L21 12l-5.813-1.912a2 2 0 0 1-1.275-1.275L12 3Z"/></svg>
  );
}

const Features = () => {
  return (
    <section id="features" className="py-24 relative overflow-hidden bg-background">
      <div className="max-w-7xl mx-auto px-6 md:px-12">
        <div className="text-center max-w-2xl mx-auto mb-20">
          <h2 className="text-3xl md:text-5xl font-bold tracking-tight mb-4">Everything you need to close.</h2>
          <p className="text-lg text-primary/60">A complete toolset designed to give you an unfair advantage in client acquisition.</p>
        </div>

        <div className="flex flex-col gap-24 md:gap-32">
          {features.map((feature, index) => {
            const isEven = index % 2 === 0;
            const Icon = feature.icon;
            
            return (
              <div key={feature.id} className={`flex flex-col gap-12 md:gap-20 items-center ${isEven ? 'md:flex-row' : 'md:flex-row-reverse'}`}>
                {/* Text Content */}
                <div className="flex-1 w-full">
                  <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    whileInView={{ opacity: 1, y: 0 }}
                    viewport={{ once: true, margin: "-100px" }}
                    transition={{ duration: 0.6 }}
                  >
                    <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-lg bg-surface border border-border mb-6">
                      <Icon size={16} className="text-accent" />
                      <span className="text-sm font-medium">{feature.label}</span>
                    </div>
                    <h3 className="text-3xl md:text-4xl font-bold tracking-tight mb-4 leading-tight">{feature.title}</h3>
                    <p className="text-lg text-primary/60 leading-relaxed">{feature.description}</p>
                  </motion.div>
                </div>
                
                {/* UI Preview */}
                <div className="flex-1 w-full">
                  <motion.div
                    initial={{ opacity: 0, scale: 0.95 }}
                    whileInView={{ opacity: 1, scale: 1 }}
                    viewport={{ once: true, margin: "-100px" }}
                    transition={{ duration: 0.8, delay: 0.2 }}
                    className="relative aspect-square md:aspect-[4/3] rounded-2xl p-1 bg-gradient-to-b from-border to-transparent"
                  >
                    <div className="absolute inset-0 bg-accent/5 blur-3xl -z-10 rounded-full"></div>
                    {feature.preview}
                  </motion.div>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </section>
  );
};

export default Features;
