import { Outlet, useNavigate, NavLink } from 'react-router-dom';
import { useAuthStore } from '@/store/authStore';
import { Button } from '@/components/ui/Button';
import { useLogout } from '@/hooks/useAuth';
import { LayoutDashboard, Search, Briefcase, Settings, Bot } from 'lucide-react';
import { cn } from '@/utils/cn';

export default function DashboardLayout() {
  const user = useAuthStore((state) => state.user);
  const navigate = useNavigate();
  const logoutMutation = useLogout();

  const handleLogout = () => {
    logoutMutation.mutate(undefined, {
      onSettled: () => {
        navigate('/login');
      }
    });
  };

  const navItems = [
    { name: 'Overview', path: '/dashboard', icon: LayoutDashboard, exact: true },
    { name: 'Scout', path: '/dashboard/scout', icon: Search, exact: false },
    { name: 'CRM', path: '/dashboard/crm', icon: Briefcase, exact: false },
    { name: 'Copilot', path: '/dashboard/copilot', icon: Bot, exact: false },
    { name: 'Settings', path: '/dashboard/settings', icon: Settings, exact: false },
  ];

  return (
    <div className="min-h-screen bg-background flex flex-col">
      {/* Top Navigation */}
      <header className="h-16 border-b border-border bg-surface/30 px-6 flex items-center justify-between sticky top-0 z-40 backdrop-blur-md">
        <div className="flex items-center gap-4">
          <div className="w-8 h-8 rounded bg-accent flex items-center justify-center text-background font-bold text-lg leading-none">
            S
          </div>
          <span className="font-bold tracking-tight text-lg hidden sm:block">ScoutAI</span>
          <div className="h-4 w-px bg-border mx-2 hidden sm:block"></div>
          <span className="text-sm font-medium text-primary/80 hidden sm:block">Workspace</span>
        </div>
        
        <div className="flex items-center gap-4">
          <span className="text-sm text-primary/60 hidden sm:block">{user?.email}</span>
          <Button variant="outline" size="sm" onClick={handleLogout} isLoading={logoutMutation.isPending}>
            Logout
          </Button>
        </div>
      </header>

      {/* Main Content */}
      <div className="flex-1 flex overflow-hidden">
        {/* Sidebar */}
        <aside className="w-64 border-r border-border bg-surface/10 p-4 hidden md:flex flex-col gap-2">
          {navItems.map(item => (
            <NavLink
              key={item.name}
              to={item.path}
              end={item.exact}
              className={({ isActive }) => cn(
                "px-3 py-2.5 rounded-md flex items-center gap-3 text-sm font-medium transition-colors",
                isActive ? "bg-accent/10 text-accent" : "text-primary/60 hover:bg-surface hover:text-primary"
              )}
            >
              <item.icon size={16} />
              {item.name}
            </NavLink>
          ))}
        </aside>

        {/* Page Content */}
        <main className="flex-1 overflow-auto p-6 md:p-8">
          <div className="max-w-6xl mx-auto h-full">
            <Outlet />
          </div>
        </main>
      </div>
    </div>
  );
}
