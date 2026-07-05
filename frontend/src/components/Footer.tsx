
import { Radar, Command, Layout, Link } from 'lucide-react';

const Footer = () => {
  return (
    <footer className="border-t border-border bg-background pt-16 pb-8">
      <div className="max-w-7xl mx-auto px-6 md:px-12">
        <div className="flex flex-col md:flex-row justify-between items-start gap-12 mb-16">
          <div className="max-w-xs">
            <div className="flex items-center gap-2 mb-4">
              <div className="w-6 h-6 rounded flex items-center justify-center text-accent">
                <Radar size={20} strokeWidth={2.5} />
              </div>
              <span className="font-semibold tracking-tight">ScoutAI</span>
            </div>
            <p className="text-sm text-primary/50">
              The AI-powered workspace for modern freelancers and agencies.
            </p>
          </div>
          
          <div className="flex gap-16">
            <div>
              <h4 className="font-medium mb-4 text-sm">Product</h4>
              <ul className="flex flex-col gap-3 text-sm text-primary/60">
                <li><a href="#" className="hover:text-primary transition-colors">Features</a></li>
                <li><a href="#" className="hover:text-primary transition-colors">Pricing</a></li>
                <li><a href="#" className="hover:text-primary transition-colors">Changelog</a></li>
                <li><a href="#" className="hover:text-primary transition-colors">Docs</a></li>
              </ul>
            </div>
            <div>
              <h4 className="font-medium mb-4 text-sm">Company</h4>
              <ul className="flex flex-col gap-3 text-sm text-primary/60">
                <li><a href="#" className="hover:text-primary transition-colors">About</a></li>
                <li><a href="#" className="hover:text-primary transition-colors">Blog</a></li>
                <li><a href="#" className="hover:text-primary transition-colors">Careers</a></li>
                <li><a href="#" className="hover:text-primary transition-colors">Contact</a></li>
              </ul>
            </div>
            <div>
              <h4 className="font-medium mb-4 text-sm">Legal</h4>
              <ul className="flex flex-col gap-3 text-sm text-primary/60">
                <li><a href="#" className="hover:text-primary transition-colors">Privacy</a></li>
                <li><a href="#" className="hover:text-primary transition-colors">Terms</a></li>
                <li><a href="#" className="hover:text-primary transition-colors">Security</a></li>
              </ul>
            </div>
          </div>
        </div>
        
        <div className="flex flex-col md:flex-row items-center justify-between pt-8 border-t border-border/50 text-sm text-primary/40">
          <p>© {new Date().getFullYear()} ScoutAI Inc. All rights reserved.</p>
          
          <div className="flex items-center gap-4 mt-4 md:mt-0">
            <a href="#" className="hover:text-primary transition-colors"><Command size={16} /></a>
            <a href="#" className="hover:text-primary transition-colors"><Layout size={16} /></a>
            <a href="#" className="hover:text-primary transition-colors"><Link size={16} /></a>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
