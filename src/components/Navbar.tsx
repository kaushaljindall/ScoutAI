import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Radar } from 'lucide-react';

const Navbar = () => {
  const [scrolled, setScrolled] = useState(false);

  useEffect(() => {
    const handleScroll = () => {
      setScrolled(window.scrollY > 20);
    };
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  const navLinks = ['Features', 'How it Works', 'Pricing', 'Testimonials', 'FAQ'];

  return (
    <motion.header
      initial={{ y: -100, opacity: 0 }}
      animate={{ y: 0, opacity: 1 }}
      transition={{ duration: 0.5, ease: 'easeOut' }}
      className={`fixed top-0 left-0 right-0 z-50 transition-all duration-300 border-b ${
        scrolled 
          ? 'bg-background/70 backdrop-blur-md border-border py-4 shadow-[0_4px_30px_rgba(0,0,0,0.1)]' 
          : 'bg-transparent border-transparent py-6'
      }`}
    >
      <div className="max-w-7xl mx-auto px-6 md:px-12 flex items-center justify-between">
        {/* Logo */}
        <div className="flex items-center gap-2 group cursor-pointer">
          <div className="w-8 h-8 rounded-lg bg-accent/10 border border-accent/20 flex items-center justify-center text-accent group-hover:bg-accent group-hover:text-primary transition-colors duration-300">
            <Radar size={18} strokeWidth={2.5} />
          </div>
          <span className="font-semibold text-lg tracking-tight">ScoutAI</span>
        </div>

        {/* Center Links */}
        <nav className="hidden md:flex items-center gap-8">
          {navLinks.map((link) => (
            <a 
              key={link} 
              href={`#${link.toLowerCase().replace(/\s+/g, '-')}`}
              className="text-sm font-medium text-primary/70 hover:text-primary transition-colors"
            >
              {link}
            </a>
          ))}
        </nav>

        {/* Right CTA */}
        <div className="flex items-center gap-4">
          <button className="text-sm font-medium text-primary/80 hover:text-primary transition-colors hidden sm:block">
            Sign In
          </button>
          <button className="bg-primary text-background hover:bg-primary/90 px-4 py-2 rounded-lg text-sm font-medium transition-all transform hover:scale-105 active:scale-95">
            Get Started
          </button>
        </div>
      </div>
    </motion.header>
  );
};

export default Navbar;
