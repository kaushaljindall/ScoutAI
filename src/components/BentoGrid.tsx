
import { motion } from 'framer-motion';
import { Filter, Search, Sparkles, LayoutDashboard, FileText, BarChart, StickyNote, Copy } from 'lucide-react';

const bentoItems = [
  { title: 'Smart Filters', colSpan: 'col-span-12 md:col-span-4', icon: Filter, desc: 'Filter by tech stack, funding, and revenue.' },
  { title: 'Website Scanner', colSpan: 'col-span-12 md:col-span-8', icon: Search, desc: 'Instantly extract pain points and key information from any URL.' },
  { title: 'AI Message Writer', colSpan: 'col-span-12 md:col-span-8', icon: Sparkles, desc: 'Generate hyper-personalized emails that get replies.' },
  { title: 'CRM', colSpan: 'col-span-12 md:col-span-4', icon: LayoutDashboard, desc: 'Track deals effortlessly.' },
  { title: 'Proposal Generator', colSpan: 'col-span-12 md:col-span-4', icon: FileText, desc: 'Create beautiful proposals in seconds.' },
  { title: 'Analytics', colSpan: 'col-span-12 md:col-span-4', icon: BarChart, desc: 'Measure what matters most.' },
  { title: 'Notes', colSpan: 'col-span-12 md:col-span-2', icon: StickyNote, desc: 'Capture thoughts.' },
  { title: 'Templates', colSpan: 'col-span-12 md:col-span-2', icon: Copy, desc: 'Save your best.' }
];

const BentoGrid = () => {
  return (
    <section className="py-24 relative bg-background">
      <div className="max-w-7xl mx-auto px-6 md:px-12">
        <div className="mb-16">
          <h2 className="text-3xl md:text-4xl font-bold tracking-tight mb-4">A complete ecosystem.</h2>
          <p className="text-lg text-primary/60 max-w-2xl">Everything you need to run your freelance business or agency, beautifully designed and integrated.</p>
        </div>

        <div className="grid grid-cols-12 gap-4 auto-rows-[160px]">
          {bentoItems.map((item, i) => {
            const Icon = item.icon;
            return (
              <motion.div
                key={i}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ duration: 0.5, delay: i * 0.05 }}
                className={`glass-card p-6 flex flex-col justify-between group overflow-hidden relative ${item.colSpan}`}
              >
                <div className="absolute top-0 right-0 p-8 opacity-0 group-hover:opacity-10 transition-opacity duration-500 transform translate-x-4 -translate-y-4 group-hover:translate-x-0 group-hover:translate-y-0">
                  <Icon size={100} />
                </div>
                <div className="w-10 h-10 rounded-lg bg-surface flex items-center justify-center border border-border group-hover:border-accent/50 group-hover:text-accent transition-colors z-10">
                  <Icon size={20} />
                </div>
                <div className="z-10 mt-4">
                  <h3 className="font-semibold text-lg mb-1">{item.title}</h3>
                  <p className="text-sm text-primary/50 group-hover:text-primary/70 transition-colors line-clamp-2">{item.desc}</p>
                </div>
              </motion.div>
            );
          })}
        </div>
      </div>
    </section>
  );
};

export default BentoGrid;
