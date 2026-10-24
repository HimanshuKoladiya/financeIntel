import React, { useState } from 'react';
import { 
  ShieldAlert, CheckCircle, Mail, AlertOctagon, 
  FileCheck, FileText, ArrowRight, Lock, Undo2 
} from 'lucide-react';

interface DecisionBriefProps {
  briefData: any;
  onRefresh: () => void;
}

export const DecisionBrief: React.FC<DecisionBriefProps> = ({ briefData, onRefresh }) => {
  const [draftMessage, setDraftMessage] = useState(briefData.draft_communication);
  const [showOverrideModal, setShowOverrideModal] = useState(false);
  const [overrideReason, setOverrideReason] = useState('Emergency Project Delivery');
  const [justification, setJustification] = useState('');
  const [waiverSigned, setWaiverSigned] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);

  const isDisputed = briefData.decision_status === 'DISPUTE_EXECUTED';
  const isOverridden = briefData.decision_status === 'MANUAL_OVERRIDE_APPROVED';

  const handleExecuteDispute = async () => {
    setIsSubmitting(true);
    try {
      const res = await fetch(`http://localhost:8000/api/decision-brief/${briefData.exception_id}/execute-dispute`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          recipient_email: "accounts.receivable@apextech.com",
          customized_message: draftMessage
        })
      });
      if (res.ok) {
        onRefresh();
      }
    } catch (e) {
      console.error(e);
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleAuthorizeOverride = async () => {
    if (!waiverSigned) return;
    setIsSubmitting(true);
    try {
      const res = await fetch(`http://localhost:8000/api/decision-brief/${briefData.exception_id}/override`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          controller_name: "Vikram Malhotra (Principal Controller)",
          reason_code: overrideReason,
          justification: justification || "Approved via VP Delegation of Authority",
          signed_waiver: waiverSigned
        })
      });
      if (res.ok) {
        setShowOverrideModal(false);
        onRefresh();
      }
    } catch (e) {
      console.error(e);
    } finally {
      setIsSubmitting(false);
    }
  };

  const evidence = briefData.fragmented_evidence;

  return (
    <div className="space-y-4">
      {/* State Notification Banner */}
      {isDisputed && (
        <div className="bg-emerald-600 text-white px-5 py-3 rounded-xl shadow-md flex items-center justify-between">
          <div className="flex items-center gap-3">
            <CheckCircle className="w-5 h-5 text-emerald-200" />
            <div>
              <div className="font-bold text-sm">Dispute Executed & SAP Payment Block Active</div>
              <div className="text-xs text-emerald-100">Discrepancy notice dispatched to supplier. SAP ECC document locked under Block 'R'.</div>
            </div>
          </div>
          <span className="text-xs bg-emerald-700 px-3 py-1 rounded-full font-mono font-semibold">Case #DISP-8841-A</span>
        </div>
      )}

      {isOverridden && (
        <div className="bg-purple-700 text-white px-5 py-3 rounded-xl shadow-md flex items-center justify-between">
          <div className="flex items-center gap-3">
            <Lock className="w-5 h-5 text-purple-200" />
            <div>
              <div className="font-bold text-sm">Manual Controller Override Logged</div>
              <div className="text-xs text-purple-200">Fiduciary sign-off recorded in SOX immutable compliance ledger. Payment released.</div>
            </div>
          </div>
          <span className="text-xs bg-purple-800 px-3 py-1 rounded-full font-mono font-semibold">Audit Level 3</span>
        </div>
      )}

      {/* Split-Screen Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        
        {/* LEFT COLUMN: Fragmented Evidence Matrix */}
        <div className="lg:col-span-6 space-y-4">
          <div className="flex items-center justify-between">
            <h3 className="text-xs font-bold uppercase tracking-wider text-slate-500">
              Fragmented Enterprise Source Records
            </h3>
            <span className="text-[11px] text-slate-400">4-Way Document Correlation</span>
          </div>

          {/* 1. Purchase Order */}
          <div className="bg-white rounded-xl border border-slate-200 p-4 shadow-sm">
            <div className="flex items-center justify-between border-b border-slate-100 pb-2 mb-3">
              <div className="flex items-center gap-2">
                <FileText className="w-4 h-4 text-blue-600" />
                <span className="text-xs font-bold text-slate-800">SAP ERP Purchase Order</span>
              </div>
              <span className="text-xs font-mono font-bold text-slate-600">{evidence.purchase_order.po_number}</span>
            </div>
            <div className="space-y-1.5 text-xs">
              {evidence.purchase_order.items?.map((item: any, idx: number) => (
                <div key={idx} className="flex justify-between items-center bg-slate-50 p-2 rounded-lg">
                  <div>
                    <div className="font-semibold text-slate-800">{item.description}</div>
                    <div className="text-[11px] text-slate-500">Qty: {item.quantity} units</div>
                  </div>
                  <div className="text-right">
                    <div className="font-mono font-bold text-slate-900">₹{item.unit_price?.toLocaleString('en-IN')}</div>
                    <div className="text-[10px] text-slate-400">Agreed PO Rate</div>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* 2. Vendor Invoice (OCR Extracted) - CONFLICT HIGHLIGHTED IN RED */}
          <div className="bg-white rounded-xl border-2 border-rose-300 p-4 shadow-sm bg-rose-50/20">
            <div className="flex items-center justify-between border-b border-rose-100 pb-2 mb-3">
              <div className="flex items-center gap-2">
                <AlertOctagon className="w-4 h-4 text-rose-600" />
                <span className="text-xs font-bold text-rose-900">Billed Vendor Invoice (OCR Extract)</span>
              </div>
              <span className="text-xs font-mono font-bold text-rose-700">{evidence.invoice.invoice_number}</span>
            </div>
            <div className="space-y-1.5 text-xs">
              {evidence.invoice.items?.map((item: any, idx: number) => (
                <div key={idx} className="flex justify-between items-center bg-rose-100/60 p-2.5 rounded-lg border border-rose-200">
                  <div>
                    <div className="font-bold text-rose-950">{item.description}</div>
                    <div className="text-[11px] text-rose-700">Invoiced: {item.quantity} units</div>
                  </div>
                  <div className="text-right">
                    <div className="font-mono font-black text-rose-700 text-sm">
                      ₹{item.unit_price?.toLocaleString('en-IN')}
                    </div>
                    <div className="text-[10px] font-bold text-rose-600 uppercase tracking-tight">
                      +₹3,400 Unauthorized Surcharge
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* 3. Goods Receipt Note (WMS) */}
          <div className="bg-white rounded-xl border border-slate-200 p-4 shadow-sm">
            <div className="flex items-center justify-between border-b border-slate-100 pb-2 mb-3">
              <div className="flex items-center gap-2">
                <FileCheck className="w-4 h-4 text-emerald-600" />
                <span className="text-xs font-bold text-slate-800">Warehouse Goods Receipt (WMS)</span>
              </div>
              <span className="text-xs font-mono font-bold text-slate-600">{evidence.goods_receipt.grn_number}</span>
            </div>
            <div className="text-xs space-y-1 bg-slate-50 p-2 rounded-lg">
              <div className="flex justify-between">
                <span className="text-slate-500">Physical Inbound Location:</span>
                <span className="font-medium text-slate-800">{evidence.goods_receipt.location}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-500">Verified Quantity Received:</span>
                <span className="font-bold text-emerald-700">40 units (100% physically received)</span>
              </div>
            </div>
          </div>

          {/* 4. Master Contract (CLM) - HIGHLIGHTED IN YELLOW */}
          <div className="bg-amber-50/60 rounded-xl border border-amber-300 p-4 shadow-sm">
            <div className="flex items-center justify-between border-b border-amber-200 pb-2 mb-2">
              <span className="text-xs font-bold text-amber-900">Contract Lifecycle Management (CLM)</span>
              <span className="text-[11px] font-mono text-amber-800">MSA-2023-V4</span>
            </div>
            <p className="text-xs text-amber-950 font-serif leading-relaxed italic bg-amber-100/50 p-2.5 rounded-lg border border-amber-200/80">
              "{evidence.contract.terms}"
            </p>
          </div>
        </div>

        {/* RIGHT COLUMN: financeIntel AI Intelligence Layer */}
        <div className="lg:col-span-6 space-y-4">
          <div className="flex items-center justify-between">
            <h3 className="text-xs font-bold uppercase tracking-wider text-slate-500">
              Autonomous Intelligence & Action Engine
            </h3>
            <span className="text-[11px] font-mono text-blue-600 font-bold">Latency: 380ms</span>
          </div>

          {/* Core Decision Badge & Exposure Summary */}
          <div className="bg-white rounded-xl border border-slate-200 p-5 shadow-sm space-y-4">
            <div className="flex items-center justify-between">
              <div>
                <span className="text-[11px] uppercase tracking-wider text-slate-400 font-semibold">Recommended Decision</span>
                <div className="mt-1">
                  <span className={`inline-flex items-center gap-1.5 px-3.5 py-1.5 rounded-lg text-xs font-black tracking-wide ${
                    isDisputed
                      ? 'bg-emerald-600 text-white'
                      : isOverridden
                      ? 'bg-purple-700 text-white'
                      : 'bg-rose-600 text-white'
                  }`}>
                    <ShieldAlert className="w-4 h-4" />
                    {isDisputed ? 'DISPUTE EXECUTED' : isOverridden ? 'CONTROLLER OVERRIDE' : 'PAYMENT HOLD RECOMMENDED'}
                  </span>
                </div>
              </div>

              <div className="text-right">
                <span className="text-[11px] uppercase tracking-wider text-slate-400 font-semibold">Financial Risk Exposure</span>
                <div className="text-2xl font-black text-rose-600 font-mono">
                  ₹{briefData.financial_exposure?.toLocaleString('en-IN', { minimumFractionDigits: 2 })}
                </div>
              </div>
            </div>

            {/* AI Verified Evidence */}
            <div className="space-y-2 border-t border-slate-100 pt-3">
              <span className="text-xs font-bold text-slate-800">Verified Evidence & Disparity Trail:</span>
              <ul className="space-y-1.5">
                {briefData.verified_evidence?.map((item: string, idx: number) => (
                  <li key={idx} className="text-xs text-slate-600 flex items-start gap-2 bg-slate-50 p-2 rounded-lg">
                    <span className="text-blue-600 font-bold text-xs mt-0.5">•</span>
                    <span>{item}</span>
                  </li>
                ))}
              </ul>
            </div>

            {/* Recommended Next Actions */}
            <div className="space-y-2 border-t border-slate-100 pt-3">
              <span className="text-xs font-bold text-slate-800">Next Recommended Protocol:</span>
              <div className="space-y-1 text-xs text-slate-600">
                {briefData.recommended_actions?.map((action: string, idx: number) => (
                  <div key={idx} className="flex items-center gap-2">
                    <ArrowRight className="w-3.5 h-3.5 text-blue-500 shrink-0" />
                    <span>{action}</span>
                  </div>
                ))}
              </div>
            </div>

            {/* Draft Communication Box */}
            <div className="border-t border-slate-100 pt-3 space-y-2">
              <div className="flex items-center justify-between">
                <span className="text-xs font-bold text-slate-800 flex items-center gap-1.5">
                  <Mail className="w-3.5 h-3.5 text-slate-500" />
                  Vendor Dispute Communication Draft
                </span>
                <span className="text-[10px] text-slate-400 font-mono">Auto-Generated</span>
              </div>
              <textarea
                value={draftMessage}
                disabled={isDisputed || isOverridden}
                onChange={(e) => setDraftMessage(e.target.value)}
                rows={5}
                className="w-full text-xs font-mono p-3 bg-slate-50 border border-slate-200 rounded-lg text-slate-800 focus:outline-none focus:ring-1 focus:ring-blue-500 disabled:opacity-75"
              />
            </div>

            {/* Action Buttons */}
            {!isDisputed && !isOverridden && (
              <div className="flex items-center justify-end gap-3 pt-2">
                <button
                  onClick={() => setShowOverrideModal(true)}
                  className="px-3.5 py-2 rounded-lg text-xs font-semibold text-slate-600 border border-slate-300 hover:bg-slate-50 transition-colors flex items-center gap-1.5"
                >
                  <Lock className="w-3.5 h-3.5 text-slate-500" />
                  <span>Manual Override...</span>
                </button>
                <button
                  onClick={handleExecuteDispute}
                  disabled={isSubmitting}
                  className="px-5 py-2 rounded-lg text-xs font-bold bg-blue-600 text-white hover:bg-blue-700 shadow-md shadow-blue-500/20 transition-all flex items-center gap-1.5"
                >
                  <Mail className="w-3.5 h-3.5" />
                  <span>Execute Dispute & Lock SAP</span>
                </button>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Manual Controller Override Modal */}
      {showOverrideModal && (
        <div className="fixed inset-0 bg-slate-950/70 backdrop-blur-sm z-50 flex items-center justify-center p-4">
          <div className="bg-white rounded-2xl max-w-lg w-full p-6 shadow-2xl space-y-4 border border-slate-200">
            <div className="flex items-center gap-3 border-b border-slate-100 pb-3">
              <div className="w-10 h-10 rounded-xl bg-purple-100 text-purple-700 flex items-center justify-center">
                <Lock className="w-5 h-5" />
              </div>
              <div>
                <h3 className="text-sm font-black text-slate-900">Authorize Manual Controller Override</h3>
                <p className="text-xs text-slate-500">SOX Compliance Level 3 Fiduciary Action</p>
              </div>
            </div>

            <div className="bg-rose-50 border border-rose-200 rounded-xl p-3 text-xs text-rose-800">
              <span className="font-bold">Warning:</span> Overriding an AI Hold releases ₹1,36,000.00 in uncontracted funds to Apex Technologies. Your credentials and justification will be logged in the permanent audit ledger.
            </div>

            <div className="space-y-3 text-xs">
              <div>
                <label className="font-bold text-slate-700 block mb-1">Override Reason Code</label>
                <select
                  value={overrideReason}
                  onChange={(e) => setOverrideReason(e.target.value)}
                  className="w-full p-2 border border-slate-200 rounded-lg bg-slate-50 focus:bg-white"
                >
                  <option value="Emergency Project Delivery">Emergency Project Delivery / Go-Live Priority</option>
                  <option value="Retrospective Addendum Pending">Retrospective CFO Pricing Addendum Pending</option>
                  <option value="Vendor Credit Note Guaranteed">Vendor Credit Note Guaranteed in Writing</option>
                </select>
              </div>

              <div>
                <label className="font-bold text-slate-700 block mb-1">Justification Narrative</label>
                <textarea
                  placeholder="Enter business justification..."
                  value={justification}
                  onChange={(e) => setJustification(e.target.value)}
                  rows={3}
                  className="w-full p-2.5 border border-slate-200 rounded-lg bg-slate-50 focus:bg-white"
                />
              </div>

              <div className="flex items-start gap-2 pt-1">
                <input
                  type="checkbox"
                  id="waiver"
                  checked={waiverSigned}
                  onChange={(e) => setWaiverSigned(e.target.checked)}
                  className="mt-0.5 rounded border-slate-300 text-blue-600 focus:ring-blue-500"
                />
                <label htmlFor="waiver" className="text-[11px] text-slate-600 leading-tight">
                  I, <span className="font-bold text-slate-900">Vikram Malhotra (Principal Controller)</span>, assume fiduciary authorization for this payment release under Delegation of Authority Schedule 4.
                </label>
              </div>
            </div>

            <div className="flex items-center justify-end gap-3 pt-3 border-t border-slate-100">
              <button
                onClick={() => setShowOverrideModal(false)}
                className="px-4 py-2 rounded-lg text-xs font-semibold text-slate-600 hover:bg-slate-100"
              >
                Cancel
              </button>
              <button
                onClick={handleAuthorizeOverride}
                disabled={!waiverSigned || isSubmitting}
                className="px-5 py-2 rounded-lg text-xs font-bold bg-purple-700 text-white hover:bg-purple-800 disabled:opacity-50"
              >
                Sign & Authorize Release
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
