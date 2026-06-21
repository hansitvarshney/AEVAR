# 🛡️ AEVAR: Financial Data Ingestion & Governance Pipeline

AEVAR is an enterprise-grade, rule-based data ingestion and financial governance engine engineered to process distributed corporate vendor invoices. Built with a modular, decoupled architecture, the system intercepts incoming transactions, enforces strict structural schema validation, runs data cleansing matrices, and segregates anomalies into an isolated audit quarantine.

The downstream business intelligence layer computes dynamic vendor risk profiles, isolates statistical price volatility outliers, tracks Net-30 revenue SLA aging metrics, and exposes a real-time operational dashboard with multi-format spreadsheet export capabilities.

---

## System Architecture & Data Flow

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

Deep Dive: Core Enterprise Features
•	1. High-Performance Duplicate Prevention: Intercepts identical vendor submissions on the fly using a high-velocity lookup hash-set, shielding downstream accounting engines from payment errors.
•	2. Cross-Border Currency Normalization: Dynamically reads international currency types (EUR, INR), standardizes values using standard algorithmic lookups, and stores uniform financial records in USD.
•	3. Automated System Audit Logger: Persists a historical execution snapshot array tracking system performance trends, logging successful items vs. quarantined anomalies over rolling cycles.
•	4. Predictive Vendor Risk Profiling: Implements a multi-pass analytical execution pattern calculating standard median operational parameters per vendor, isolating transactional outliers spiking ‭$> 2\times$‬‭‬ past historical baselines.
•	5. Accounts Payable SLA Clocks: Runs date arithmetic over invoice timestamps to track corporate cash exposures, warning operators of items approaching or exceeding Net-30 fulfillment parameters.
•	6. Multi-Format Structural Data Exports: Encodes runtime memory dataframes into standard downloadable CSV spreadsheets, allowing non-technical finance operators to cleanly export transaction summaries.

Project Workspace Topology                  
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

⚡ Quickstart & Deployment
1. Environment Initialization
Ensure you are running Python 3.10+ within a virtual workspace environment:
# Initialize and source environment layout
python3 -m venv venv
source venv/bin/activate

# Install required package dependencies
pip install -r requirements.txt
2. Run the Data Pipeline Simulation Cycle
Execute the data lifecycle pipeline phases sequentially from the root project directory:
# Phase A: Seed the landing zone with simulated transaction datasets
PYTHONPATH=. python -m src.ingestion.mock_generator

# Phase B: Fire the primary core ingestion, de-duplication, and validation engines
PYTHONPATH=. python -m src.ingestion.engine
3. Launch the Operational Governance UI
Boot the real-time financial tracking dashboard panel:
streamlit run src/app/dashboard.py


Production Engineering Controls
•	Defensive Failure Isolation: Valid transactions continue through the pipeline uninterrupted even if adjacent rows in the data block are heavily corrupted or structurally deformed.
•	Graceful Crash Mitigation: Missing configuration paths or missing raw files trigger detailed terminal errors instead of executing unsafe operations.
•	Metadata Rich Audits: Quarantined items keep their entire original payload alongside clear descriptions of why they failed, providing a clean audit trail.