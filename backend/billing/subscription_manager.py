class SubscriptionManager:
    PLANS = [
        {
            "id": "plan_free",
            "name": "Community Starter",
            "price_usd": 0,
            "price_inr": 0,
            "billing_cycle": "Forever Free",
            "features": [
                "100 Query Executions / month",
                "Up to 5 Ingested Datasets",
                "Standard Auto-Cleaning ETL",
                "Basic Charts & KPI Cards",
                "Community Support"
            ],
            "is_current": True,
            "badge": "Current Tier"
        },
        {
            "id": "plan_pro",
            "name": "Pro Data Strategist",
            "price_usd": 29,
            "price_inr": 2499,
            "billing_cycle": "Monthly",
            "features": [
                "10,000 Query Executions / month",
                "Unlimited Dataset Ingestion",
                "AI Business Brain & Predictive Forecasts",
                "Automated PII Masking (Aadhaar/PAN/Cards)",
                "Executive PDF Report Generator",
                "Voice & Multilingual NLP Assistant",
                "Priority Email & Slack Support"
            ],
            "is_popular": True,
            "badge": "Most Popular"
        },
        {
            "id": "plan_enterprise",
            "name": "Enterprise Autonomous Brain",
            "price_usd": 199,
            "price_inr": 16999,
            "billing_cycle": "Monthly / Billed Annually",
            "features": [
                "Unlimited High-Throughput Analytics",
                "Full DPDP Act 2023 & GDPR Compliance Audit",
                "Cryptographic SHA-256 Audit Ledger",
                "Custom Sector Playbooks & Fine-Tuning",
                "Live IoT Stream & Webhook Connectors",
                "Air-Gapped Private Cloud & On-Prem Deployment",
                "24/7 Dedicated Solutions Engineer"
            ],
            "badge": "Enterprise Ready"
        }
    ]

    def __init__(self):
        self.current_plan = "plan_free"
        self.query_quota_used = 18
        self.query_quota_limit = 100

    def upgrade_plan(self, plan_id):
        for p in self.PLANS:
            if p["id"] == plan_id:
                self.current_plan = plan_id
                self.query_quota_limit = 10000 if plan_id == "plan_pro" else 999999
                return True, f"Successfully upgraded to {p['name']}!"
        return False, "Plan ID not found."

    def get_status(self):
        plan_obj = next((p for p in self.PLANS if p["id"] == self.current_plan), self.PLANS[0])
        return {
            "current_plan": plan_obj,
            "query_quota_used": self.query_quota_used,
            "query_quota_limit": self.query_quota_limit,
            "quota_remaining": max(0, self.query_quota_limit - self.query_quota_used),
            "plans": self.PLANS
        }
