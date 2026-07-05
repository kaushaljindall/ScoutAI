
import Navbar from '@/components/Navbar';
import Hero from '@/components/Hero';
import TrustedBy from '@/components/TrustedBy';
import Features from '@/components/Features';
import Workflow from '@/components/Workflow';
import DashboardShowcase from '@/components/DashboardShowcase';
import BentoGrid from '@/components/BentoGrid';
import Testimonials from '@/components/Testimonials';
import Pricing from '@/components/Pricing';
import FAQ from '@/components/FAQ';
import Footer from '@/components/Footer';
import CTASection from '@/components/CTASection';

function LandingPage() {
  return (
    <div className="min-h-screen bg-background font-sans selection:bg-accent/30 selection:text-primary">
      <Navbar />
      <main>
        <Hero />
        <TrustedBy />
        <Features />
        <Workflow />
        <DashboardShowcase />
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

export default LandingPage;
