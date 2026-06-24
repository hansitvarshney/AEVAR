import os
import json
from pathlib import Path
from pydantic import BaseModel, Field
from google import genai
from google.genai import types
from config.settings import PROCESSED_DATA_DIR

# 1. Define the strictly-typed structure we want back from the Enterprise Agent
class ExecutiveBriefingSchema(BaseModel):
    risk_assessment_score: float = Field(..., description="Overall risk rating from 0.0 (Safe) to 1.0 (Critical Threat) based on anomalous patterns.")
    executive_summary: str = Field(..., description="High-level corporate briefing summarizing the structural anomalies vs intentional fraud attempts.")
    fraud_exposure_usd: float = Field(..., description="Total aggregated dollar value currently targeted by explicit rogue fraud injections.")
    critical_action_items: list[str] = Field(..., description="Strategic remediation steps recommended for the board or forensic accounting team.")
    requires_immediate_freeze: bool = Field(..., description="Flag true if fraud exposure or risk profile warrants an immediate accounts payable ledger freeze.")

def run_autonomous_audit():
    """
    Ingests the compiled GraphRAG audit ledger and runs a native Gemini 
    Structured Output sequence to produce an executive risk asset.
    """
    audit_report_path = PROCESSED_DATA_DIR / "quarantine_audit_report.json"
    
    if not audit_report_path.exists():
        print("❌ Error: GraphRAG audit ledger payload not found. Run the analytics reporter first.")
        return

    # Ingest the structured JSON artifact we saved in Milestone 4
    with open(audit_report_path, "r") as f:
        graph_audit_data = json.load(f)

    print("🤖 Initializing AEVAR AI Executive Auditor Agent...")
    
    # Initialize the official Google GenAI Client
    # Expects GEMINI_API_KEY to be set in your shell environment variables
    client = genai.Client()

    # Frame an airtight, high-context enterprise auditor prompt
    prompt = f"""
    You are the Chief Financial Risk Officer Agent for AEVAR. Your task is to evaluate the following 
    GraphRAG Quarantine Audit Ledger data and generate a definitive corporate risk briefing.
    
    Analyze the discrepancy between routine clerical entry errors (from contract-holding valid vendors) 
    and malicious, unmapped rogue entities attempting injection attacks (e.g., Corrupted Inc).
    
    Here is the live telemetry payload:
    {json.dumps(graph_audit_data, indent=2)}
    """

    try:
        # Request a structured output explicitly mapped to our Pydantic schema
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=ExecutiveBriefingSchema,
                temperature=0.2, # Low temperature for analytical determinism
            ),
        )
        
        # Parse the guaranteed valid JSON string back into a dictionary
        briefing_result = json.loads(response.text)
        
        print("\n✨ AI EXECUTIVE BRIEFING GENERATED SUCCESSFULLY ✨")
        print("==================================================")
        print(f"📈 Risk Assessment Score : {briefing_result['risk_assessment_score']}/1.0")
        print(f"💰 Fraud Exposure Asset  : ${briefing_result['fraud_exposure_usd']:,}")
        print(f"🔒 Emergency Freeze Required: {briefing_result['requires_immediate_freeze']}")
        print(f"📝 Executive Summary:\n{briefing_result['executive_summary']}\n")
        print("⚡ Recommended Action Items:")
        for item in briefing_result['critical_action_items']:
            print(f"  - {item}")
        print("==================================================")

        # Persist this final executive layer to disk
        output_file = PROCESSED_DATA_DIR / "executive_briefing.json"
        with open(output_file, "w") as out:
            json.dump(briefing_result, out, indent=4)
        print(f"📁 Saved Executive Asset -> {output_file}\n")
        
        return briefing_result

    except Exception as e:
        print(f"❌ Agent Orchestration Failure: {str(e)}")
        return None

if __name__ == "__main__":
    run_autonomous_audit()