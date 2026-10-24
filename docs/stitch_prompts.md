# Google Stitch UI Design Prompts

Use the following prompts directly in **Google Stitch** (Project ID: `14706436105306456784`) or any generative design canvas to render the exact pixel-perfect enterprise interfaces.

---

### Screen 1: Executive P2P Decision Intelligence Dashboard
*Screen ID: `c697348fb5d345b394479a1770e7467f`*

```markdown
Design an ultra-clean, high-density Enterprise B2B SaaS Executive Dashboard for "financeIntel" (Procure-to-Pay Decision Intelligence Layer). 

Layout & Theme:
- Viewport: Desktop 1440x900px.
- Palette: Corporate slate gray and deep navy blue (#0B192C, #1E3E62, #001F3F), crisp pure white cards (#FFFFFF), subtle borders (#E2E8F0), slate text (#1E293B, #64748B), with vivid accent badges (Rose #EF4444, Amber #F59E0B, Emerald #10B981, Blue #2563EB).
- Typography: Inter or SF Pro Display, clean tabular numbers for currency.

Header & Navigation:
- Fixed Left Sidebar: Dark navy slate (#0F172A). Logo: financeIntel icon (hexagonal AI chip + audit checkmark). Nav items: Dashboard (active, glowing blue indicator), Exception Queue (with badge '12'), Data Sources (SAP, CLM, WMS status green), Audit Logs, System Settings.
- Top Header: Workspace breadcrumb "Enterprise Global / Finance Operations", Search bar with shortcut tag "⌘K", live synchronization badge "SAP ECC & Coupa Sync: Active (30s ago)", Notification bell with red dot, User profile "Vikram Malhotra - Principal Financial Controller".

Main Content Area:
1. Executive KPI Metrics Bar (4 summary cards):
   - "Total Flagged Exceptions": 14 Cases (+3 today).
   - "Total Financial Exposure at Risk": ₹48,92,400 (Red highlighted subtext).
   - "Automated Dispute Resolution Rate": 87.4% (+4.2% MoM).
   - "Working Capital Saved (MTD)": ₹1,12,45,000 (Emerald badge).
2. Charts & Analytics Grid (2 Columns):
   - Left (60%): Recharts-style Area & Bar Chart showing "30-Day Discrepancy Volume vs Exposure Value (₹)" highlighting Price Variances vs Quantity/GRN shortfalls.
   - Right (40%): "Risk Exposure by Vendor" Donut Chart (Apex Technologies 42%, TechCorp Solutions 28%, LogisticsGlobal 18%, Others 12%).
3. Urgent Exception Priority Feed:
   - Mini-table showing top 3 high-severity items with quick actions: "Review Decision Brief". Line 1: Apex Technologies - PO-2024-8841 (Price Variance ₹1,36,000 on 40 Laptops).
```

---

### Screen 2: Real-Time Exception Queue & Discrepancy Hub
*Screen ID: `28382024e7544a2793d390579ef12526`*

```markdown
Design an enterprise Data Grid Screen for "financeIntel - Discrepancy Queue & Match Exceptions".

Visual Structure:
- Persistent dark navy sidebar and enterprise top bar.
- Action Bar: Search input "Filter by PO#, Vendor, Invoice or SKU...", multi-select dropdown filters: Exception Type (All, Price Variance, Quantity Mismatch, Missing GRN, Unapproved Freight), Severity (Critical, High, Medium), Vendor Select, Date Range picker ("Last 7 Days"). Right-aligned: "Export Audit Ledger (CSV/PDF)" and "Run Instant Cross-Check Batch".
- Exception Data Table (High-density tabular layout):
  - Columns:
    1. Severity & Status Pill: [CRITICAL HOLD - Red]
    2. PO Number: #PO-2024-8841 (clickable link)
    3. Vendor Name: Apex Technologies Ltd.
    4. Invoice Ref: #INV-99210-A
    5. Discrepancy Type: "Unit Price > Contract MSA Rate"
    6. Exposure Amount: ₹1,36,000 (Bold red tabular figures)
    7. AI Confidence Score: 99.4% (Subtle green progress bar)
    8. Source Disparity: "PO Line 1 (₹68,500) vs Invoice Line 1 (₹71,900) × 40 units"
    9. Action: Primary blue button "Inspect Decision Brief →"
  - Line 2: [HIGH HOLD - Amber] #PO-2024-8890 | TechCorp Solutions | INV-4402 | "GRN Quantity Shortfall (30 Recv vs 50 Billed Monitors)" | ₹2,40,000 | 97.8% | "Inspect Decision Brief →"
  - Line 3: [MEDIUM - Amber] #PO-2024-8902 | Global Office Supplies | INV-1102 | "Missing Warehouse GRN Receipt" | ₹84,200 | 91.2% | "Inspect Decision Brief →"
- Bottom Pagination & Telemetry: Showing 1-10 of 14 exceptions, Average AI Resolution Latency: 420ms.
```

---

### Screen 3: Cinematic Decision Brief (40 Laptops Price Discrepancy - Active Hold State)
*Screen ID: `f455c5c9292944148a11a8e3d1a5b958`*

```markdown
Design a split-screen Cinematic Decision Brief view for financeIntel resolving an active high-stakes P2P discrepancy: "40 Enterprise Laptops - Price Override".

Top Sub-Header:
- Breadcrumbs: "Exception Queue / PO-2024-8841 / Apex Technologies".
- Banner: Urgent Warning Bar (Deep blue background with gold borders): "Cross-Document Discrepancy Detected between Master Contract MSA-2023-V4 and Vendor Invoice INV-99210-A".

Split Screen Layout (50% / 50% split):

LEFT SIDE: "Fragmented Evidence Matrix" (4 Collapsible Accordion Cards)
- Card 1: Purchase Order #PO-2024-8841 (SAP ERP)
  - Details: 40x ThinkPad T14 Gen 4 @ ₹68,500/unit | Total: ₹27,40,000. Status: Released & Approved.
- Card 2: Vendor Invoice #INV-99210-A (OCR Extracted PDF)
  - Details: 40x ThinkPad T14 Gen 4 @ [₹71,900/unit] highlighted in pulsing red box with warning tooltip | Billed Total: [₹28,76,000].
- Card 3: Goods Receipt Note #GRN-44910 (WMS Inbound)
  - Details: 40 units physically received and barcode-verified at Bangalore DC on Oct 18, 2024. Quality: Accepted.
- Card 4: Master Service Agreement #MSA-2023-V4 (Contract Lifecycle Management - CLM)
  - Clause 4.2 highlighted in yellow: "Agreed device rate fixed at ₹68,500 net through Q4 2024. No unilateral surcharge shall apply without written CFO addendum."

RIGHT SIDE: "financeIntel Autonomous Intelligence Engine"
- Decision Badge: Large bold pill [DECISION: PAYMENT HOLD RECOMMENDED] (Red background #FEE2E2, text #991B1B, shield-alert icon).
- Financial Risk Quantification Card:
  - Big metric: ₹1,36,000 Overcharge Risk
  - Calculation breakdown: (₹71,900 Billed - ₹68,500 Contracted) × 40 Units = ₹1,36,000 Net Exposure.
- Verified Cross-Evidence Reasoning (AI synthesis with citation chips):
  - Bullet 1: "Invoice unit rate exceeds Contract MSA Clause 4.2 by ₹3,400 per laptop."
  - Bullet 2: "PO correctly honors MSA price (₹68,500). Vendor accounts billing team applied non-negotiated price list."
  - Bullet 3: "Warehouse GRN confirms full physical quantity receipt (40 units). No partial delivery dispute exists."
- Recommended Action Steps:
  - 1. Freeze SAP Payment Run for Invoice #INV-99210-A.
  - 2. Issue automated debit note / revised invoice request to Apex Technologies.
- Interactive Draft Vendor Communication (Editable Rich Text Box):
  - Recipient: accounts.receivable@apextech.com | Subject: Discrepancy Notice: Invoice INV-99210-A against PO-2024-8841
  - Body: "Dear Apex Technologies Billing Team, payment on Invoice INV-99210-A is on HOLD due to a ₹3,400/unit variance against contracted pricing under MSA-2023-V4 Clause 4.2..."
- Action Buttons Bar (Bottom right):
  - [Execute Dispute & Dispatch Notice] (Vibrant Blue primary button)
  - [Manual Controller Override...] (Subtle ghost button with lock icon)
  - [Flag for Vendor Call] (White outlined button)
```

---

### Screen 4: financeIntel - Decision Brief (Dispute Executed State)
*Screen ID: `2bbd55aa033d47469781ba59ac9d003a`*

```markdown
Design the "Dispute Executed & Automated Block State" for the financeIntel Decision Brief.

Visual Changes from Hold State:
- Top Banner: Emerald green gradient banner: "DISPUTE OFFICIALLY TRANSMITTED & ERP PAYMENT BLOCKED - Case #DISP-8841-A".
- Right Side AI Intelligence Panel:
  - Decision Badge: Changed to [STATUS: DISPUTE TRANSMITTED TO VENDOR] (Teal/Emerald styling with sent checkmark).
  - Exposure Mitigated Card: "₹1,36,000 Working Capital Protected from Erroneous Payout".
  - ERP Integration Status Card (Sub-panel):
    - SAP ECC / S4HANA Status: "Payment Block 'R' (Invoice Verification) applied to Accounting Document #510009214".
    - Automated Vendor Email: "Dispatched Oct 24, 2024 at 10:52 AM via SMTP Gateway. Delivery Status: DELIVERED (Message ID: <disp-8841@financeintel.corp>)."
  - Audit Trail & Event Timeline:
    - 10:48 AM: Cross-document reasoning engine flagged ₹3,400 unit price variance.
    - 10:51 AM: Verified against Contract MSA-2023-V4 Clause 4.2.
    - 10:52 AM: Dispute executed by Controller Vikram Malhotra.
    - 10:52 AM: Vendor notified; SAP payment block active.
  - Action Controls:
    - Primary Button: [Awaiting Vendor Revised Invoice - Check Inbound OCR]
    - Secondary: [Download Complete Dispute Dossier PDF]
    - Tertiary: [Withdraw Dispute / Reset Case]
```

---

### Screen 5: financeIntel - Decision Brief (Manual Controller Override State)
*Screen ID: `58f60d300d1846648235869acc0d7649`*

```markdown
Design the "Manual Controller Override Modal & State" for the financeIntel Decision Brief.

Modal / Overlay Layer:
- High-severity warning modal dialog over the Decision Brief view.
- Header: "Authorize Manual Payment Override - Audit Level 3 Event".
- Security Warning Banner: "Overriding an AI Hold exposes the organization to ₹1,36,000 in uncontracted expenditure. This transaction will be permanently recorded in the immutable SOX compliance audit ledger."
- Form Controls:
  - Override Reason Code (Dropdown): "Emergency Project Delivery / Retrospective CFO Addendum Pending".
  - Authorizing Executive (Read-only): Vikram Malhotra (Principal Financial Controller, Employee ID: FC-9921).
  - Justification & Evidence Narrative (Mandatory Textarea with character counter 142/500): "Approved as per verbal alignment with VP of Infrastructure due to critical project go-live deadline. Vendor will issue credit memo on Q1 renewal."
  - Supporting Documentation Upload: Drag-and-drop zone with uploaded file "VP_Email_Approval_Oct24.msg" (Green checkmark).
  - Digital Signature Confirmation: Checkbox "I certify that I have reviewed the conflicting Contract MSA and assume fiduciary authorization for this ₹1,36,000 variance under Delegation of Authority (DoA) Schedule 4."
- Action Buttons:
  - [Cancel & Return to Hold] (Neutral slate button)
  - [Authorize Override & Release SAP Payment] (Dark Amber/Rose destructive-level action button with biometric/key icon).
```
