import React from 'react';
import { LayoutDashboard, AlertOctagon, Database, FileText, Settings, ShieldAlert } from 'lucide-react';

interface SidebarProps {
  currentTab: string;
  setCurrentTab: (tab: string) => void;
  exceptionCount: number;
}

export const Sidebar: React.FC<SidebarProps> = ({ currentTab, setCurrentTab, exceptionCount }) => {
  const menuItems = [
    { id: 'dashboard', label: 'Executive Overview', icon: LayoutDashboard },
    { id: 'queue', label: 'Exception Queue', icon: AlertOctagon, badge: exceptionCount },
    { id: 'datasources', label: 'Enterprise Connectors', icon: Database },
    { id: 'audit', label: 'SOX Compliance Ledger', icon: FileText },
    { id: 'settings', label: 'Intelligence Rules', icon: Settings },
  ];

  return (
    <aside className="w-64 bg-slate-950 text-slate-300 flex flex-col justify-between shrink-0 select-none">
      <div>
        <div className="h-16 flex items-center gap-3 px-6 border-b border-slate-800">
          <div className="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center text-white font-black text-base shadow-lg shadow-blue-500/30">
            <ShieldAlert className="w-5 h-5 text-white" />
          </div>
          <div>
            <div className="font-bold text-white tracking-wide text-sm">financeIntel</div>
            <div className="text-[10px] text-blue-400 font-mono">INTELLIGENCE LAYER</div>
          </div>
        </div>

        <nav className="p-3 space-y-1">
          {menuItems.map((item) => {
            const Icon = item.icon;
            const isActive = currentTab === item.id;
            return (
              <button
                key={item.id}
                onClick={() => setCurrentTab(item.id)}
                className={`w-full flex items-center justify-between px-3.5 py-2.5 rounded-lg text-xs font-medium transition-all ${
                  isActive
                    ? 'bg-blue-600 text-white font-semibold shadow-md shadow-blue-600/30'
                    : 'text-slate-400 hover:text-slate-100 hover:bg-slate-900'
                }`}
              >
                <div className="flex items-center gap-3">
                  <Icon className={`w-4 h-4 ${isActive ? 'text-white' : 'text-slate-400'}`} />
                  <span>{item.label}</span>
                </div>
                {item.badge !== undefined && (
                  <span className={`px-2 py-0.5 rounded-full text-[10px] font-bold ${
                    isActive ? 'bg-white text-blue-700' : 'bg-rose-500/20 text-rose-300 border border-rose-500/30'
                  }`}>
                    {item.badge}
                  </span>
                )}
              </button>
            );
          })}
        </nav>
      </div>

      <div className="p-4 border-t border-slate-800 bg-slate-900/50 m-3 rounded-xl">
        <div className="text-[11px] font-semibold text-slate-200">System Autonomous Health</div>
        <div className="text-[10px] text-slate-400 mt-0.5">Airflow Orchestrator: Nominal</div>
        <div className="w-full bg-slate-800 h-1.5 rounded-full mt-2 overflow-hidden">
          <div className="bg-emerald-500 h-full w-[94%]" />
        </div>
      </div>
    </aside>
  );
};
