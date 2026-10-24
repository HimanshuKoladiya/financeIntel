from pydantic import BaseModel
from typing import List, Dict, Any, Optional

class DisputeActionRequest(BaseModel):
    recipient_email: str
    customized_message: str

class OverrideActionRequest(BaseModel):
    controller_name: str
    reason_code: str
    justification: str
    signed_waiver: bool

class ExceptionSummary(BaseModel):
    id: str
    type: str
    severity: str
    vendor_name: str
    po_number: str
    invoice_number: str
    financial_exposure: float
    status: str

class DecisionBriefDetail(BaseModel):
    id: str
    exception_id: str
    decision_status: str
    financial_exposure: float
    ai_reasoning_text: str
    verified_evidence: List[str]
    recommended_actions: List[str]
    draft_communication: str
    audit_events: List[Dict[str, Any]]
    fragmented_evidence: Dict[str, Any]
