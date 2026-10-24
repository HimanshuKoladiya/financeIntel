from datetime import datetime
from sqlalchemy import Column, String, Numeric, Text, Date, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from .database import Base

class Vendor(Base):
    __tablename__ = "vendors"
    id = Column(String(64), primary_key=True)
    name = Column(String(255), nullable=False)
    contact_email = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class Contract(Base):
    __tablename__ = "contracts"
    id = Column(String(64), primary_key=True)
    vendor_id = Column(String(64), ForeignKey("vendors.id"))
    title = Column(String(255), nullable=False)
    terms_text = Column(Text, nullable=False)
    agreed_pricing_json = Column(JSONB, nullable=False)
    effective_date = Column(Date, nullable=False)
    expiry_date = Column(Date, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class PurchaseOrder(Base):
    __tablename__ = "purchase_orders"
    id = Column(String(64), primary_key=True)
    po_number = Column(String(64), unique=True, nullable=False)
    vendor_id = Column(String(64), ForeignKey("vendors.id"))
    total_amount = Column(Numeric(14, 2), nullable=False)
    items_json = Column(JSONB, nullable=False)
    status = Column(String(32), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class GoodsReceipt(Base):
    __tablename__ = "goods_receipts"
    id = Column(String(64), primary_key=True)
    grn_number = Column(String(64), unique=True, nullable=False)
    po_id = Column(String(64), ForeignKey("purchase_orders.id"))
    received_items_json = Column(JSONB, nullable=False)
    received_date = Column(Date, nullable=False)
    warehouse_location = Column(String(128), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class Invoice(Base):
    __tablename__ = "invoices"
    id = Column(String(64), primary_key=True)
    invoice_number = Column(String(64), unique=True, nullable=False)
    po_id = Column(String(64), ForeignKey("purchase_orders.id"))
    vendor_id = Column(String(64), ForeignKey("vendors.id"))
    billed_amount = Column(Numeric(14, 2), nullable=False)
    billed_items_json = Column(JSONB, nullable=False)
    status = Column(String(32), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class ExceptionCase(Base):
    __tablename__ = "exception_cases"
    id = Column(String(64), primary_key=True)
    type = Column(String(64), nullable=False)
    severity = Column(String(32), nullable=False)
    vendor_name = Column(String(255), nullable=False)
    po_number = Column(String(64), nullable=False)
    invoice_number = Column(String(64), nullable=False)
    financial_exposure = Column(Numeric(14, 2), nullable=False)
    status = Column(String(32), nullable=False)
    related_doc_ids = Column(JSONB, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    brief = relationship("DecisionBrief", back_populates="exception_case", uselist=False)

class DecisionBrief(Base):
    __tablename__ = "decision_briefs"
    id = Column(String(64), primary_key=True)
    exception_id = Column(String(64), ForeignKey("exception_cases.id"))
    decision_status = Column(String(64), nullable=False)
    financial_exposure = Column(Numeric(14, 2), nullable=False)
    ai_reasoning_text = Column(Text, nullable=False)
    verified_evidence_json = Column(JSONB, nullable=False)
    recommended_actions_json = Column(JSONB, nullable=False)
    draft_communication = Column(Text, nullable=False)
    audit_events_json = Column(JSONB, default=list)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    exception_case = relationship("ExceptionCase", back_populates="brief")
