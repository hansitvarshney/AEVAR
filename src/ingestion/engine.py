import json
from pathlib import Path
from config.settings import RAW_DATA_DIR, PROCESSED_DATA_DIR, QUARANTINE_DIR
from src.ingestion.schemas import RawInvoiceModel
from pydantic import ValidationError

def run_pipeline():
    raw_file = RAW_DATA_DIR / "raw_invoices.json"
    
    # Sanity check: make sure mock data actually exists
    if not raw_file.exists():
        print(f"❌ Error: Could not find raw data file at {raw_file}")
        print("Please run: PYTHONPATH=. python -m src.ingestion.mock_generator first!")
        return 0, 0

    with open(raw_file, "r") as f:
        invoices = json.load(f)

    valid_invoices = []
    quarantined_entries = []

    # Process and validate each transaction record
    for record in invoices:
        try:
            # Pass record through the Pydantic structural validation model
            validated_invoice = RawInvoiceModel(**record)
            # Pydantic exports model dump as standard dict format
            valid_invoices.append(validated_invoice.model_dump(mode='json'))
        except ValidationError as e:
            # Capture the validation errors along with the raw payload
            corrupted_record = record.copy()
            
            # Extract just the readable text messages from Pydantic's errors
            readable_errors = []
            for err in e.errors():
                location = " -> ".join(str(loc) for loc in err["loc"])
                message = err["msg"]
                readable_errors.append(f"[{location}]: {message}")
            
            corrupted_record["errors"] = readable_errors
            quarantined_entries.append(corrupted_record)

    # Save cleanly processed corporate records
    processed_file = PROCESSED_DATA_DIR / "clean_invoices.json"
    with open(processed_file, "w") as f:
        json.dump(valid_invoices, f, indent=4)

    # Save intercepted corrupted records to quarantine files
    quarantine_file = QUARANTINE_DIR / "quarantined_invoices.json"
    with open(quarantine_file, "w") as f:
        json.dump(quarantined_entries, f, indent=4)

    return len(valid_invoices), len(quarantined_entries)

if __name__ == "__main__":
    processed, quarantined = run_pipeline()
    
    print("\n" + "="*45)
    print("         🚀 INGESTION ENGINE METRICS 🚀        ")
    print("="*45)
    print(f" ✅ Successfully Processed Records : {processed}")
    print(f" ❌ Routed to Quarantine Logs     : {quarantined}")
    print(f" Total Invoices Evaluated          : {processed + quarantined}")
    print("="*45 + "\n")