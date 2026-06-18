import json
import random
from config.settings import RAW_DATA_DIR

def generate_chaotic_invoices(count=100):
    raw_file_path = RAW_DATA_DIR / "raw_invoices.json"
    invoices = []
    
    for i in range(count):
        invoice = {
            "invoice_id": f"INV-{1000 + i}",
            "vendor_name": random.choice(["Alpha Const", "Beta Logistics", "Gamma Build", "Corrupted Inc"]),
            "amount": random.choice([float(random.randint(5000, 50000)), f"${random.randint(5000, 50000)}", -1500.0, None]),
            "status": random.choice(["PAID", "PENDING", "PROCESSING", ""])
        }
        invoices.append(invoice)
        
    with open(raw_file_path, "w") as f:
        json.dump(invoices, f, indent=4)
        
    print("✅ Chaotic mock data generated inside data/raw/raw_invoices.json")

if __name__ == "__main__":
    generate_chaotic_invoices()