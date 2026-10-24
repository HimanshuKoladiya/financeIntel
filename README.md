# financeIntel: Procure-to-Pay (P2P) Decision Intelligence Layer

`financeIntel` is a centralized intelligence layer that connects across ERPs (SAP ECC/S4HANA), Contract Lifecycle Management (CLM), Warehouse Management Systems (WMS), and OCR Invoicing pipelines. It moves beyond brittle 3-way matching by running continuous, multi-source AI reasoning to protect corporate working capital.

---

## Quickstart Deployment

### 1. Prerequisites
- Docker Engine 24+ & Docker Compose v2+
- Git

### 2. Launch the Entire Stack
```bash
git clone https://github.com/your-org/financeintel.git
cd financeintel
docker compose up --build -d
```

### 3. Service Ports & Access Points
| Service | URL | Default Credentials | Description |
| :--- | :--- | :--- | :--- |
| **financeIntel UI** | `http://localhost:3000` | N/A | Next.js Split-Screen Dashboard |
| **FastAPI REST API** | `http://localhost:8000/docs` | N/A | OpenAPI Interactive Documentation |
| **Apache Airflow** | `http://localhost:8080` | `admin` / `admin` | Data Ingestion DAG & Pipeline Monitor |
| **PostgreSQL 15** | `localhost:5432` | `finance_admin` / `secure_finance_password_2026` | Financial Transaction Database |

---

## Verifying the P2P Scenarios

### Scenario 1: The 40 Laptops Price Variance
1. Open `http://localhost:3000`.
2. Locate `#PO-2024-8841` (Apex Technologies Ltd.) in the Exception Queue.
3. Observe the **Decision Brief**:
   - **PO Line:** 40x ThinkPad T14 @ ₹68,500.
   - **Contract MSA-2023-V4:** Rate capped at ₹68,500 net.
   - **Invoice INV-99210-A:** Billed at ₹71,900 (Highlighted in pulsing Red).
   - **Quantified Exposure:** ₹1,36,000 on hold.
4. Click **"Execute Dispute & Lock SAP"**:
   - The UI immediately transitions to the **Dispute Executed State** (`2bbd55aa033d47469781ba59ac9d003a`).
   - A payment block 'R' is logged in SAP ERP with an automated audit record.

### Scenario 2: Controller Override (`58f60d300d1846648235869acc0d7649`)
1. Reset the case or select an active hold item.
2. Click **"Manual Override..."**.
3. Select an override reason, provide a narrative justification, check the SOX compliance waiver, and click **"Sign & Authorize Release"**.
4. The system logs the fiduciary decision directly into the SOX compliance ledger and releases the payment block.
