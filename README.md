# 🛡️ AEVAR: Financial Data Ingestion & Governance Pipeline

AEVAR is an enterprise-grade, rule-based data ingestion and financial governance engine engineered to process distributed corporate vendor invoices. Built with a modular, decoupled architecture, the system intercepts incoming transactions, enforces strict structural schema validation, runs data cleansing matrices, and segregates anomalies into an isolated audit quarantine.

The downstream business intelligence layer computes dynamic vendor risk profiles, isolates statistical price volatility outliers, tracks Net-30 revenue SLA aging metrics, and exposes a real-time operational dashboard with multi-format spreadsheet export capabilities.

---

## 🏗️ System Architecture & Data Flow

The pipeline is split into isolated execution zones to guarantee high data durability and clear separation of concerns:

1. **Ingestion Gate & De-duplication:** Raw data streams are ingested and run against in-memory tracking structures to catch duplicate transaction IDs before secondary execution layers fire.
2. **Schema Enforcement & Normalization:** Records pass through Pydantic boundary models. Validated transactions are cross-checked against currency lookup tables and normalized to standard USD.
3. **Quarantine Routing Desk:** Corrupted fields, bad text schemas, or logical failures are gracefully intercepted, injected with specific error metadata array stacks, and written to a non-destructive quarantine ledger.
4. **Statistical Analytics Core:** Downstream processors aggregate clean ledgers to calculate historical standard cost medians per individual vendor, tagging dynamic pricing anomalies.
5. **Operational UI Cockpit:** Streamlit visualizes historical pipeline metrics, SLA compliance, and outputs formatted dataframes with memory-encoded CSV download actions.

```text
 [ Raw JSON Ingest ] ──► [ Duplicate Filter Set ] ──► [ Pydantic Schema Guard ]
                                                              │
                                    ┌─────────────────────────┴────────────────────────┐
                                    ▼ (Pass)                                           ▼ (Fail)
                       [ Multi-Currency Normalizer ]                      [ Append Error Metadata Log ]
                                    │                                                  │
                                    ▼                                                  ▼
                       [ Verified Corporate Ledger ]                      [ Isolated Quarantine Vault ]
                                    │                                                  │
                                    ▼                                                  ▼
                     [ Analytics: Vendor Risk Profiler ]                  [ Operational Audit Desk UI ]
                                    │
                                    ▼
                      [ Interactive UI Dashboard ] ──► [ Multi-Format CSV Export Engine ]

                      
AEVAR/
├── config/
│   └── settings.py          # Operational file-system path & configuration definitions
├── data/
│   ├── raw/                 # Input landing zone for raw transaction datasets
│   ├── processed/           # Production-ready clean data warehouses & pipeline logs
│   └── quarantine/          # Isolated storage vaults for anomalous error-stamped records
├── src/
│   ├── analytics/
│   │   └── reporter.py      # Statistical median calculators & vendor risk profilers
│   ├── app/
│   │   └── dashboard.py     # Streamlit UI engine, timeline charts, & export components
│   └── ingestion/
│       ├── engine.py        # Core processing logic, duplicate gates, & normalization blocks
│       ├── mock_generator.py# High-variance mock ecosystem simulator
│       └── schemas.py       # Pydantic rigorous field boundaries & type validations
├── requirements.txt         # Production dependencies
└── README.md                # System documentation