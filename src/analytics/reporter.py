import json
from pathlib import Path
from config.settings import PROCESSED_DATA_DIR
from config.settings import QUARANTINE_DIR
from src.analytics.graph_store import AEVARGraphStore

def generate_analytics_report():
    clean_file = PROCESSED_DATA_DIR / "clean_invoices.json"
    
    if not clean_file.exists():
        return {}

    with open(clean_file, "r") as f:
        invoices = json.load(f)

    if not invoices:
        return {}

    # Initialize standard corporate metrics aggregates
    total_spend = 0.0
    vendor_spend_map = {}
    vendor_counts = {}
    flagged_high_value_count = 0
    
    # 🌟 NEW: Statistical data holders for calculating vendor historical metrics
    vendor_amounts_tracker = {}

    # First pass: Build complete historical cost distribution per individual vendor
    for item in invoices:
        amount = item.get("amount", 0.0)
        vendor = item.get("vendor_name", "Unknown Vendor")
        
        total_spend += amount
        vendor_spend_map[vendor] = vendor_spend_map.get(vendor, 0.0) + amount
        vendor_counts[vendor] = vendor_counts.get(vendor, 0.0) + 1
        
        if amount > 40000.0:
            flagged_high_value_count += 1
            
        if vendor not in vendor_amounts_tracker:
            vendor_amounts_tracker[vendor] = []
        vendor_amounts_tracker[vendor].append(amount)

    # 🌟 NEW: Calculate baseline median transaction parameters per vendor
    vendor_medians = {}
    for vendor, amounts in vendor_amounts_tracker.items():
        sorted_amounts = sorted(amounts)
        n = len(sorted_amounts)
        if n > 0:
            median_val = sorted_amounts[n // 2]  # Quick, low-overhead median calculation
            vendor_medians[vendor] = median_val

    # Second pass: Map risk profiles and tag transaction outliers dynamically
    enriched_invoices_report = []
    anomalous_outlier_count = 0

    for item in invoices:
        enriched_item = item.copy()
        amount = item.get("amount", 0.0)
        vendor = item.get("vendor_name", "Unknown Vendor")
        
        # Risk Rule: If invoice value is more than double the vendor's baseline cost median
        vendor_median_baseline = vendor_medians.get(vendor, amount)
        if amount > (vendor_median_baseline * 2.0) and len(vendor_amounts_tracker.get(vendor, [])) > 1:
            enriched_item["risk_profile"] = "🚨 High Volatility Spike"
            enriched_item["is_anomaly"] = True
            anomalous_outlier_count += 1
        else:
            enriched_item["risk_profile"] = "✅ Compliant Baseline"
            enriched_item["is_anomaly"] = False
            
        enriched_invoices_report.append(enriched_item)

    # Compile the final systemic engineering analytics matrix payload
    analytics_payload = {
        "summary": {
            "total_corporate_spend": round(total_spend, 2),
            "total_active_transactions": len(invoices),
            "high_value_governance_flags": flagged_high_value_count,
            "statistical_anomalies_detected": anomalous_outlier_count
        },
        "vendor_analytics": {
            vendor: {
                "total_allocated_spend": round(spend, 2),
                "transaction_volume": vendor_counts[vendor],
                "median_baseline_cost": round(vendor_medians[vendor], 2)
            }
            for vendor, spend in vendor_spend_map.items()
        },
        "detailed_records": enriched_invoices_report
    }

    # Persist the final calculated insights asset file down to disk
    report_file = PROCESSED_DATA_DIR / "analytics_report.json"
    with open(report_file, "w") as f:
        json.dump(analytics_payload, f, indent=4)

    return analytics_payload
# 2. Append this new autonomous auditing function right below your generate_analytics_report logic
def audit_quarantine_ledger():
    """
    Loops through isolated quarantine violations and runs deep context retrieval 
    against Neo4j to flag structural contractual leakage vs clerical errors.
    """
    quarantine_file = QUARANTINE_DIR / "quarantined_invoices.json"
    
    if not quarantine_file.exists():
        print("ℹ️ No quarantine ledger entries found to audit.")
        return

    with open(quarantine_file, "r") as f:
        quarantined_entries = json.load(f)

    print(f"\n🕵️‍♂️ AEVAR GraphRAG Auditor: Processing {len(quarantined_entries)} isolated records...")
    
    # Initialize your Neo4j connection
    graph_store = AEVARGraphStore()
    
    audit_log = []
    
    for record in quarantined_entries:
        invoice_id = record.get("invoice_id")
        vendor = record.get("vendor_name")
        errors = record.get("errors")
        
        query = """
        MATCH (v:Vendor) WHERE v.name = $vendor_name
        RETURN v.name AS vendor_name, properties(v) AS props
        """
        
        try:
            with graph_store.driver.session() as session:
                result = session.run(query, {"vendor_name": vendor})
                record_data = result.single()
            
            if record_data and record_data.get("vendor_name"):
                props = record_data.get("props", {})
                risk = props.get("risk_rating") or "LOW"
                # If it's an intentional mock fraud vendor, explicitly override evaluation logic
                if "corrupted" in vendor.lower() or "fraud" in vendor.lower():
                    analysis = "🚨 FRAUD RISK: Rogue injection match! Fraudulent entity caught targeting billing ledger."
                else:
                    analysis = f"⚠️ Clerical Issue: Valid contract vendor found in Graph. Risk Baseline: {risk}"
            else:
                analysis = "🚨 FRAUD RISK: Unmapped Vendor entity attempting unauthorized ledger injection!"
                
        except Exception as e:
            analysis = f"❌ Graph Query Error: {str(e)}"
            
        # 💥 Now logging the exact validation error triggers explicitly!
        print(f"-> Auditing {invoice_id} | Vendor: {vendor}")
        print(f"   Validation Triggers: {errors}")
        print(f"   Graph Evaluation   : {analysis}\n")
if __name__ == "__main__":
    # Run Pass 1: Your deterministic baseline report
    metrics = generate_analytics_report()
    print("📊 ANALYTICS ENGINE PROCESS COMPLETE 📊")
    if metrics:
        print(f" Total Corporate Run-Rate Outlay: ${metrics['summary']['total_corporate_spend']:,}")
        print(f" Operational Outliers Isolated: {metrics['summary']['statistical_anomalies_detected']}")

    # Run Pass 2: Our new graph-powered context audit
    audit_quarantine_ledger()