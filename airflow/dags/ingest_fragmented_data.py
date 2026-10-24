from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
import requests
import json

default_args = {
    'owner': 'financeintel_data_ops',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email_on_failure': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=2),
}

def extract_and_load_fragmented_p2p_data():
    """
    Simulates extracting fragmented transactional data from:
    1. SAP ECC (Purchase Orders)
    2. Coupa / OCR Pipeline (Vendor Invoices)
    3. Manhattan WMS (Warehouse Goods Receipt Notes)
    4. Icertis / Ironclad CLM (Master Service Agreements)
    Injects data directly via backend internal database or REST mock.
    """
    import psycopg2
    from psycopg2.extras import Json

    conn = psycopg2.connect("postgresql://finance_admin:secure_finance_password_2026@postgres:5432/financeintel_db")
    cur = conn.cursor()

    # 1. Seed Vendors
    cur.execute("""
        INSERT INTO vendors (id, name, contact_email)
        VALUES 
            ('VEND-001', 'Apex Technologies Ltd.', 'accounts.receivable@apextech.com'),
            ('VEND-002', 'TechCorp Solutions Inc.', 'billing@techcorpsolutions.com')
        ON CONFLICT (id) DO NOTHING;
    """)

    # 2. Seed Master Contracts (CLM)
    cur.execute("""
        INSERT INTO contracts (id, vendor_id, title, terms_text, agreed_pricing_json, effective_date, expiry_date)
        VALUES 
            (
                'CONT-APEX-2023',
                'VEND-001',
                'Master Hardware & Infrastructure Framework Agreement MSA-2023-V4',
                'Clause 4.2: ThinkPad T14 Gen 4 enterprise units are rate-locked at ₹68,500 net per unit through Q4 2024. No inflation surcharge permitted without prior written CFO addendum.',
                %s,
                '2023-01-01',
                '2025-12-31'
            ),
            (
                'CONT-TECH-2024',
                'VEND-002',
                'Commercial Display Supply Agreement 2024',
                'Clause 2.1: 34-inch UltraWide USB-C Displays agreed at ₹12,000 per unit delivered with 3-year warranty.',
                %s,
                '2024-01-01',
                '2025-12-31'
            )
        ON CONFLICT (id) DO NOTHING;
    """, (
        Json([{"sku": "SKU-LAP-T14", "description": "ThinkPad T14 Gen 4 Laptop", "max_unit_price": 68500.00}]),
        Json([{"sku": "SKU-MON-34W", "description": "34-inch UltraWide Display Monitor", "max_unit_price": 12000.00}])
    ))

    # 3. Seed Purchase Orders (SAP ERP)
    cur.execute("""
        INSERT INTO purchase_orders (id, po_number, vendor_id, total_amount, items_json, status)
        VALUES 
            (
                'PO-8841',
                'PO-2024-8841',
                'VEND-001',
                2740000.00,
                %s,
                'APPROVED'
            ),
            (
                'PO-8890',
                'PO-2024-8890',
                'VEND-002',
                600000.00,
                %s,
                'APPROVED'
            )
        ON CONFLICT (id) DO NOTHING;
    """, (
        Json([{"sku": "SKU-LAP-T14", "description": "ThinkPad T14 Gen 4 Laptop", "quantity": 40, "unit_price": 68500.00}]),
        Json([{"sku": "SKU-MON-34W", "description": "34-inch UltraWide Display Monitor", "quantity": 50, "unit_price": 12000.00}])
    ))

    # 4. Seed Goods Receipts (WMS)
    cur.execute("""
        INSERT INTO goods_receipts (id, grn_number, po_id, received_items_json, received_date, warehouse_location)
        VALUES 
            (
                'GRN-44910',
                'GRN-44910',
                'PO-8841',
                %s,
                '2024-10-18',
                'Bangalore Central Logistics Hub (DC-02)'
            ),
            (
                'GRN-44988',
                'GRN-44988',
                'PO-8890',
                %s,
                '2024-10-20',
                'Mumbai Primary Depot (DC-01)'
            )
        ON CONFLICT (id) DO NOTHING;
    """, (
        # 40 laptops received in full
        Json([{"sku": "SKU-LAP-T14", "description": "ThinkPad T14 Gen 4 Laptop", "received_quantity": 40}]),
        # Only 30 monitors physically received out of 50 billed!
        Json([{"sku": "SKU-MON-34W", "description": "34-inch UltraWide Display Monitor", "received_quantity": 30}])
    ))

    # 5. Seed Discrepant Invoices
    cur.execute("""
        INSERT INTO invoices (id, invoice_number, po_id, vendor_id, billed_amount, billed_items_json, status)
        VALUES 
            (
                'INV-99210',
                'INV-99210-A',
                'PO-8841',
                'VEND-001',
                2876000.00,
                %s,
                'RECEIVED'
            ),
            (
                'INV-4402',
                'INV-4402',
                'PO-8890',
                'VEND-002',
                600000.00,
                %s,
                'RECEIVED'
            )
        ON CONFLICT (id) DO NOTHING;
    """, (
        # Invoiced at ₹71,900 instead of contracted ₹68,500!
        Json([{"sku": "SKU-LAP-T14", "description": "ThinkPad T14 Gen 4 Laptop", "quantity": 40, "unit_price": 71900.00}]),
        # Invoiced for 50 units while only 30 received!
        Json([{"sku": "SKU-MON-34W", "description": "34-inch UltraWide Display Monitor", "quantity": 50, "unit_price": 12000.00}])
    ))

    # 6. Generate Exception Cases & Decision Briefs
    # Case A: 40 Laptops Price Variance (₹1,36,000 Exposure)
    cur.execute("""
        INSERT INTO exception_cases (
            id, type, severity, vendor_name, po_number, invoice_number, financial_exposure, status, related_doc_ids
        )
        VALUES (
            'EXC-8841',
            'PRICE_VARIANCE',
            'CRITICAL',
            'Apex Technologies Ltd.',
            'PO-2024-8841',
            'INV-99210-A',
            136000.00,
            'HOLD',
            %s
        )
        ON CONFLICT (id) DO NOTHING;
    """, (
        Json({
            "po_id": "PO-8841",
            "invoice_id": "INV-99210",
            "grn_id": "GRN-44910",
            "contract_id": "CONT-APEX-2023"
        }),
    ))

    cur.execute("""
        INSERT INTO decision_briefs (
            id, exception_id, decision_status, financial_exposure, ai_reasoning_text,
            verified_evidence_json, recommended_actions_json, draft_communication, audit_events_json
        )
        VALUES (
            'BRIEF-8841',
            'EXC-8841',
            'HOLD',
            136000.00,
            'Cross-Document AI Reasoning detected an unauthorized unit price variance. Invoiced rate exceeds Contract MSA Clause 4.2 by ₹3,400 per laptop across 40 units.',
            %s,
            %s,
            %s,
            %s
        )
        ON CONFLICT (id) DO NOTHING;
    """, (
        Json([
            "Invoice INV-99210-A bills 40 units of 'ThinkPad T14 Gen 4' at ₹71,900.00/unit.",
            "Master Contract MSA-2023-V4 Clause 4.2 explicitly limits price to ₹68,500.00 net through Q4 2024.",
            "PO-2024-8841 matches contract price (₹68,500). Variance originates solely on vendor billing line.",
            "WMS GRN-44910 confirms full delivery receipt of 40 units in good order."
        ]),
        Json([
            "Apply immediate SAP ERP Payment Block 'R' on Invoice #INV-99210-A.",
            "Issue Discrepancy Notice & Request amended invoice or ₹1,36,000 credit memo."
        ]),
        (
            "To: accounts.receivable@apextech.com\n"
            "Subject: PAYMENT HOLD: Invoice INV-99210-A against PO-2024-8841 (Price Variance)\n\n"
            "Dear Apex Technologies Billing Team,\n\n"
            "Payment for Invoice INV-99210-A has been placed on HOLD due to a ₹3,400/unit price variance.\n"
            "Under MSA-2023-V4 Clause 4.2, the agreed price is ₹68,500.00 for 40 units of ThinkPad T14 Gen 4, whereas "
            "₹71,900.00 was billed, creating an uncontracted variance of ₹1,36,000.00.\n\n"
            "Please provide an amended invoice or credit note to release payment."
        ),
        Json([
            {"timestamp": "2024-10-24 09:15:00 UTC", "action": "INSPECTION_COMPLETED", "actor": "financeIntel AI Agent", "details": "4-Way match discrepancy flagged"}
        ])
    ))

    # Case B: 20 Monitors Quantity Shortfall (₹2,40,000 Exposure)
    cur.execute("""
        INSERT INTO exception_cases (
            id, type, severity, vendor_name, po_number, invoice_number, financial_exposure, status, related_doc_ids
        )
        VALUES (
            'EXC-8890',
            'QUANTITY_SHORTFALL',
            'HIGH',
            'TechCorp Solutions Inc.',
            'PO-2024-8890',
            'INV-4402',
            240000.00,
            'HOLD',
            %s
        )
        ON CONFLICT (id) DO NOTHING;
    """, (
        Json({
            "po_id": "PO-8890",
            "invoice_id": "INV-4402",
            "grn_id": "GRN-44988",
            "contract_id": "CONT-TECH-2024"
        }),
    ))

    cur.execute("""
        INSERT INTO decision_briefs (
            id, exception_id, decision_status, financial_exposure, ai_reasoning_text,
            verified_evidence_json, recommended_actions_json, draft_communication, audit_events_json
        )
        VALUES (
            'BRIEF-8890',
            'EXC-8890',
            'HOLD',
            240000.00,
            'Physical goods receipt shortfall detected: Invoice bills for 50 monitors while WMS GRN confirms physical receipt of only 30 units (20 missing units).',
            %s,
            %s,
            %s,
            %s
        )
        ON CONFLICT (id) DO NOTHING;
    """, (
        Json([
            "Invoice INV-4402 bills for 50x '34-inch UltraWide Display Monitor' @ ₹12,000.00 = ₹6,00,000.",
            "WMS GRN-44988 at Mumbai Depot DC-01 registers physical dock intake of only 30 units.",
            "Unreconciled physical variance: 20 units missing from warehouse receiving logs."
        ]),
        Json([
            "Withhold ₹2,40,000.00 from Invoice #INV-4402.",
            "Release partial payment for 30 verified units (₹3,60,000.00) or hold pending second delivery manifest."
        ]),
        (
            "To: billing@techcorpsolutions.com\n"
            "Subject: Quantity Shortfall Notice: Invoice INV-4402 against PO-2024-8890\n\n"
            "Dear Billing Team,\n\n"
            "WMS receiving confirms only 30 of the 50 billed 34-inch UltraWide monitors have been received at our Mumbai Depot. "
            "Payment for the 20 unreceived units (₹2,40,000.00) has been withheld."
        ),
        Json([])
    ))

    conn.commit()
    cur.close()
    conn.close()

with DAG(
    'financeintel_fragmented_ingestion',
    default_args=default_args,
    description='Nightly ingestion and cross-system synthesis from ERP, WMS, CLM into financeIntel',
    schedule_interval='@hourly',
    catchup=False,
) as dag:

    ingest_task = PythonOperator(
        task_id='ingest_and_run_cross_reasoning',
        python_callable=extract_and_load_fragmented_p2p_data,
    )
