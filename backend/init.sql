-- financeIntel Initial Database Schema & Seed Data
CREATE TABLE IF NOT EXISTS vendors (
    id VARCHAR(64) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    contact_email VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS contracts (
    id VARCHAR(64) PRIMARY KEY,
    vendor_id VARCHAR(64) REFERENCES vendors(id),
    title VARCHAR(255) NOT NULL,
    terms_text TEXT NOT NULL,
    agreed_pricing_json JSONB NOT NULL,
    effective_date DATE NOT NULL,
    expiry_date DATE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS purchase_orders (
    id VARCHAR(64) PRIMARY KEY,
    po_number VARCHAR(64) UNIQUE NOT NULL,
    vendor_id VARCHAR(64) REFERENCES vendors(id),
    total_amount NUMERIC(14, 2) NOT NULL,
    items_json JSONB NOT NULL,
    status VARCHAR(32) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS goods_receipts (
    id VARCHAR(64) PRIMARY KEY,
    grn_number VARCHAR(64) UNIQUE NOT NULL,
    po_id VARCHAR(64) REFERENCES purchase_orders(id),
    received_items_json JSONB NOT NULL,
    received_date DATE NOT NULL,
    warehouse_location VARCHAR(128) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS invoices (
    id VARCHAR(64) PRIMARY KEY,
    invoice_number VARCHAR(64) UNIQUE NOT NULL,
    po_id VARCHAR(64) REFERENCES purchase_orders(id),
    vendor_id VARCHAR(64) REFERENCES vendors(id),
    billed_amount NUMERIC(14, 2) NOT NULL,
    billed_items_json JSONB NOT NULL,
    status VARCHAR(32) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS exception_cases (
    id VARCHAR(64) PRIMARY KEY,
    type VARCHAR(64) NOT NULL, -- PRICE_VARIANCE, QUANTITY_SHORTFALL, MISSING_GRN
    severity VARCHAR(32) NOT NULL, -- CRITICAL, HIGH, MEDIUM
    vendor_name VARCHAR(255) NOT NULL,
    po_number VARCHAR(64) NOT NULL,
    invoice_number VARCHAR(64) NOT NULL,
    financial_exposure NUMERIC(14, 2) NOT NULL,
    status VARCHAR(32) NOT NULL, -- HOLD, DISPUTED, OVERRIDDEN, RESOLVED
    related_doc_ids JSONB NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS decision_briefs (
    id VARCHAR(64) PRIMARY KEY,
    exception_id VARCHAR(64) REFERENCES exception_cases(id),
    decision_status VARCHAR(64) NOT NULL,
    financial_exposure NUMERIC(14, 2) NOT NULL,
    ai_reasoning_text TEXT NOT NULL,
    verified_evidence_json JSONB NOT NULL,
    recommended_actions_json JSONB NOT NULL,
    draft_communication TEXT NOT NULL,
    audit_events_json JSONB DEFAULT '[]'::jsonb,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Optimize queries for high-frequency analytical lookups
CREATE INDEX IF NOT EXISTS idx_po_vendor ON purchase_orders(vendor_id);
CREATE INDEX IF NOT EXISTS idx_invoice_po ON invoices(po_id);
CREATE INDEX IF NOT EXISTS idx_grn_po ON goods_receipts(po_id);
CREATE INDEX IF NOT EXISTS idx_exceptions_status ON exception_cases(status);
CREATE INDEX IF NOT EXISTS idx_invoices_items ON invoices USING gin (billed_items_json);
