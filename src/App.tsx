
import Navbar from './components/Navbar';
import Hero from './components/Hero';
import Features from './components/Features';
import Workflow from './components/Workflow';
import BentoGrid from './components/BentoGrid';
import Testimonials from './components/Testimonials';
import Pricing from './components/Pricing';
import FAQ from './components/FAQ';
import Footer from './components/Footer';
import CTASection from './components/CTASection';

function App() {
  return (
    <div className="min-h-screen bg-background font-sans selection:bg-accent/30 selection:text-primary">
      <Navbar />
      <main>
        <Hero />
        <Features />
        <Workflow />
        <BentoGrid />
        <Testimonials />
        <Pricing />
        <FAQ />
        <CTASection />
      </main>
      <Footer />
    </div>
  );
}

export default App;
