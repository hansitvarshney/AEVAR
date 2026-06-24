Markdown
# 🛡️ AEVAR: Autonomous Financial Governance & GraphRAG Audit Pipeline

AEVAR is an enterprise-grade financial data ingestion, governance, and autonomous risk mitigation engine. The platform is engineered to ingest high-throughput corporate transaction feeds, enforce deterministic data validation schemas, cross-reference structural anomalies against an underlying graph database relationship matrix (**GraphRAG**), and synthesize executive security briefings via strictly-typed autonomous AI agents.

The core objective of AEVAR is to solve a multi-million dollar corporate problem: distinguishing benign, routine data-entry mistakes made by contractual partners (**Clerical Anomalies**) from intentional, unmapped billing ledger injection attacks (**Active Fraud Risks**).

---

## 🏗️ System Architecture & Data Flow

The platform relies on a completely decoupled, modular micro-services blueprint:

[ Raw Invoices JSON ]
│
▼
┌──────────────────────────┐
│  1. Ingestion Engine     │ ──► [ Validated Clean Ledger ] ──► (Persisted Data)
│  (Deterministic Pydantic)│
└──────────────────────────┘
│
▼ (Isolates Anomalies)
┌──────────────────────────┐
│  2. Quarantine Registry  │ ──► [ quarantined_invoices.json ]
└──────────────────────────┘
│
▼ (Enriches Context)
┌──────────────────────────┐
│  3. Neo4j GraphRAG Tier  │ ──► Cross-references entity paths & contract states
└──────────────────────────┘
│
▼ (Generates Analytics Payload)
┌──────────────────────────┐
│  4. Autonomous AI Agent  │ ──► Invokes Gemini-2.5-Flash with Pydantic Schema
└──────────────────────────┘
│
▼ (Structured Output Generation)
┌──────────────────────────┐
│  5. Streamlit Dashboard  │ ──► Live Telemetry + Real-time Audit Triggering
└──────────────────────────┘

1. **Deterministic Ingestion Layer:** Ingests unstructured billing items, parsing and enforcing type-safety, constraint boundaries, and value boundaries via Pydantic model schemas. Items passing validation move to the clean billing ledger; failures are routed to the Quarantine Registry.
2. **GraphRAG Audit Layer (Neo4j):** Isolates the quarantined data and maps the entities into a Neo4j Property Graph. It evaluates whether the vendor possesses active contract nodes, baseline vendor risk scores, or is completely unmapped in the corporate registry (rogue entity matches).
3. **Structured Intelligence Tier (Gemini-2.5-Flash):** Consumes the aggregated multi-modal data payload from the graph evaluation. Operating under low-temperature determinism and constrained by strict Pydantic schemas, it generates precise risk scores, dollar exposures, and mitigation steps.
4. **Operations Command Center (Streamlit):** Translates complex JSON/Graph data trails into a visual executive layout with performance-optimized data caching (`@st.cache_data`) and dynamic asynchronous action triggers.

---

## 🛠️ Repository File Structure

```text
AEVAR/
├── config/
│   └── settings.py              # Centralized environment pathing & constants
├── data/
│   ├── raw/                     # Mock data landing zone
│   ├── quarantine/              # Intercepted structural anomalies
│   └── processed/               # Clean ledgers, Graph reports, and AI briefings
├── src/
│   ├── ingestion/
│   │   ├── engine.py            # Stream parser and Pydantic validation rules
│   │   └── schemas.py           # Strictly-typed invoice definitions
│   ├── analytics/
│   │   ├── graph_store.py       # Neo4j Driver management & Cypher evaluation
│   │   └── reporter.py          # Corporate run-rate calculator & aggregation suite
│   ├── agents/
│   │   └── auditor.py           # Google GenAI SDK Agent orchestration & schema forcing
│   └── app/
│       └── dashboard.py         # Caching Streamlit UI & metrics telemetry
├── requirements.txt             # Project ecosystem dependencies
└── README.md                    # Core operational manual
🎛️ Technology Stack & Dependencies
Orchestration & UI: Python 3.11+, Streamlit
Data Engineering & Formatting: Pandas, Pydantic v2
Knowledge Graph Database: Neo4j Graph Database (Cypher Query Language)
Generative AI Core: Google GenAI SDK (gemini-2.5-flash)
Type Forcing Layer: Pydantic Structural Schemas
🚀 Installation & Local Environment Setup
1. Clone & Initialize Virtual Environment
Bash
git clone [https://github.com/hansitvarshney/AEVAR.git](https://github.com/hansitvarshney/AEVAR.git)
cd AEVAR

# Create and fire up virtual environment
python3 -m venv venv
source venv/bin/activate

# Install the enterprise dependencies
pip install -r requirements.txt
2. Configure Environment Access Keys
Set your infrastructure environment variables. Ensure your local Neo4j instance is running:
Bash
# Securely bind the native Gemini Client Key
export GEMINI_API_KEY="your_google_ai_studio_api_key_here"

# Establish Neo4j Graph Database Credentials
export NEO4J_URI="bolt://localhost:7687"
export NEO4J_USER="neo4j"
export NEO4J_PASSWORD="your_password"
3. Initialize and Seed the Knowledge Graph
Populate your local Neo4j graph instances with foundational company metadata, standard supplier nodes, and contract state matrices:
Bash
python seed.py
4. Boot the Data Pipeline & Launch the Dashboard
Run the end-to-end data processing engine and spin up the visual telemetry reporting workspace:
Bash
streamlit run src/app/dashboard.py
🤖 AI Agent Structured Reasoning Specification
The AI Auditor Agent utilizes an advanced corporate framework, compelling the language model to behave as an explicit analytical interface. By applying a custom strict Pydantic parsing layer, the agent bypasses standard non-deterministic textual string responses and outputs guaranteed structured analytical schemas:
Python
class ExecutiveBriefingSchema(BaseModel):
    risk_assessment_score: float = Field(..., description="Overall risk rating from 0.0 (Safe) to 1.0 (Critical Threat)")
    executive_summary: str = Field(..., description="High-level corporate briefing summarizing patterns.")
    fraud_exposure_usd: float = Field(..., description="Total dollar value currently targeted by explicit fraud injections.")
    critical_action_items: list[str] = Field(..., description="Remediation steps recommended for forensic accounting.")
    requires_immediate_freeze: bool = Field(..., description="True if fraud exposure warrants ledger freeze.")
This prevents corporate telemetry compilation failures, ensuring raw database values map perfectly into dashboard UI metric cards and executive notification components.
📈 Portfolio Competencies Demonstrated
Direct Enterprise Cloud Interfacing: Implemented structural agent patterns using the official native Google GenAI SDK, completely eliminating heavy third-party framework overhead.
Advanced GraphRAG implementation: Merged deterministic data screening with contextual graph traversals inside Neo4j using optimized Cypher processing.
Production-Grade UX Optimization: Implemented strict execution telemetry, data-caching mechanisms (@st.cache_data), and self-contained runtime data pipelines inside Streamlit.
Airtight Repository Practices: Developed a modular, enterprise-ready folder structure backed by structured git commits.