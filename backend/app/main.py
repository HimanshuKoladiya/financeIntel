from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List, Dict, Any

from .database import get_db, engine, Base
from . import models, schemas
from .ai_engine import FinanceIntelAIEngine

from datetime import date

# Ensure schema creation on startup
Base.metadata.create_all(bind=engine)

def seed_initial_data():
    from .database import SessionLocal
    db = SessionLocal()
    try:
        if db.query(models.ExceptionCase).count() == 0:
            # Seed Vendors
            v1 = models.Vendor(id="VEND-001", name="Apex Technologies Ltd.", contact_email="accounts.receivable@apextech.com")
            v2 = models.Vendor(id="VEND-002", name="TechCorp Solutions Inc.", contact_email="billing@techcorpsolutions.com")
            db.add_all([v1, v2])

            # Seed Contracts
            c1 = models.Contract(
                id="CONT-APEX-2023",
                vendor_id="VEND-001",
                title="Master Hardware & Infrastructure Framework Agreement MSA-2023-V4",
                terms_text="Clause 4.2: ThinkPad T14 Gen 4 enterprise units are rate-locked at ₹68,500 net per unit through Q4 2024. No inflation surcharge permitted without prior written CFO addendum.",
                agreed_pricing_json=[{"sku": "SKU-LAP-T14", "description": "ThinkPad T14 Gen 4 Laptop", "max_unit_price": 68500.00}],
                effective_date=date(2023, 1, 1),
                expiry_date=date(2025, 12, 31)
            )
            c2 = models.Contract(
                id="CONT-TECH-2024",
                vendor_id="VEND-002",
                title="Commercial Display Supply Agreement 2024",
                terms_text="Clause 2.1: 34-inch UltraWide USB-C Displays agreed at ₹12,000 per unit delivered with 3-year warranty.",
                agreed_pricing_json=[{"sku": "SKU-MON-34W", "description": "34-inch UltraWide Display Monitor", "max_unit_price": 12000.00}],
                effective_date=date(2024, 1, 1),
                expiry_date=date(2025, 12, 31)
            )
            db.add_all([c1, c2])

            # Seed POs
            po1 = models.PurchaseOrder(
                id="PO-8841",
                po_number="PO-2024-8841",
                vendor_id="VEND-001",
                total_amount=2740000.00,
                items_json=[{"sku": "SKU-LAP-T14", "description": "ThinkPad T14 Gen 4 Laptop", "quantity": 40, "unit_price": 68500.00}],
                status="APPROVED"
            )
            po2 = models.PurchaseOrder(
                id="PO-8890",
                po_number="PO-2024-8890",
                vendor_id="VEND-002",
                total_amount=600000.00,
                items_json=[{"sku": "SKU-MON-34W", "description": "34-inch UltraWide Display Monitor", "quantity": 50, "unit_price": 12000.00}],
                status="APPROVED"
            )
            db.add_all([po1, po2])

            # Seed Goods Receipts
            grn1 = models.GoodsReceipt(
                id="GRN-44910",
                grn_number="GRN-44910",
                po_id="PO-8841",
                received_items_json=[{"sku": "SKU-LAP-T14", "description": "ThinkPad T14 Gen 4 Laptop", "received_quantity": 40}],
                received_date=date(2024, 10, 18),
                warehouse_location="Bangalore Central Logistics Hub (DC-02)"
            )
            grn2 = models.GoodsReceipt(
                id="GRN-44988",
                grn_number="GRN-44988",
                po_id="PO-8890",
                received_items_json=[{"sku": "SKU-MON-34W", "description": "34-inch UltraWide Display Monitor", "received_quantity": 30}],
                received_date=date(2024, 10, 20),
                warehouse_location="Mumbai Primary Depot (DC-01)"
            )
            db.add_all([grn1, grn2])

            # Seed Invoices
            inv1 = models.Invoice(
                id="INV-99210",
                invoice_number="INV-99210-A",
                po_id="PO-8841",
                vendor_id="VEND-001",
                billed_amount=2876000.00,
                billed_items_json=[{"sku": "SKU-LAP-T14", "description": "ThinkPad T14 Gen 4 Laptop", "quantity": 40, "unit_price": 71900.00}],
                status="RECEIVED"
            )
            inv2 = models.Invoice(
                id="INV-4402",
                invoice_number="INV-4402",
                po_id="PO-8890",
                vendor_id="VEND-002",
                billed_amount=600000.00,
                billed_items_json=[{"sku": "SKU-MON-34W", "description": "34-inch UltraWide Display Monitor", "quantity": 50, "unit_price": 12000.00}],
                status="RECEIVED"
            )
            db.add_all([inv1, inv2])

            # Seed Exception Cases
            exc1 = models.ExceptionCase(
                id="EXC-8841",
                type="PRICE_VARIANCE",
                severity="CRITICAL",
                vendor_name="Apex Technologies Ltd.",
                po_number="PO-2024-8841",
                invoice_number="INV-99210-A",
                financial_exposure=136000.00,
                status="HOLD",
                related_doc_ids={"po_id": "PO-8841", "invoice_id": "INV-99210", "grn_id": "GRN-44910", "contract_id": "CONT-APEX-2023"}
            )
            exc2 = models.ExceptionCase(
                id="EXC-8890",
                type="QUANTITY_SHORTFALL",
                severity="HIGH",
                vendor_name="TechCorp Solutions Inc.",
                po_number="PO-2024-8890",
                invoice_number="INV-4402",
                financial_exposure=240000.00,
                status="HOLD",
                related_doc_ids={"po_id": "PO-8890", "invoice_id": "INV-4402", "grn_id": "GRN-44988", "contract_id": "CONT-TECH-2024"}
            )
            db.add_all([exc1, exc2])

            # Seed Decision Briefs
            brief1 = models.DecisionBrief(
                id="BRIEF-8841",
                exception_id="EXC-8841",
                decision_status="HOLD",
                financial_exposure=136000.00,
                ai_reasoning_text="Cross-Document AI Reasoning detected an unauthorized unit price variance. Invoiced rate exceeds Contract MSA Clause 4.2 by ₹3,400 per laptop across 40 units.",
                verified_evidence_json=[
                    "Invoice INV-99210-A bills 40 units of 'ThinkPad T14 Gen 4' at ₹71,900.00/unit.",
                    "Master Contract MSA-2023-V4 Clause 4.2 explicitly limits price to ₹68,500.00 net through Q4 2024.",
                    "PO-2024-8841 matches contract price (₹68,500). Variance originates solely on vendor billing line.",
                    "WMS GRN-44910 confirms full delivery receipt of 40 units in good order."
                ],
                recommended_actions_json=[
                    "Apply immediate SAP ERP Payment Block 'R' on Invoice #INV-99210-A.",
                    "Issue Discrepancy Notice & Request amended invoice or ₹1,36,000 credit memo."
                ],
                draft_communication=(
                    "To: accounts.receivable@apextech.com\n"
                    "Subject: PAYMENT HOLD: Invoice INV-99210-A against PO-2024-8841 (Price Variance)\n\n"
                    "Dear Apex Technologies Billing Team,\n\n"
                    "Payment for Invoice INV-99210-A has been placed on HOLD due to a ₹3,400/unit price variance.\n"
                    "Under MSA-2023-V4 Clause 4.2, the agreed price is ₹68,500.00 for 40 units of ThinkPad T14 Gen 4, whereas "
                    "₹71,900.00 was billed, creating an uncontracted variance of ₹1,36,000.00.\n\n"
                    "Please provide an amended invoice or credit note to release payment."
                ),
                audit_events_json=[
                    {"timestamp": "2024-10-24 09:15:00 UTC", "action": "INSPECTION_COMPLETED", "actor": "financeIntel AI Agent", "details": "4-Way match discrepancy flagged"}
                ]
            )
            brief2 = models.DecisionBrief(
                id="BRIEF-8890",
                exception_id="EXC-8890",
                decision_status="HOLD",
                financial_exposure=240000.00,
                ai_reasoning_text="Physical goods receipt shortfall detected: Invoice bills for 50 monitors while WMS GRN confirms physical receipt of only 30 units (20 missing units).",
                verified_evidence_json=[
                    "Invoice INV-4402 bills for 50x '34-inch UltraWide Display Monitor' @ ₹12,000.00 = ₹6,00,000.",
                    "WMS GRN-44988 at Mumbai Depot DC-01 registers physical dock intake of only 30 units.",
                    "Unreconciled physical variance: 20 units missing from warehouse receiving logs."
                ],
                recommended_actions_json=[
                    "Withhold ₹2,40,000.00 from Invoice #INV-4402.",
                    "Release partial payment for 30 verified units (₹3,60,000.00) or hold pending second delivery manifest."
                ],
                draft_communication=(
                    "To: billing@techcorpsolutions.com\n"
                    "Subject: Quantity Shortfall Notice: Invoice INV-4402 against PO-2024-8890\n\n"
                    "Dear Billing Team,\n\n"
                    "WMS receiving confirms only 30 of the 50 billed 34-inch UltraWide monitors have been received at our Mumbai Depot. "
                    "Payment for the 20 unreceived units (₹2,40,000.00) has been withheld."
                ),
                audit_events_json=[]
            )
            db.add_all([brief1, brief2])
            db.commit()
    except Exception as err:
        db.rollback()
        print("Warning during seed:", err)
    finally:
        db.close()

seed_initial_data()


app = FastAPI(
    title="financeIntel Intelligence Layer API",
    description="Enterprise Decision Intelligence Platform for Procure-to-Pay (P2P) Discrepancies",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status": "healthy", "layer": "financeIntel-v2"}

@app.get("/api/dashboard/metrics")
def get_dashboard_metrics(db: Session = Depends(get_db)):
    exceptions = db.query(models.ExceptionCase).all()
    pending = [e for e in exceptions if e.status in ["HOLD", "DISPUTED"]]
    total_exposure = sum([float(e.financial_exposure) for e in pending])
    
    return {
        "pending_exceptions_count": len(pending),
        "total_exposure_on_hold": total_exposure,
        "automated_dispute_rate": 88.5,
        "working_capital_protected": 11245000.00,
        "recent_activity": [
            {"time": "10:48 AM", "event": "Cross-Document Reasoning flagged PO-2024-8841 (Price Variance)", "type": "ALERT"},
            {"time": "09:30 AM", "event": "Dispute #DISP-8820 accepted by LogisticsGlobal - Credit Note issued", "type": "SUCCESS"},
            {"time": "Yesterday", "event": "Controller Override executed on PO-2024-8790 by VP Finance", "type": "INFO"}
        ]
    }

@app.get("/api/exceptions", response_model=List[schemas.ExceptionSummary])
def list_exceptions(db: Session = Depends(get_db)):
    records = db.query(models.ExceptionCase).order_by(models.ExceptionCase.created_at.desc()).all()
    return [
        schemas.ExceptionSummary(
            id=r.id,
            type=r.type,
            severity=r.severity,
            vendor_name=r.vendor_name,
            po_number=r.po_number,
            invoice_number=r.invoice_number,
            financial_exposure=float(r.financial_exposure),
            status=r.status
        )
        for r in records
    ]

@app.get("/api/decision-brief/{exception_id}", response_model=schemas.DecisionBriefDetail)
def get_decision_brief(exception_id: str, db: Session = Depends(get_db)):
    exc = db.query(models.ExceptionCase).filter(models.ExceptionCase.id == exception_id).first()
    if not exc:
        raise HTTPException(status_code=404, detail="Exception record not found")

    brief = db.query(models.DecisionBrief).filter(models.DecisionBrief.exception_id == exception_id).first()
    if not brief:
        raise HTTPException(status_code=404, detail="Decision brief not generated yet")

    # Fetch fragmented documentation context
    doc_ids = exc.related_doc_ids or {}
    po = db.query(models.PurchaseOrder).filter(models.PurchaseOrder.id == doc_ids.get("po_id")).first()
    inv = db.query(models.Invoice).filter(models.Invoice.id == doc_ids.get("invoice_id")).first()
    grn = db.query(models.GoodsReceipt).filter(models.GoodsReceipt.id == doc_ids.get("grn_id")).first()
    contract = db.query(models.Contract).filter(models.Contract.id == doc_ids.get("contract_id")).first()

    evidence_matrix = {
        "purchase_order": {
            "po_number": po.po_number if po else "N/A",
            "total_amount": float(po.total_amount) if po else 0.0,
            "items": po.items_json if po else []
        },
        "invoice": {
            "invoice_number": inv.invoice_number if inv else "N/A",
            "billed_amount": float(inv.billed_amount) if inv else 0.0,
            "items": inv.billed_items_json if inv else []
        },
        "goods_receipt": {
            "grn_number": grn.grn_number if grn else "N/A",
            "received_date": str(grn.received_date) if grn else "N/A",
            "location": grn.warehouse_location if grn else "N/A",
            "items": grn.received_items_json if grn else []
        },
        "contract": {
            "title": contract.title if contract else "N/A",
            "terms": contract.terms_text if contract else "N/A",
            "pricing": contract.agreed_pricing_json if contract else []
        }
    }

    return schemas.DecisionBriefDetail(
        id=brief.id,
        exception_id=exc.id,
        decision_status=brief.decision_status,
        financial_exposure=float(brief.financial_exposure),
        ai_reasoning_text=brief.ai_reasoning_text,
        verified_evidence=brief.verified_evidence_json or [],
        recommended_actions=brief.recommended_actions_json or [],
        draft_communication=brief.draft_communication,
        audit_events=brief.audit_events_json or [],
        fragmented_evidence=evidence_matrix
    )

@app.post("/api/decision-brief/{exception_id}/execute-dispute")
def execute_dispute(
    exception_id: str,
    payload: schemas.DisputeActionRequest,
    db: Session = Depends(get_db)
):
    exc = db.query(models.ExceptionCase).filter(models.ExceptionCase.id == exception_id).first()
    brief = db.query(models.DecisionBrief).filter(models.DecisionBrief.exception_id == exception_id).first()
    if not exc or not brief:
        raise HTTPException(status_code=404, detail="Entity not found")

    exc.status = "DISPUTED"
    brief.decision_status = "DISPUTE_EXECUTED"
    brief.draft_communication = payload.customized_message
    
    events = list(brief.audit_events_json or [])
    events.append({
        "timestamp": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC"),
        "action": "DISPUTE_DISPATCHED",
        "actor": "Autonomous P2P Agent / Controller Approval",
        "details": f"Dispatched email to {payload.recipient_email}; Applied Payment Block 'R' in SAP ERP."
    })
    brief.audit_events_json = events

    db.commit()
    return {"status": "SUCCESS", "message": "Dispute executed and SAP payment block active"}

@app.post("/api/decision-brief/{exception_id}/override")
def controller_override(
    exception_id: str,
    payload: schemas.OverrideActionRequest,
    db: Session = Depends(get_db)
):
    if not payload.signed_waiver:
        raise HTTPException(status_code=400, detail="Digital fiduciary waiver signature is mandatory.")

    exc = db.query(models.ExceptionCase).filter(models.ExceptionCase.id == exception_id).first()
    brief = db.query(models.DecisionBrief).filter(models.DecisionBrief.exception_id == exception_id).first()
    if not exc or not brief:
        raise HTTPException(status_code=404, detail="Entity not found")

    exc.status = "OVERRIDDEN"
    brief.decision_status = "MANUAL_OVERRIDE_APPROVED"

    events = list(brief.audit_events_json or [])
    events.append({
        "timestamp": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC"),
        "action": "CONTROLLER_OVERRIDE_EXECUTED",
        "actor": payload.controller_name,
        "details": f"Reason: {payload.reason_code} | Justification: {payload.justification}"
    })
    brief.audit_events_json = events

    db.commit()
    return {"status": "SUCCESS", "message": "Manual override recorded in compliance ledger"}
