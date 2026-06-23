import sys
from pathlib import Path
# Force append the parent project root directory workspace directly to the system lookup paths
sys.path.append(str(Path(__file__).resolve().parents[2]))
import streamlit as st  # standard import alias
import json
import pandas as pd
from datetime import datetime
from pathlib import Path
from config.settings import PROCESSED_DATA_DIR, QUARANTINE_DIRs
from src.analytics.reporter import generate_analytics_report

# Configure clean enterprise viewport structure
st.set_page_config(page_title="AEVAR | Financial Governance Engine", layout="wide")

st.title("🛡️ AEVAR: Financial Data Ingestion & Governance Engine")
st.markdown("---")

# File Path Resolutions
clean_file = PROCESSED_DATA_DIR / "clean_invoices.json"
quarantine_file = QUARANTINE_DIR / "quarantined_invoices.json"
history_file = PROCESSED_DATA_DIR / "pipeline_history.json"

# Re-run backend engines dynamically to ensure data synchronization
analytics_data = generate_analytics_report()

# -------------------------------------------------------------------------
# 📈 SECTION 1: EXECUTION METRICS LOGGER & PIPELINE HISTORY GRAPH
# -------------------------------------------------------------------------
st.subheader("⚙️ Data Pipeline Operational Health History")

if history_file.exists():
    with open(history_file, "r") as hf:
        history_log = json.load(hf)
    
    if history_log:
        df_history = pd.DataFrame(history_log)
        # Rename structural columns for readable presentation labels
        df_history_chart = df_history.rename(columns={
            "processed_successfully": "Clean Success Records", 
            "quarantined_failures": "Quarantine Interceptions"
        }).set_index("timestamp")
        
        # Display operational volumes inside a clean line chart visualization
        st.line_chart(df_history_chart, height=200)
st.markdown("---")

# -------------------------------------------------------------------------
# 📊 SECTION 2: EXECUTIVE KPIS & RISK PROFILER OVERVIEW
# -------------------------------------------------------------------------
if analytics_data and "summary" in analytics_data:
    summary = analytics_data["summary"]
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(label="Total Corporate Outlay", value=f"${summary['total_corporate_spend']:,}")
    with col2:
        st.metric(label="Ingested Transactions", value=summary["total_active_transactions"])
    with col3:
        st.metric(label="High-Value Flags (>$40K)", value=summary["high_value_governance_flags"])
    with col4:
        st.metric(label="Price Volatility Outliers", value=summary["statistical_anomalies_detected"])
else:
    st.warning("No clean computational metrics found. Please execute your mock dataset generator first.")

st.markdown("---")

# -------------------------------------------------------------------------
# ⏳ SECTION 3: REVENUE SLA AGING COMPLIANCE DESK
# -------------------------------------------------------------------------
st.subheader("⏳ Accounts Payable Aging & SLA Compliance Desk")
aging_col1, aging_col2 = st.columns([1, 2])

critical_sla_count = 0
clean_invoices_list = analytics_data.get("detailed_records", [])

# Parse dates dynamically using pandas to measure age from current time threshold
if clean_invoices_list:
    for inv in clean_invoices_list:
        if "invoice_date" in inv:
            try:
                inv_date = datetime.strptime(inv["invoice_date"], "%Y-%m-%d")
                days_elapsed = (datetime.now() - inv_date).days
                if days_elapsed > 30:
                    critical_sla_count += 1
            except ValueError:
                pass

with aging_col1:
    if critical_sla_count > 0:
        st.error(f"⚠️ Unsettled Items Past Net-30 SLA: {critical_sla_count}")
    else:
        st.success("✅ Cash Flow Optimal: All clean invoices comply with standard Net-30 intervals.")
with aging_col2:
    st.info("💡 Governance Rule: Invoices older than 30 days require immediate dynamic cash allocation sign-off.")

st.markdown("---")

# -------------------------------------------------------------------------
# 🖥️ SECTION 4: INTERACTIVE LEDGER EXPLORER & MULTI-FORMAT EXPORTS
# -------------------------------------------------------------------------
tab1, tab2 = st.tabs(["🟢 Verified Corporate Ledger", "🔴 Isolated Quarantine Vault"])

with tab1:
    st.subheader("Verified & Normalized Transaction Influx")
    if clean_invoices_list:
        df_clean = pd.DataFrame(clean_invoices_list)
        
        # Style dataframe to make risk profile tags easily scanable
        st.dataframe(df_clean, use_container_width=True)
        
        # 📥 Enterprise Feature: CSV Export Mechanism
        csv_clean = df_clean.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Export Verified Ledger to CSV",
            data=csv_clean,
            file_name=f"aevar_clean_ledger_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )
    else:
        st.info("No clean transaction records present.")

with tab2:
    st.subheader("Intercepted Structural & Logical Anomalies")
    if quarantine_file.exists():
        with open(quarantine_file, "r") as qf:
            quarantine_records = json.load(qf)
            
        if quarantine_records:
            df_quarantine = pd.DataFrame(quarantine_records)
            st.dataframe(df_quarantine, use_container_width=True)
            
            # 📥 Enterprise Feature: CSV Export Mechanism
            csv_quarantine = df_quarantine.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Export Isolated Vault to CSV",
                data=csv_quarantine,
                file_name=f"aevar_quarantine_audit_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )
        else:
            st.success("Pipeline running clean. Quarantine vault contains zero structural errors.")
    else:
        st.success("Quarantine registry sound.")