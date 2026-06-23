import json
from datetime import datetime
from pathlib import Path
from src.analytics.graph_store import AEVARGraphStore
from typing import Dict, Any, List, Literal
from typing_extensions import TypedDict

# 1. Your Exact Original Validation & Configuration Imports
from config.settings import RAW_DATA_DIR, PROCESSED_DATA_DIR, QUARANTINE_DIR
from src.ingestion.schemas import RawInvoiceModel
from pydantic import ValidationError

# 2. Advanced Agentic Orchestration Imports
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI


# =====================================================================
# 1. LANGGRAPH STATE DEFINITION
# =====================================================================
class IngestionState(TypedDict):
    """
    Maintains the state across the data-extraction and structural-validation pipeline.
    """
    raw_unstructured_text: str    # Messy text input sent directly via user or dashboard
    extracted_json_list: List[Dict[str, Any]] # Structured payload processed by the LLM
    valid_records_count: int      # Cumulative count of valid corporate ledger entries
    quarantine_records_count: int # Cumulative count of isolated anomalies
    routing_destination: str      # State-machine directional flag
    errors: List[str]             # Execution logs capturing pipeline noise


# =====================================================================
# 2. STATE GRAPH WORKFLOW NODES
# =====================================================================

def extract_unstructured_text_node(state: IngestionState) -> Dict[str, Any]:
    """
    Node 1: Uses LLM Structured Outputs bound directly to your RawInvoiceModel 
    to force text extraction into a predictable JSON array layout.
    """
    raw_text = state.get("raw_unstructured_text", "").strip()
    if not raw_text:
        # If no unstructured text is explicitly given, bypass extraction smoothly
        return {"extracted_json_list": [], "errors": []}

    # Low-temperature engine configuration for absolute deterministic extraction
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    structured_llm = llm.with_structured_output(RawInvoiceModel)
    
    try:
        system_prompt = f"Extract all relevant invoice parameters into clean fields out of this text log: {raw_text}"
        extraction_result = structured_llm.invoke(system_prompt)
        
        # Format the Pydantic dictionary into a processing array list
        extracted_data = [extraction_result.model_dump(mode='json')]
        return {
            "extracted_json_list": extracted_data,
            "errors": []
        }
    except Exception as e:
        return {
            "extracted_json_list": [],
            "errors": [f"LLM Structural Extraction Node Failure: {str(e)}"]
        }


def run_deterministic_engine_node(state: IngestionState) -> Dict[str, Any]:
    """
    Node 2: YOUR EXACT ORIGINAL ENGINE (Fully Integrated).
    Processes data streams, converts currencies, intercepts duplicates, and logs metric histories.
    """
    # Look for agentically extracted json items first; fallback to files if empty
    invoices = state.get("extracted_json_list", [])
    
    if not invoices:
        raw_file = RAW_DATA_DIR / "raw_invoices.json"
        
        if not raw_file.exists():
            print(f"❌ Error: Could not find raw data file at {raw_file}")
            return {
                "valid_records_count": 0,
                "quarantine_records_count": 0,
                "routing_destination": "failed",
                "errors": state["errors"] + [f"File missing at {raw_file}"]
            }

        with open(raw_file, "r") as f:
            invoices = json.load(f)

    valid_invoices = []
    quarantined_entries = []
    
    # 🌟 Your original in-memory tracker for structural duplicate interception
    seen_invoice_ids = set()
    
    # 🌟 Your static standard corporate conversion rates relative to USD
    EXCHANGE_RATES = {"USD": 1.0, "EUR": 1.08, "INR": 0.012}

    for record in invoices:
        corrupted_record = record.copy()
        invoice_id = record.get("invoice_id")

        # 1️⃣ INTERCEPT DUPLICATES BEFORE RUNNING PYDANTIC VALIDATION
        if invoice_id in seen_invoice_ids:
            corrupted_record["errors"] = ["Security Flag: Duplicate Transaction ID Intercepted"]
            quarantined_entries.append(corrupted_record)
            continue
        
        try:
            # Pass record through your customized Pydantic validation boundaries
            validated_invoice = RawInvoiceModel(**record)
            invoice_dict = validated_invoice.model_dump(mode='json')
            
            # 2️⃣ MULTI-CURRENCY NORMALIZATION MATRIX
            currency = invoice_dict.get("currency", "USD")
            raw_amount = invoice_dict.get("amount", 0.0)
            
            if currency != "USD":
                rate = EXCHANGE_RATES.get(currency, 1.0)
                invoice_dict["amount"] = round(raw_amount * rate, 2)
                invoice_dict["currency"] = "USD"  # Standardized base currency conversion

            valid_invoices.append(invoice_dict)
            seen_invoice_ids.add(invoice_id)  # Track this unique ID to catch eventual duplicates
            try:
             graph_db = AEVARGraphStore()
             graph_db.log_validated_invoice(
                 invoice_id=invoice_dict.get("invoice_id"),
                 vendor_name=invoice_dict.get("vendor_name"),
                 item_code=invoice_dict.get("item_code", "M-CE-01"), # Fallback generic item
                 amount=invoice_dict.get("amount"),
                 quantity=invoice_dict.get("quantity", 100.0),      # Fallback sample qty
                 project_id=invoice_dict.get("project_id", "PROJ-ALPHA")
             )
             graph_db.close()
            except Exception as g_err:
             print(f"⚠️ Graph database sync bypassed: {g_err}")
        except ValidationError as e:
            readable_errors = []
            for err in e.errors():
                location = " -> ".join(str(loc) for loc in err["loc"])
                message = err["msg"]
                readable_errors.append(f"[{location}]: {message}")
            
            corrupted_record["errors"] = readable_errors
            quarantined_entries.append(corrupted_record)

    # Persist clean structural corporate datasets
    processed_file = PROCESSED_DATA_DIR / "clean_invoices.json"
    with open(processed_file, "w") as f:
        json.dump(valid_invoices, f, indent=4)

    # Persist isolated system quarantine audit data blocks
    quarantine_file = QUARANTINE_DIR / "quarantined_invoices.json"
    with open(quarantine_file, "w") as f:
        json.dump(quarantined_entries, f, indent=4)

    # 3️⃣ PERSISTENT PIPELINE DATA METRICS LOGGER FOR METRIC HISTORY
    history_file = PROCESSED_DATA_DIR / "pipeline_history.json"
    history_data = []
    
    if history_file.exists():
        try:
            with open(history_file, "r") as hf:
                history_data = json.load(hf)
        except Exception:
            history_data = []

    # Keep a rolling historical trace of the last 15 operational executions
    history_data.append({
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "processed_successfully": len(valid_invoices),
        "quarantined_failures": len(quarantined_entries)
    })
    history_data = history_data[-15:]
    
    with open(history_file, "w") as hf:
        json.dump(history_data, hf, indent=4)

    return {
        "valid_records_count": len(valid_invoices),
        "quarantine_records_count": len(quarantined_entries),
        "routing_destination": "success" if len(quarantined_entries) == 0 else "needs_reconciliation"
    }


# =====================================================================
# 3. GRAPH ENGINE PIPELINE COMPILATION
# =====================================================================
def compile_workflow_graph():
    workflow = StateGraph(IngestionState)
    
    # Register graph nodes
    workflow.add_node("extract_unstructured_text", extract_unstructured_text_node)
    workflow.add_node("run_deterministic_engine", run_deterministic_engine_node)
    
    # Establish pipeline sequence
    workflow.set_entry_point("extract_unstructured_text")
    workflow.add_edge("extract_unstructured_text", "run_deterministic_engine")
    
    # Handle clean programmatic execution exit matching LangGraph standards
    def route_decision(state: IngestionState) -> Literal["complete", "failed"]:
        if state["routing_destination"] in ["success", "needs_reconciliation"]:
            return "complete"
        return "failed"
        
    workflow.add_conditional_edges(
        "run_deterministic_engine",
        route_decision,
        {
            "complete": END,
            "failed": END
        }
    )
    
    return workflow.compile()


# =====================================================================
# 4. BACKWARD COMPATIBLE APPLICATION WRAPPER
# =====================================================================
def run_pipeline(unstructured_text: str = None):
    """
    Main orchestration function.
    - If unstructured_text is passed: Uses LLM to extract fields, then validates.
    - If no text is passed: Natively processes your local raw_invoices.json file.
    """
    app = compile_workflow_graph()
    
    initial_state: IngestionState = {
        "raw_unstructured_text": unstructured_text if unstructured_text else "",
        "extracted_json_list": [],
        "valid_records_count": 0,
        "quarantine_records_count": 0,
        "routing_destination": "",
        "errors": []
    }
    
    final_state = app.invoke(initial_state)
    return final_state["valid_records_count"], final_state["quarantine_records_count"]


if __name__ == "__main__":
    # Natively executes over raw_invoices.json file to guarantee backward compatibility!
    processed, quarantined = run_pipeline()
    
    print("\n" + "="*45)
    print(f"🚀 INGESTION ENGINE METRICS COMPLETE 🚀")
    print(f" Clean Records Logged: {processed}")
    print(f" Isolated Quarantine Anomalies: {quarantined}")
    print("="*45 + "\n")