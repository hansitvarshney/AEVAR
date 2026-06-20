import json
from datetime import datetime
from pathlib import Path
from config.settings import RAW_DATA_DIR, PROCESSED_DATA_DIR, QUARANTINE_DIR
from src.ingestion.schemas import RawInvoiceModel
from pydantic import ValidationError

def run_pipeline():
    raw_file = RAW_DATA_DIR / "raw_invoices.json"
    
    if not raw_file.exists():
        print(f"❌ Error: Could not find raw data file at {raw_file}")
        return 0, 0

    with open(raw_file, "r") as f:
        invoices = json.load(f)

    valid_invoices = []
    quarantined_entries = []
    
    # 🌟 NEW: In-memory tracker for structural duplicate interception
    seen_invoice_ids = set()
    
    # 🌟 NEW: Static standard corporate conversion rates relative to USD
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
            # Pass record through our customized Pydantic validation boundaries
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

    return len(valid_invoices), len(quarantined_entries)

if __name__ == "__main__":
    processed, quarantined = run_pipeline()
    print("\n" + "="*45)
    print(f"🚀 INGESTION ENGINE METRICS COMPLETE 🚀")
    print(f" Clean Records Logged: {processed}")
    print(f" Isolated Quarantine Anomalies: {quarantined}")
    print("="*45 + "\n")