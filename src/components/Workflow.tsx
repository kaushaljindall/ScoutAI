
import { motion } from 'framer-motion';
import { Search, Globe2, MessageSquareText, Activity, CheckCircle2 } from 'lucide-react';

const steps = [
  { icon: Search, title: 'Find Businesses' },
  { icon: Globe2, title: 'Analyze Website' },
  { icon: MessageSquareText, title: 'Generate Outreach' },
  { icon: Activity, title: 'Track Conversations' },
  { icon: CheckCircle2, title: 'Win Clients', highlight: true }
];

const Workflow = () => {
  return (
    <section id="how-it-works" className="py-24 relative bg-background overflow-hidden border-y border-border/50">
      {/* Background gradients */}
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-full max-w-4xl h-[2px] bg-gradient-to-r from-transparent via-border to-transparent -z-10"></div>
      
      <div className="max-w-7xl mx-auto px-6 md:px-12">
        <div className="text-center max-w-2xl mx-auto mb-16">
          <h2 className="text-3xl md:text-5xl font-bold tracking-tight mb-4">Autopilot for your pipeline.</h2>
          <p className="text-lg text-primary/60">From discovery to signed contract, all in one continuous flow.</p>
        </div>

        <div className="relative">
          {/* Connector Line (Desktop) */}
          <div className="hidden md:block absolute top-1/2 left-[10%] right-[10%] h-[2px] bg-border -translate-y-1/2 z-0">
            <motion.div 
              className="h-full bg-gradient-to-r from-accent/0 via-accent to-accent-secondary/0"
              initial={{ width: "0%", left: "0%" }}
              whileInView={{ 
                width: ["0%", "100%", "0%"], 
                left: ["0%", "0%", "100%"] 
              }}
              transition={{ duration: 3, repeat: Infinity, ease: "easeInOut" }}
            />
          </div>

          {/* Connector Line (Mobile) */}
          <div className="md:hidden absolute left-1/2 top-[10%] bottom-[10%] w-[2px] bg-border -translate-x-1/2 z-0">
            <motion.div 
              className="w-full bg-gradient-to-b from-accent/0 via-accent to-accent-secondary/0"
              initial={{ height: "0%", top: "0%" }}
              whileInView={{ 
                height: ["0%", "100%", "0%"], 
                top: ["0%", "0%", "100%"] 
              }}
              transition={{ duration: 3, repeat: Infinity, ease: "easeInOut" }}
            />
          </div>

          <div className="flex flex-col md:flex-row justify-between items-center gap-12 md:gap-4 relative z-10">
            {steps.map((step, index) => {
              const Icon = step.icon;
              return (
                <motion.div 
                  key={index}
                  initial={{ opacity: 0, y: 20 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  viewport={{ once: true }}
                  transition={{ duration: 0.5, delay: index * 0.1 }}
                  className="flex flex-col items-center gap-4 group"
                >
                  <div className={`w-16 h-16 rounded-2xl flex items-center justify-center border transition-all duration-300 ${
                    step.highlight 
                      ? 'bg-accent/10 border-accent/50 text-accent group-hover:scale-110 shadow-[0_0_20px_rgba(59,130,246,0.2)]' 
                      : 'bg-surface border-border text-primary/60 group-hover:border-primary/30 group-hover:text-primary group-hover:scale-105'
                  }`}>
                    <Icon size={24} />
                  </div>
                  <span className={`text-sm font-medium text-center max-w-[120px] ${
                    step.highlight ? 'text-primary' : 'text-primary/70'
                  }`}>
                    {step.title}
                  </span>
                </motion.div>
              );
            })}
          </div>
        </div>
      </div>
    </section>
  );
};

export default Workflow;
