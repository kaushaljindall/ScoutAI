
import { motion } from 'framer-motion';
import { Check } from 'lucide-react';

const plans = [
  {
    name: 'Starter',
    price: '$0',
    description: 'Perfect for trying out ScoutAI.',
    features: ['10 AI credits per month', 'Basic website scanning', 'Standard templates', 'Community support'],
    cta: 'Start for free',
    highlight: false
  },
  {
    name: 'Pro',
    price: '$49',
    period: '/mo',
    description: 'Everything you need to scale your outreach.',
    features: ['1000 AI credits per month', 'Deep website analysis', 'Custom AI models', 'CRM Integration', 'Priority support'],
    cta: 'Get Pro',
    highlight: true
  },
  {
    name: 'Team',
    price: '$99',
    period: '/mo/user',
    description: 'For agencies and scaling teams.',
    features: ['Unlimited AI credits', 'Advanced webhooks', 'Team collaboration', 'Custom workflows', 'Dedicated success manager'],
    cta: 'Contact Sales',
    highlight: false
  }
];

const Pricing = () => {
  return (
    <section id="pricing" className="py-24 bg-background border-t border-border/50">
      <div className="max-w-7xl mx-auto px-6 md:px-12">
        <div className="text-center mb-16">
          <h2 className="text-3xl md:text-4xl font-bold tracking-tight mb-4">Simple, transparent pricing.</h2>
          <p className="text-lg text-primary/60">No hidden fees. Cancel anytime.</p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-5xl mx-auto">
          {plans.map((plan, i) => (
            <motion.div
              key={i}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.5, delay: i * 0.1 }}
              className={`p-8 rounded-2xl border transition-all duration-300 flex flex-col ${
                plan.highlight 
                  ? 'bg-surface/50 border-accent/50 shadow-[0_0_30px_rgba(59,130,246,0.1)]' 
                  : 'bg-transparent border-border hover:border-primary/20'
              }`}
            >
              <div className="mb-6">
                <h3 className="text-xl font-medium mb-2">{plan.name}</h3>
                <div className="flex items-baseline gap-1 mb-2">
                  <span className="text-4xl font-bold">{plan.price}</span>
                  {plan.period && <span className="text-primary/50 text-sm">{plan.period}</span>}
                </div>
                <p className="text-sm text-primary/60">{plan.description}</p>
              </div>

              <div className="flex-1">
                <ul className="flex flex-col gap-4 mb-8">
                  {plan.features.map((feature, j) => (
                    <li key={j} className="flex items-start gap-3 text-sm">
                      <div className="mt-0.5 w-4 h-4 rounded-full bg-accent/10 flex items-center justify-center shrink-0">
                        <Check size={10} className="text-accent" />
                      </div>
                      <span className="text-primary/80">{feature}</span>
                    </li>
                  ))}
                </ul>
              </div>

              <button className={`w-full py-3 rounded-xl text-sm font-medium transition-all ${
                plan.highlight
                  ? 'bg-primary text-background hover:bg-primary/90'
                  : 'bg-surface hover:bg-surface-hover border border-border text-primary'
              }`}>
                {plan.cta}
              </button>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default Pricing;
