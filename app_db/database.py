import os
from appwrite.client import Client
from appwrite.services.databases import Databases
import uuid
import json
from typing import Dict, Any
from dotenv import load_dotenv

load_dotenv()

class AppwriteDatabase:
    def __init__(self):
        self.client = Client()
        self.endpoint = os.getenv("APPWRITE_ENDPOINT", "https://cloud.appwrite.io/v1")
        self.project_id = os.getenv("APPWRITE_PROJECT_ID")
        self.api_key = os.getenv("APPWRITE_API_KEY")
        self.database_id = os.getenv("APPWRITE_DATABASE_ID")
        self.collection_id = os.getenv("APPWRITE_SCANS_COLLECTION_ID")
        
        if self.project_id and self.api_key:
            self.client.set_endpoint(self.endpoint)
            self.client.set_project(self.project_id)
            self.client.set_key(self.api_key)
            self.db = Databases(self.client)
        else:
            self.db = None

    def save_scan(self, scan_data: Dict[str, Any]):
        if not self.db:
            print("Appwrite not configured. Skipping save.")
            return None
            
        try:
            # Prepare document data as per Constitution Section 8.1
            document = {
                "scan_id": str(uuid.uuid4()),
                "user_id": scan_data.get("user_id", "guest"),
                "repo_url": scan_data.get("repo_url"),
                "repo_name": scan_data.get("repo_name"),
                "scanned_at": scan_data.get("scanned_at"),
                "health_score": scan_data.get("health_score"),
                "grade": scan_data.get("grade"),
                "total_findings": len(scan_data.get("findings", [])),
                "critical_count": scan_data.get("counts", {}).get("critical", 0),
                "high_count": scan_data.get("counts", {}).get("high", 0),
                "medium_count": scan_data.get("counts", {}).get("medium", 0),
                "low_count": scan_data.get("counts", {}).get("low", 0),
                "findings_json": json.dumps(scan_data.get("findings", [])),
                "ai_summary": scan_data.get("ai_summary", ""),
                "scan_duration": int(scan_data.get("duration", 0))
            }
            
            result = self.db.create_document(
                database_id=self.database_id,
                collection_id=self.collection_id,
                document_id=document["scan_id"],
                data=document
            )
            return result
        except Exception as e:
            print(f"Appwrite Save Error: {e}")
            return None
