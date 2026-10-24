'use client';

import React, { useEffect, useState } from 'react';
import { Header } from '@/components/Header';
import { Sidebar } from '@/components/Sidebar';
import { ExceptionQueue } from '@/components/ExceptionQueue';
import { DecisionBrief } from '@/components/DecisionBrief';
import { ShieldAlert, AlertTriangle, TrendingDown, DollarSign } from 'lucide-react';

export default function Home() {
  const [currentTab, setCurrentTab] = useState('queue');
  const [exceptions, setExceptions] = useState<any[]>([]);
  const [selectedExceptionId, setSelectedExceptionId] = useState<string>('EXC-8841');
  const [briefData, setBriefData] = useState<any>(null);
  const [metrics, setMetrics] = useState<any>({
    pending_exceptions_count: 2,
    total_exposure_on_hold: 376000,
    automated_dispute_rate: 88.5,
    working_capital_protected: 11245000
  });

  const fetchExceptions = async () => {
    try {
      const res = await fetch('http://localhost:8000/api/exceptions');
      if (res.ok) {
        const data = await res.json();
        setExceptions(data);
      }
    } catch (e) {
      console.warn("Backend not reachable yet, using fallback data");
      setExceptions([
        {
          id: 'EXC-8841',
          type: 'PRICE_VARIANCE',
          severity: 'CRITICAL',
          vendor_name: 'Apex Technologies Ltd.',
          po_number: 'PO-2024-8841',
          invoice_number: 'INV-99210-A',
          financial_exposure: 136000,
          status: 'HOLD'
        },
        {
          id: 'EXC-8890',
          type: 'QUANTITY_SHORTFALL',
          severity: 'HIGH',
          vendor_name: 'TechCorp Solutions Inc.',
          po_number: 'PO-2024-8890',
          invoice_number: 'INV-4402',
          financial_exposure: 240000,
          status: 'HOLD'
        }
      ]);
    }
  };

  const fetchBrief = async (id: string) => {
    try {
      const res = await fetch(`http://localhost:8000/api/decision-brief/${id}`);
      if (res.ok) {
        const data = await res.json();
        setBriefData(data);
      }
    } catch (e) {
      console.warn("Backend not reachable, rendering client fallback brief");
      setBriefData({
        id: 'BRIEF-8841',
        exception_id: 'EXC-8841',
        decision_status: 'HOLD',
        financial_exposure: 136000,
        ai_reasoning_text: 'Cross-document AI reasoning detected unauthorized ₹3,400 surcharge on 40 laptops.',
        verified_evidence: [
          "Invoice INV-99210-A bills 40x ThinkPad T14 at ₹71,900.00/unit.",
          "Contract MSA-2023-V4 Clause 4.2 caps rate at ₹68,500.00 net through Q4 2024.",
          "WMS GRN-44910 verifies 40 units physically received in Bangalore Central Hub."
        ],
        recommended_actions: [
          "Apply immediate SAP ERP Payment Block 'R' on Invoice #INV-99210-A.",
          "Issue automated dispute notification to supplier."
        ],
        draft_communication: "Dear Apex Technologies Billing Team,\nPayment on Invoice INV-99210-A is on HOLD due to a ₹3,400/unit variance against MSA-2023-V4 Clause 4.2.",
        fragmented_evidence: {
          purchase_order: {
            po_number: 'PO-2024-8841',
            total_amount: 2740000,
            items: [{ description: 'ThinkPad T14 Gen 4 Laptop', quantity: 40, unit_price: 68500 }]
          },
          invoice: {
            invoice_number: 'INV-99210-A',
            billed_amount: 2876000,
            items: [{ description: 'ThinkPad T14 Gen 4 Laptop', quantity: 40, unit_price: 71900 }]
          },
          goods_receipt: {
            grn_number: 'GRN-44910',
            location: 'Bangalore Central Logistics Hub (DC-02)',
            received_date: '2024-10-18',
            items: [{ description: 'ThinkPad T14 Gen 4 Laptop', received_quantity: 40 }]
          },
          contract: {
            title: 'Master Hardware MSA-2023-V4',
            terms: 'Clause 4.2: ThinkPad T14 Gen 4 enterprise units are rate-locked at ₹68,500 net per unit through Q4 2024. No unilateral surcharge permitted.'
          }
        }
      });
    }
  };

  useEffect(() => {
    fetchExceptions();
  }, []);

  useEffect(() => {
    if (selectedExceptionId) {
      fetchBrief(selectedExceptionId);
    }
  }, [selectedExceptionId]);

  return (
    <div className="flex h-screen bg-slate-100 font-sans overflow-hidden">
      <Sidebar
        currentTab={currentTab}
        setCurrentTab={setCurrentTab}
        exceptionCount={exceptions.filter(e => e.status === 'HOLD').length}
      />

      <div className="flex-1 flex flex-col min-w-0 overflow-y-auto">
        <Header />

        <main className="p-6 space-y-6">
          {/* Executive Summary Metrics Strip */}
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
            <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-sm flex items-center justify-between">
              <div>
                <span className="text-[11px] font-bold uppercase tracking-wider text-slate-500">Exceptions on Hold</span>
                <div className="text-2xl font-black text-slate-900 mt-1">{metrics.pending_exceptions_count} Cases</div>
              </div>
              <div className="w-10 h-10 rounded-xl bg-rose-50 text-rose-600 flex items-center justify-center">
                <AlertTriangle className="w-5 h-5" />
              </div>
            </div>

            <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-sm flex items-center justify-between">
              <div>
                <span className="text-[11px] font-bold uppercase tracking-wider text-slate-500">Value on Hold</span>
                <div className="text-2xl font-black text-rose-600 mt-1 font-mono">
                  ₹{metrics.total_exposure_on_hold?.toLocaleString('en-IN')}
                </div>
              </div>
              <div className="w-10 h-10 rounded-xl bg-amber-50 text-amber-600 flex items-center justify-center">
                <DollarSign className="w-5 h-5" />
              </div>
            </div>

            <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-sm flex items-center justify-between">
              <div>
                <span className="text-[11px] font-bold uppercase tracking-wider text-slate-500">Auto-Dispute Rate</span>
                <div className="text-2xl font-black text-slate-900 mt-1">{metrics.automated_dispute_rate}%</div>
              </div>
              <div className="w-10 h-10 rounded-xl bg-blue-50 text-blue-600 flex items-center justify-center">
                <TrendingDown className="w-5 h-5" />
              </div>
            </div>

            <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-sm flex items-center justify-between">
              <div>
                <span className="text-[11px] font-bold uppercase tracking-wider text-slate-500">Protected Working Capital</span>
                <div className="text-2xl font-black text-emerald-600 mt-1 font-mono">
                  ₹{(metrics.working_capital_protected / 10000000).toFixed(2)} Cr
                </div>
              </div>
              <div className="w-10 h-10 rounded-xl bg-emerald-50 text-emerald-600 flex items-center justify-center">
                <ShieldAlert className="w-5 h-5" />
              </div>
            </div>
          </div>

          {/* Exception Queue Table */}
          <ExceptionQueue
            exceptions={exceptions}
            onSelectException={(id) => setSelectedExceptionId(id)}
            selectedId={selectedExceptionId}
          />

          {/* Cinematic Split-Screen Decision Brief */}
          {briefData && (
            <div className="pt-2">
              <div className="mb-3 flex items-center justify-between">
                <h2 className="text-sm font-bold text-slate-900">
                  Inspecting Case #{selectedExceptionId}: {briefData.fragmented_evidence.purchase_order.po_number}
                </h2>
                <span className="text-xs text-slate-500">Click below to test Hold, Dispute Executed, or Override transitions</span>
              </div>
              <DecisionBrief
                briefData={briefData}
                onRefresh={() => {
                  fetchExceptions();
                  fetchBrief(selectedExceptionId);
                }}
              />
            </div>
          )}
        </main>
      </div>
    </div>
  );
}
