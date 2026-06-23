from neo4j import GraphDatabase

class AEVARGraphStore:
    def __init__(self, uri="bolt://localhost:7687", user="neo4j", password="password123"):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def seed_master_boq(self, project_id: str, project_name: str, item_code: str, description: str, max_qty: float, unit_rate: float):
        """
        Populates the baseline contractual limits for a project.
        """
        query = """
        MERGE (p:Project {id: $project_id})
        ON CREATE SET p.name = $project_name
        
        MERGE (b:MasterBOQItem {item_code: $item_code})
        ON CREATE SET b.description = $description, b.max_quantity = $max_qty, b.unit_rate = $unit_rate
        
        MERGE (p)-[:HAS_BLUEPRINT]->(b)
        """
        with self.driver.session() as session:
            session.run(query, project_id=project_id, project_name=project_name, 
                        item_code=item_code, description=description, max_qty=max_qty, unit_rate=unit_rate)

    def log_validated_invoice(self, invoice_id: str, vendor_name: str, item_code: str, amount: float, quantity: float, project_id: str):
        """
        Links incoming physical vendor spending back to contract entities.
        """
        query = """
        MERGE (v:Vendor {name: $vendor_name})
        
        CREATE (i:Invoice {id: $invoice_id, amount: $amount, quantity: $quantity, timestamp: timestamp()})
        
        MERGE (p:Project {id: $project_id})
        MERGE (b:MasterBOQItem {item_code: $item_code})
        
        CREATE (v)-[:ISSUED]->(i)
        CREATE (i)-[:BILLED_TO]->(p)
        CREATE (i)-[:CHARGED_FOR]->(b)
        """
        with self.driver.session() as session:
            session.run(query, invoice_id=invoice_id, vendor_name=vendor_name, 
                        item_code=item_code, amount=amount, quantity=quantity, project_id=project_id)