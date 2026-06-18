import json
from pathlib import Path
from config.settings import PROCESSED_DATA_DIR

def compute_business_metrics():
    processed_file = PROCESSED_DATA_DIR / "clean_invoices.json"
    
    if not processed_file.exists():
        print(f"❌ Analytics Error: No processed data found at {processed_file}")
        return

    with open(processed_file, "r") as f:
        invoices = json.load(f)

    if not invoices:
        print("⚠️ No valid invoices found to analyze.")
        return

    # Initialize analytical metrics parameters
    total_spend = 0.0
    vendor_aggregates = {}
    high_value_alerts = []
    HIGH_VALUE_THRESHOLD = 40000.0

    for inv in invoices:
        amount = inv["amount"]
        vendor = inv["vendor_name"]
        inv_id = inv["invoice_id"]
        
        # Accumulate absolute metrics
        total_spend += amount
        
        # Aggregate stats per vendor
        if vendor not in vendor_aggregates:
            vendor_aggregates[vendor] = {"total_spent": 0.0, "invoice_count": 0}
        
        vendor_aggregates[vendor]["total_spent"] += amount
        vendor_aggregates[vendor]["invoice_count"] += 1
        
        # Risk & Compliance Check: Flag unusually large corporate expenses
        if amount >= HIGH_VALUE_THRESHOLD:
            high_value_alerts.append({"invoice_id": inv_id, "vendor": vendor, "amount": amount})

    # Print a beautiful, clean corporate executive summary dashboard
    print("\n" + "="*50)
    print("       📊 EXECUTABLE BUSINESS INTELLIGENCE REPORT      ")
    print("="*50)
    print(f" 💰 Total Validated Spend : ${total_spend:,.2f}")
    print(f" 📑 Total Invoices Settled: {len(invoices)}")
    print(f" 📈 Average Invoice Value : ${total_spend / len(invoices):,.2f}")
    
    print("\n🏢 VENDOR PERFORMANCE METRICS:")
    print("-" * 50)
    for vendor, stats in vendor_aggregates.items():
        avg_value = stats["total_spent"] / stats["invoice_count"]
        print(f" • {vendor:<15} | Total: ${stats['total_spent']:>10,.2f} | Count: {stats['invoice_count']:>2} | Avg: ${avg_value:,.2f}")
        
    if high_value_alerts:
        print("\n🚨 RISK MITIGATION: HIGH-VALUE AUDIT ALERTS (>= $40K)")
        print("-" * 50)
        for alert in high_value_alerts:
            print(f" ⚠️ FLAG: {alert['invoice_id']} | {alert['vendor']:<15} | Requires Sign-off: ${alert['amount']:,.2f}")
            
    print("="*50 + "\n")

if __name__ == "__main__":
    compute_business_metrics()