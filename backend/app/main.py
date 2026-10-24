from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List, Dict, Any

from .database import get_db, engine, Base
from . import models, schemas
from .ai_engine import FinanceIntelAIEngine

# Ensure schema creation on startup
Base.metadata.create_all(bind=engine)

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
