import { Outlet } from 'react-router-dom';

export default function AuthLayout() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-background p-4 relative overflow-hidden">
      {/* Subtle background gradient for auth pages */}
      <div className="absolute top-1/4 -left-1/4 w-[500px] h-[500px] bg-accent/10 rounded-full blur-[120px] pointer-events-none"></div>
      <div className="absolute bottom-1/4 -right-1/4 w-[500px] h-[500px] bg-accent-secondary/10 rounded-full blur-[120px] pointer-events-none"></div>
      
      <div className="w-full max-w-md z-10">
        <div className="text-center mb-8">
          <div className="inline-flex items-center justify-center w-12 h-12 rounded-xl bg-accent/10 border border-accent/20 text-accent mb-4">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M19.07 4.93A10 10 0 0 0 6.99 3.34"/><path d="M4 5.49A10 10 0 0 0 4.6 20.64"/><path d="M19.07 4.93a10 10 0 0 1-2.52 16.3"/><path d="M2.5 12h14"/><path d="M12 2.5v14"/><path d="M7 12l5 5 5-5"/></svg>
          </div>
          <h1 className="text-2xl font-bold tracking-tight">ScoutAI</h1>
        </div>
        
        <Outlet />
      </div>
    </div>
  );
}
