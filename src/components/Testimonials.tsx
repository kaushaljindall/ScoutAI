
import { motion } from 'framer-motion';
import { Quote } from 'lucide-react';

const testimonials = [
  {
    quote: "I used to spend 15 hours a week just researching prospects and drafting emails that felt 'good enough'. ScoutAI reduced that to maybe 2 hours, and my reply rate actually went up. The contextual analysis is eerily good.",
    author: "David Chen",
    role: "Founder, Polygon Digital",
    initials: "DC",
    color: "bg-blue-500/20 text-blue-400"
  },
  {
    quote: "Most AI tools generate obvious boilerplate. What impressed me about Scout is how it picks up on subtle technical details from a prospect's website and weaves them into the outreach naturally.",
    author: "Sarah Jenkins",
    role: "Head of Growth, StackFlow",
    initials: "SJ",
    color: "bg-emerald-500/20 text-emerald-400"
  },
  {
    quote: "We replaced our entire messy stack of generic scraping tools, CRM, and email sequencers with this. It just makes sense to have discovery, research, and outreach in a single, well-designed workflow.",
    author: "Marcus Aurelius",
    role: "Agency Owner, Rome Studio",
    initials: "MA",
    color: "bg-purple-500/20 text-purple-400"
  }
];

const Testimonials = () => {
  return (
    <section id="testimonials" className="py-24 relative bg-background overflow-hidden">
      <div className="absolute inset-0 bg-accent/5 [mask-image:radial-gradient(ellipse_at_center,white,transparent_70%)] -z-10"></div>
      
      <div className="max-w-7xl mx-auto px-6 md:px-12">
        <div className="text-center mb-16">
          <h2 className="text-3xl md:text-4xl font-bold tracking-tight mb-4">Don't just take our word for it.</h2>
          <p className="text-lg text-primary/60">Join hundreds of founders and freelancers closing better deals.</p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {testimonials.map((t, i) => (
            <motion.div
              key={i}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.6, delay: i * 0.1 }}
              className="glass-card p-8 flex flex-col relative group"
            >
              <Quote size={40} className="text-surface absolute top-6 right-6 -z-10 transition-transform group-hover:scale-110 duration-500" />
              <p className="text-primary/80 leading-relaxed mb-8 relative z-10">"{t.quote}"</p>
              
              <div className="mt-auto flex items-center gap-4">
                <div className={`w-10 h-10 rounded-full flex items-center justify-center font-medium text-sm ${t.color}`}>
                  {t.initials}
                </div>
                <div>
                  <h4 className="font-medium text-sm">{t.author}</h4>
                  <p className="text-xs text-primary/50">{t.role}</p>
                </div>
              </div>
            </motion.div>
          ))}
        </div>
        
        {/* Trusted By Logos */}
        <div className="mt-24 border-t border-border/50 pt-12">
          <p className="text-center text-sm text-primary/40 font-medium mb-8">TRUSTED BY TEAMS AT</p>
          <div className="flex flex-wrap justify-center items-center gap-8 md:gap-16 opacity-50 grayscale hover:grayscale-0 transition-all duration-500">
            {/* Using text representations instead of images for clean look */}
            <span className="text-xl font-bold tracking-tighter">LINEAR</span>
            <span className="text-xl font-bold tracking-tight">Vercel</span>
            <span className="text-xl font-semibold tracking-wide">stripe</span>
            <span className="text-xl font-bold">Raycast</span>
            <span className="text-xl font-bold tracking-tight">RESEND</span>
          </div>
        </div>
      </div>
    </section>
  );
};

export default Testimonials;
