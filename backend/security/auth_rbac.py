class AuthManager:
    ROLES = {
        "Admin": ["all"],
        "DataEngineer": ["ingest", "clean", "transform", "lineage", "query", "view_dashboards"],
        "DataAnalyst": ["query", "view_dashboards", "ai_brain", "export_reports"],
        "BusinessViewer": ["view_dashboards", "read_insights"],
        "Auditor": ["view_compliance", "view_audit_logs", "verify_cryptography"]
    }

    USERS = {
        "admin@dataos.ai": {"name": "Chief Data Officer", "role": "Admin", "pass": "admin123"},
        "analyst@dataos.ai": {"name": "Senior BI Analyst", "role": "DataAnalyst", "pass": "analyst123"},
        "auditor@dataos.ai": {"name": "DPDP Compliance Officer", "role": "Auditor", "pass": "audit123"}
    }

    @classmethod
    def authenticate(cls, email, password):
        user = cls.USERS.get(email)
        if user and user["pass"] == password:
            return {
                "authenticated": True,
                "email": email,
                "name": user["name"],
                "role": user["role"],
                "token": f"bearer_{hash(email)}_{user['role']}"
            }
        return {"authenticated": False, "error": "Invalid credentials"}
