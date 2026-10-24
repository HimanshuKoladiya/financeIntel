import React from 'react';
import { AlertTriangle, ArrowUpRight, ShieldAlert, CheckCircle2 } from 'lucide-react';

interface ExceptionItem {
  id: string;
  type: string;
  severity: string;
  vendor_name: string;
  po_number: string;
  invoice_number: string;
  financial_exposure: number;
  status: string;
}

interface ExceptionQueueProps {
  exceptions: ExceptionItem[];
  onSelectException: (id: string) => void;
  selectedId?: string;
}

export const ExceptionQueue: React.FC<ExceptionQueueProps> = ({
  exceptions,
  onSelectException,
  selectedId
}) => {
  return (
    <div className="bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden">
      <div className="p-4 border-b border-slate-200 flex items-center justify-between bg-slate-50/50">
        <div>
          <h2 className="text-sm font-bold text-slate-900">Cross-Document Exception Queue</h2>
          <p className="text-xs text-slate-500">Autonomous reasoning flagged payment risks requiring controller sign-off</p>
        </div>
        <span className="text-xs font-semibold bg-blue-50 text-blue-700 px-3 py-1 rounded-full border border-blue-200">
          {exceptions.length} Active Discrepancies
        </span>
      </div>

      <div className="overflow-x-auto">
        <table className="w-full text-left text-xs">
          <thead className="bg-slate-50 text-slate-600 font-semibold uppercase tracking-wider border-b border-slate-200">
            <tr>
              <th className="py-3 px-4">Severity / Status</th>
              <th className="py-3 px-4">Vendor Entity</th>
              <th className="py-3 px-4">PO & Invoice Ref</th>
              <th className="py-3 px-4">Discrepancy Signature</th>
              <th className="py-3 px-4 text-right">Monetary Exposure</th>
              <th className="py-3 px-4 text-center">Action</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-100">
            {exceptions.map((item) => {
              const isSelected = item.id === selectedId;
              const isCritical = item.severity === 'CRITICAL';
              return (
                <tr
                  key={item.id}
                  className={`hover:bg-slate-50 transition-colors ${
                    isSelected ? 'bg-blue-50/70 border-l-4 border-blue-600' : ''
                  }`}
                >
                  <td className="py-3.5 px-4 whitespace-nowrap">
                    <span className={`inline-flex items-center gap-1 px-2.5 py-1 rounded-md text-[11px] font-bold ${
                      item.status === 'DISPUTED'
                        ? 'bg-emerald-50 text-emerald-700 border border-emerald-200'
                        : item.status === 'OVERRIDDEN'
                        ? 'bg-purple-50 text-purple-700 border border-purple-200'
                        : isCritical
                        ? 'bg-rose-50 text-rose-700 border border-rose-200'
                        : 'bg-amber-50 text-amber-700 border border-amber-200'
                    }`}>
                      {item.status === 'HOLD' ? <AlertTriangle className="w-3 h-3" /> : <CheckCircle2 className="w-3 h-3" />}
                      {item.status}: {item.severity}
                    </span>
                  </td>
                  <td className="py-3.5 px-4 font-bold text-slate-900 whitespace-nowrap">
                    {item.vendor_name}
                  </td>
                  <td className="py-3.5 px-4 whitespace-nowrap text-slate-600 font-mono">
                    <div>{item.po_number}</div>
                    <div className="text-[10px] text-slate-400">{item.invoice_number}</div>
                  </td>
                  <td className="py-3.5 px-4 font-medium text-slate-700">
                    {item.type === 'PRICE_VARIANCE' ? 'Unit Price > Contract MSA Ceiling' : 'Billed Qty > Warehouse GRN Receipt'}
                  </td>
                  <td className="py-3.5 px-4 text-right font-black text-slate-900 whitespace-nowrap font-mono">
                    ₹{item.financial_exposure.toLocaleString('en-IN', { minimumFractionDigits: 2 })}
                  </td>
                  <td className="py-3.5 px-4 text-center whitespace-nowrap">
                    <button
                      onClick={() => onSelectException(item.id)}
                      className={`inline-flex items-center gap-1 px-3 py-1.5 rounded-lg text-xs font-bold transition-all ${
                        isSelected
                          ? 'bg-blue-600 text-white shadow-sm'
                          : 'bg-white text-slate-700 border border-slate-300 hover:bg-slate-100'
                      }`}
                    >
                      <span>Decision Brief</span>
                      <ArrowUpRight className="w-3 h-3" />
                    </button>
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
};
