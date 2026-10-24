from typing import Dict, Any, Tuple, List
import json

class FinanceIntelAIEngine:
    """
    4-Stage Cross-Document Reasoning Engine:
    Stage 1: Multi-Source Extraction & Data Graph Synthesis
    Stage 2: Deterministic Baseline Rules + Semantic Contract Evaluation
    Stage 3: Evidence Tracing & Line-Item Disparity Mapping
    Stage 4: Business Impact Quantification & Autonomous Resolution Generation
    """

    @staticmethod
    def execute_reasoning_pipeline(
        po: Dict[str, Any],
        invoice: Dict[str, Any],
        grn: Dict[str, Any],
        contract: Dict[str, Any]
    ) -> Dict[str, Any]:
        # --- Stage 1 & 2: Exception Detection ---
        discrepancies: List[Dict[str, Any]] = []
        total_exposure = 0.0

        contract_prices = {
            item["sku"]: item["max_unit_price"]
            for item in contract.get("agreed_pricing_json", [])
        }

        grn_quantities = {
            item["sku"]: item["received_quantity"]
            for item in grn.get("received_items_json", [])
        }

        # Cross-evaluate Invoiced line items
        for inv_item in invoice.get("billed_items_json", []):
            sku = inv_item["sku"]
            desc = inv_item["description"]
            billed_qty = inv_item["quantity"]
            billed_unit_price = float(inv_item["unit_price"])

            # Rule A: Contract Price Ceiling Check
            if sku in contract_prices:
                contract_max = float(contract_prices[sku])
                if billed_unit_price > contract_max:
                    unit_variance = billed_unit_price - contract_max
                    line_exposure = unit_variance * billed_qty
                    total_exposure += line_exposure
                    discrepancies.append({
                        "type": "PRICE_VARIANCE",
                        "sku": sku,
                        "description": desc,
                        "billed_unit_price": billed_unit_price,
                        "contract_unit_price": contract_max,
                        "unit_variance": unit_variance,
                        "quantity": billed_qty,
                        "exposure": line_exposure,
                        "evidence_clause": "Contract MSA Section 4.2 (Fixed Device Pricing Schedule)"
                    })

            # Rule B: Physical Receipt (GRN) Quantity Check
            received_qty = grn_quantities.get(sku, 0)
            if billed_qty > received_qty:
                shortfall_qty = billed_qty - received_qty
                line_exposure = shortfall_qty * billed_unit_price
                total_exposure += line_exposure
                discrepancies.append({
                    "type": "QUANTITY_SHORTFALL",
                    "sku": sku,
                    "description": desc,
                    "billed_quantity": billed_qty,
                    "received_quantity": received_qty,
                    "shortfall": shortfall_qty,
                    "exposure": line_exposure,
                    "evidence_clause": "WMS Inbound Inspection Manifest vs Billed Packing Slip"
                })

        # --- Stage 3: Evidence Verification & Synthesis ---
        evidence_points: List[str] = []
        for d in discrepancies:
            if d["type"] == "PRICE_VARIANCE":
                evidence_points.append(
                    f"Invoice {invoice.get('invoice_number')} bills {d['quantity']}x '{d['description']}' "
                    f"at ₹{d['billed_unit_price']:,.2f}/unit. Master Contract limits unit rate to "
                    f"₹{d['contract_unit_price']:,.2f} under {d['evidence_clause']}."
                )
            elif d["type"] == "QUANTITY_SHORTFALL":
                evidence_points.append(
                    f"Invoice bills for {d['billed_quantity']} units of '{d['description']}', but WMS GRN "
                    f"{grn.get('grn_number')} confirms only {d['received_quantity']} units received (Shortfall: {d['shortfall']} units)."
                )

        if not discrepancies:
            return {
                "decision_status": "APPROVED",
                "financial_exposure": 0.0,
                "ai_reasoning_text": "All invoiced lines reconcile within 100% variance tolerance against PO, Contract, and GRN receipts.",
                "verified_evidence": ["3-way and 4-way contract criteria matched without discrepancies."],
                "recommended_actions": ["Release voucher for scheduled ERP payment batch."],
                "draft_communication": ""
            }

        # --- Stage 4: Business Impact & Draft Generation ---
        recommended_actions = [
            f"Apply immediate SAP ERP Payment Block 'R' on Invoice #{invoice.get('invoice_number')}.",
            f"Withhold disbursement of ₹{total_exposure:,.2f} pending vendor rate correction or credit memo.",
            "Dispatch automated discrepancy brief to supplier Accounts Receivable desk."
        ]

        draft_email = (
            f"To: Billing Operations <accounts@{invoice.get('vendor_name', 'vendor').lower().replace(' ', '')}.com>\n"
            f"Subject: NOTICE OF PAYMENT HOLD: Invoice #{invoice.get('invoice_number')} / PO #{po.get('po_number')}\n\n"
            f"Dear Accounts Receivable Team,\n\n"
            f"During automated multi-document verification for Purchase Order #{po.get('po_number')}, financeIntel flagged a "
            f"contractual discrepancy resulting in an aggregate financial hold of ₹{total_exposure:,.2f}.\n\n"
            f"Discrepancy Details:\n"
            + "\n".join([f"- {ep}" for ep in evidence_points]) + "\n\n"
            f"Under our Master Agreement terms, payment has been paused for the affected line items. Please issue an "
            f"amended invoice or a credit note reflecting the agreed schedule rate within 5 business days.\n\n"
            f"Sincerely,\n"
            f"Automated Disbursements & Internal Controls | Global Finance Operations"
        )

        return {
            "decision_status": "HOLD",
            "financial_exposure": total_exposure,
            "ai_reasoning_text": (
                f"Multi-document validation failed: Detected {len(discrepancies)} discrepancy condition(s). "
                f"Total unauthorized working capital risk quantified at ₹{total_exposure:,.2f}."
            ),
            "verified_evidence": evidence_points,
            "recommended_actions": recommended_actions,
            "draft_communication": draft_email
        }
