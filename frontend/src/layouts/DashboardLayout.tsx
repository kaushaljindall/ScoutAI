import { Outlet, useNavigate } from 'react-router-dom';
import { useAuthStore } from '@/store/authStore';
import { Button } from '@/components/ui/Button';

export default function DashboardLayout() {
  const logout = useAuthStore((state) => state.logout);
  const user = useAuthStore((state) => state.user);
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <div className="min-h-screen bg-background flex flex-col">
      {/* Top Navigation */}
      <header className="h-16 border-b border-border bg-surface/30 px-6 flex items-center justify-between sticky top-0 z-40 backdrop-blur-md">
        <div className="flex items-center gap-4">
          <span className="font-bold tracking-tight text-lg">ScoutAI</span>
          <div className="h-4 w-px bg-border mx-2"></div>
          <span className="text-sm font-medium text-primary/80">Dashboard</span>
        </div>
        
        <div className="flex items-center gap-4">
          <span className="text-sm text-primary/60">{user?.email}</span>
          <Button variant="outline" size="sm" onClick={handleLogout}>
            Logout
          </Button>
        </div>
      </header>

      {/* Main Content */}
      <div className="flex-1 flex overflow-hidden">
        {/* Sidebar */}
        <aside className="w-64 border-r border-border bg-surface/10 p-4 hidden md:flex flex-col gap-2">
          <div className="px-3 py-2 rounded-md bg-accent/10 text-accent font-medium text-sm">
            Overview
          </div>
          <div className="px-3 py-2 rounded-md text-primary/60 hover:bg-surface hover:text-primary transition-colors cursor-pointer text-sm font-medium">
            Leads
          </div>
          <div className="px-3 py-2 rounded-md text-primary/60 hover:bg-surface hover:text-primary transition-colors cursor-pointer text-sm font-medium">
            Campaigns
          </div>
          <div className="px-3 py-2 rounded-md text-primary/60 hover:bg-surface hover:text-primary transition-colors cursor-pointer text-sm font-medium">
            Settings
          </div>
        </aside>

        {/* Page Content */}
        <main className="flex-1 overflow-auto p-6 md:p-8">
          <div className="max-w-6xl mx-auto">
            <Outlet />
          </div>
        </main>
      </div>
    </div>
  );
}
