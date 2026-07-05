import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { ChevronDown } from 'lucide-react';

const faqs = [
  {
    question: "How does the AI personalization actually work?",
    answer: "ScoutAI uses a combination of web scraping and LLMs. When you input a company, we scrape their public website, recent news, and LinkedIn profiles. Our AI then synthesizes this data to identify pain points and matches them against your service offerings to craft a highly relevant message."
  },
  {
    question: "Does it integrate with my current CRM?",
    answer: "Yes, ScoutAI offers native integrations with Hubspot, Salesforce, and Pipedrive. For everything else, you can use our webhooks or Zapier integration to push prospects and conversations wherever you need them."
  },
  {
    question: "Is it safe to use with my LinkedIn account?",
    answer: "We don't automate actions on your LinkedIn account directly to comply with their Terms of Service. Instead, ScoutAI generates the perfect message and provides a 1-click 'Open in LinkedIn' button that pre-fills your clipboard."
  },
  {
    question: "What counts as an 'AI credit'?",
    answer: "One AI credit is used when you perform a deep website analysis or generate a personalized outreach message. Basic searches and CRM tracking do not consume credits."
  }
];

const FAQ = () => {
  const [openIndex, setOpenIndex] = useState<number | null>(0);

  return (
    <section id="faq" className="py-24 bg-background">
      <div className="max-w-3xl mx-auto px-6 md:px-12">
        <div className="text-center mb-16">
          <h2 className="text-3xl font-bold tracking-tight mb-4">Frequently Asked Questions</h2>
        </div>

        <div className="flex flex-col gap-4">
          {faqs.map((faq, index) => (
            <div 
              key={index} 
              className="border border-border rounded-xl bg-surface/30 overflow-hidden transition-colors hover:border-border/80"
            >
              <button 
                className="w-full text-left px-6 py-5 flex items-center justify-between focus:outline-none"
                onClick={() => setOpenIndex(openIndex === index ? null : index)}
              >
                <span className="font-medium pr-8">{faq.question}</span>
                <ChevronDown 
                  size={20} 
                  className={`text-primary/50 transition-transform duration-300 shrink-0 ${openIndex === index ? 'rotate-180' : ''}`} 
                />
              </button>
              
              <AnimatePresence>
                {openIndex === index && (
                  <motion.div
                    initial={{ height: 0, opacity: 0 }}
                    animate={{ height: 'auto', opacity: 1 }}
                    exit={{ height: 0, opacity: 0 }}
                    transition={{ duration: 0.3, ease: 'easeInOut' }}
                  >
                    <div className="px-6 pb-5 text-primary/60 text-sm leading-relaxed">
                      {faq.answer}
                    </div>
                  </motion.div>
                )}
              </AnimatePresence>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default FAQ;
