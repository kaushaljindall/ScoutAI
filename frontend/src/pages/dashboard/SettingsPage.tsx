import { useState } from 'react';
import { Button } from '@/components/ui/Button';
import { useAuthStore } from '@/store/authStore';
import { User, Shield, Bell, Palette, Globe, Briefcase, Download, LogOut, CheckCircle2 } from 'lucide-react';
import { cn } from '@/utils/cn';

export default function SettingsPage() {
  const user = useAuthStore((state) => state.user);
  const [activeTab, setActiveTab] = useState('Profile');
  const [saved, setSaved] = useState(false);

  const tabs = [
    { name: 'Profile', icon: User },
    { name: 'Account & Security', icon: Shield },
    { name: 'Notifications', icon: Bell },
    { name: 'Appearance', icon: Palette },
    { name: 'Branding', icon: Briefcase },
    { name: 'Data & Export', icon: Download },
  ];

  const handleSave = () => {
    setSaved(true);
    setTimeout(() => setSaved(false), 3000);
  };

  return (
    <div className="h-full flex flex-col pt-2 pb-6">
      <div className="mb-6 flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Settings</h1>
          <p className="text-primary/60 mt-1">Manage your account preferences and application settings.</p>
        </div>
      </div>

      <div className="flex gap-8 flex-1 min-h-0">
        {/* Sidebar */}
        <div className="w-64 shrink-0 flex flex-col gap-1">
          {tabs.map((tab) => (
            <button
              key={tab.name}
              onClick={() => setActiveTab(tab.name)}
              className={cn(
                "flex items-center gap-3 px-4 py-3 rounded-lg text-sm font-medium transition-colors text-left",
                activeTab === tab.name 
                  ? "bg-accent/10 text-accent" 
                  : "text-primary/70 hover:bg-surface/50 hover:text-primary"
              )}
            >
              <tab.icon size={16} />
              {tab.name}
            </button>
          ))}
          
          <div className="mt-auto pt-4 border-t border-border/50">
             <button className="flex items-center gap-3 px-4 py-3 rounded-lg text-sm font-medium text-red-500 hover:bg-red-500/10 transition-colors w-full text-left">
                <LogOut size={16} /> Sign Out All Devices
             </button>
          </div>
        </div>

        {/* Content Area */}
        <div className="flex-1 bg-surface/20 border border-border/50 rounded-2xl overflow-y-auto">
          {activeTab === 'Profile' && (
            <div className="p-8 max-w-2xl">
              <h2 className="text-xl font-bold mb-6">Profile Information</h2>
              
              <div className="space-y-6">
                <div className="flex items-center gap-6 pb-6 border-b border-border/50">
                  <div className="w-20 h-20 rounded-full bg-accent/20 flex items-center justify-center text-accent text-2xl font-bold">
                    {user?.email?.[0].toUpperCase() || 'S'}
                  </div>
                  <div>
                    <Button variant="outline" size="sm" className="mb-2">Upload New Avatar</Button>
                    <p className="text-xs text-primary/50">At least 800x800 px recommended. JPG or PNG is allowed.</p>
                  </div>
                </div>
                
                <div className="grid grid-cols-2 gap-4">
                  <div className="space-y-2">
                    <label className="text-sm font-medium">First Name</label>
                    <input type="text" className="w-full bg-background border border-border/50 rounded-lg p-2.5 text-sm outline-none focus:border-accent" defaultValue="Scout" />
                  </div>
                  <div className="space-y-2">
                    <label className="text-sm font-medium">Last Name</label>
                    <input type="text" className="w-full bg-background border border-border/50 rounded-lg p-2.5 text-sm outline-none focus:border-accent" defaultValue="User" />
                  </div>
                </div>
                
                <div className="space-y-2">
                  <label className="text-sm font-medium">Email Address</label>
                  <input type="email" disabled className="w-full bg-surface/50 border border-border/50 rounded-lg p-2.5 text-sm outline-none opacity-60" value={user?.email} />
                </div>
                
                <div className="space-y-2">
                  <label className="text-sm font-medium">Time Zone</label>
                  <div className="relative">
                    <Globe size={16} className="absolute left-3 top-1/2 -translate-y-1/2 text-primary/50" />
                    <select className="w-full bg-background border border-border/50 rounded-lg p-2.5 pl-10 text-sm outline-none focus:border-accent appearance-none">
                      <option>Asia/Kolkata (IST)</option>
                      <option>America/New_York (EST)</option>
                      <option>Europe/London (GMT)</option>
                    </select>
                  </div>
                </div>
              </div>
            </div>
          )}

          {activeTab === 'Branding' && (
            <div className="p-8 max-w-2xl">
              <h2 className="text-xl font-bold mb-2">Default Branding</h2>
              <p className="text-sm text-primary/60 mb-6">These details will be used automatically in Proposals and Documents.</p>
              
              <div className="space-y-6">
                <div className="space-y-2">
                  <label className="text-sm font-medium">Company Name</label>
                  <input type="text" className="w-full bg-background border border-border/50 rounded-lg p-2.5 text-sm outline-none focus:border-accent" placeholder="e.g. Acme Web Services" />
                </div>
                
                <div className="grid grid-cols-2 gap-4">
                  <div className="space-y-2">
                    <label className="text-sm font-medium">Website</label>
                    <input type="url" className="w-full bg-background border border-border/50 rounded-lg p-2.5 text-sm outline-none focus:border-accent" placeholder="https://" />
                  </div>
                  <div className="space-y-2">
                    <label className="text-sm font-medium">Support Email</label>
                    <input type="email" className="w-full bg-background border border-border/50 rounded-lg p-2.5 text-sm outline-none focus:border-accent" placeholder="hello@company.com" />
                  </div>
                </div>
                
                <div className="space-y-2">
                  <label className="text-sm font-medium">Brand Primary Color</label>
                  <div className="flex items-center gap-4">
                    <input type="color" className="w-10 h-10 rounded cursor-pointer bg-background" defaultValue="#6366f1" />
                    <span className="text-sm font-mono text-primary/60">#6366f1</span>
                  </div>
                </div>
              </div>
            </div>
          )}
          
          {activeTab === 'Data & Export' && (
            <div className="p-8 max-w-2xl">
              <h2 className="text-xl font-bold mb-6">Data Management</h2>
              
              <div className="space-y-4">
                <div className="p-4 border border-border/50 bg-background rounded-xl flex items-center justify-between">
                   <div>
                     <h4 className="font-semibold text-sm">Export CRM Data</h4>
                     <p className="text-xs text-primary/60 mt-1">Download all your leads and pipelines in CSV format.</p>
                   </div>
                   <Button variant="outline" size="sm" className="gap-2"><Download size={14} /> Export CSV</Button>
                </div>
                
                <div className="p-4 border border-border/50 bg-background rounded-xl flex items-center justify-between">
                   <div>
                     <h4 className="font-semibold text-sm">Workspace Backup</h4>
                     <p className="text-xs text-primary/60 mt-1">Download a full JSON backup of your documents and notes.</p>
                   </div>
                   <Button variant="outline" size="sm" className="gap-2"><Download size={14} /> Backup JSON</Button>
                </div>
              </div>
            </div>
          )}
          
          {/* Footer Save Button */}
          <div className="sticky bottom-0 p-4 border-t border-border/50 bg-surface/50 backdrop-blur-md flex justify-end items-center gap-4">
             {saved && <span className="text-emerald-500 text-sm flex items-center gap-1.5 animate-in fade-in"><CheckCircle2 size={14} /> Settings Saved</span>}
             <Button onClick={handleSave} className="min-w-[120px]">Save Changes</Button>
          </div>
        </div>
      </div>
    </div>
  );
}
