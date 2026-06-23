# seed.py
from src.analytics.graph_store import AEVARGraphStore

def seed_database():
    graph = AEVARGraphStore()
    print("🌱 Seeding Master BOQ ceilings into Neo4j...")
    
    # Project Alpha contract parameters
    graph.seed_master_boq(
        project_id="PROJ-ALPHA",
        project_name="National Highway expansion Phase-1",
        item_code="M-CE-01",
        description="Grade 53 Portland Cement (Bags)",
        max_qty=5000.0, # Max contractual boundary limit
        unit_rate=6.5
    )
    
    graph.seed_master_boq(
        project_id="PROJ-ALPHA",
        project_name="National Highway expansion Phase-1",
        item_code="M-ST-02",
        description="Structural Reinforcement Steel Bars (Tons)",
        max_qty=120.0,
        unit_rate=1200.0
    )
    
    graph.close()
    print("✅ Neo4j database initialized with baseline engineering blueprints!")

if __name__ == "__main__":
    seed_database()