
import { motion } from 'framer-motion';

const CTASection = () => {
  return (
    <section className="py-32 relative overflow-hidden bg-background">
      {/* Decorative Background */}
      <div className="absolute inset-0 flex items-center justify-center pointer-events-none">
        <div className="w-[800px] h-[800px] bg-accent/5 rounded-full blur-[100px]"></div>
      </div>
      
      <div className="max-w-4xl mx-auto px-6 md:px-12 relative z-10 text-center">
        <motion.div
          initial={{ opacity: 0, scale: 0.95 }}
          whileInView={{ opacity: 1, scale: 1 }}
          viewport={{ once: true }}
          transition={{ duration: 0.8 }}
        >
          <h2 className="text-4xl md:text-6xl font-bold tracking-tight mb-8">
            Ready to fill your pipeline?
          </h2>
          <p className="text-xl text-primary/60 mb-12 max-w-2xl mx-auto">
            Stop searching and start closing. Join the next generation of freelancers and agencies.
          </p>
          
          <button className="px-10 py-5 bg-primary text-background hover:bg-primary/90 font-medium rounded-xl text-lg transition-all transform hover:scale-[1.02] active:scale-[0.98] shadow-[0_0_30px_rgba(255,255,255,0.15)]">
            Start Your Free Trial
          </button>
        </motion.div>
      </div>
    </section>
  );
};

export default CTASection;
