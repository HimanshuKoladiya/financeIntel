import React from 'react';
import { Search, Bell, ShieldCheck, User } from 'lucide-react';

export const Header: React.FC = () => {
  return (
    <header className="h-16 bg-white border-b border-slate-200 px-6 flex items-center justify-between sticky top-0 z-20">
      <div className="flex items-center gap-4">
        <span className="text-xs font-semibold uppercase tracking-wider text-slate-500">
          Enterprise Disbursements
        </span>
        <span className="text-slate-300">/</span>
        <span className="text-sm font-semibold text-slate-900">
          Procure-to-Pay (P2P) Decision Intelligence
        </span>
      </div>

      <div className="flex items-center gap-5">
        <div className="relative">
          <Search className="w-4 h-4 text-slate-400 absolute left-3 top-1/2 -translate-y-1/2" />
          <input
            type="text"
            placeholder="Search PO#, Invoice#, Vendor (⌘K)"
            className="pl-9 pr-4 py-1.5 text-xs bg-slate-50 border border-slate-200 rounded-lg w-64 focus:outline-none focus:ring-1 focus:ring-blue-500 focus:bg-white"
          />
        </div>

        <div className="flex items-center gap-2 px-2.5 py-1 bg-emerald-50 border border-emerald-200 rounded-full text-emerald-700 text-xs font-medium">
          <ShieldCheck className="w-3.5 h-3.5 text-emerald-600" />
          <span>SAP ECC & CLM Live Sync</span>
        </div>

        <button className="relative p-2 text-slate-500 hover:text-slate-700 hover:bg-slate-100 rounded-lg transition-colors">
          <Bell className="w-4 h-4" />
          <span className="absolute top-1.5 right-1.5 w-2 h-2 bg-rose-500 rounded-full" />
        </button>

        <div className="flex items-center gap-3 border-l border-slate-200 pl-4">
          <div className="w-8 h-8 rounded-full bg-slate-900 text-white flex items-center justify-center font-bold text-xs">
            VM
          </div>
          <div className="text-left hidden md:block">
            <div className="text-xs font-bold text-slate-900">Vikram Malhotra</div>
            <div className="text-[10px] text-slate-500">Principal Financial Controller</div>
          </div>
        </div>
      </div>
    </header>
  );
};
