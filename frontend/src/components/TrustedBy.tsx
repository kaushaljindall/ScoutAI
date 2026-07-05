
const TrustedBy = () => {
  return (
    <section className="py-12 border-y border-border/50 bg-background/50">
      <div className="max-w-7xl mx-auto px-6 md:px-12">
        <p className="text-center text-sm text-primary/40 font-medium mb-8">TRUSTED BY TEAMS AT</p>
        <div className="flex flex-wrap justify-center items-center gap-8 md:gap-16 opacity-40 grayscale hover:grayscale-0 transition-all duration-500">
          <span className="text-xl font-bold tracking-tighter">ACME CORP</span>
          <span className="text-xl font-bold tracking-tight">Globex</span>
          <span className="text-xl font-semibold tracking-wide">soylent</span>
          <span className="text-xl font-bold">Initech</span>
          <span className="text-xl font-bold tracking-tight">UMBRELLA</span>
        </div>
      </div>
    </section>
  );
};

export default TrustedBy;
