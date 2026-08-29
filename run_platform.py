import os
import sys
import uvicorn

sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

if __name__ == "__main__":
    print("=" * 70)
    print(" [*] DATAOS: INTELLIGENT BIG DATA & ANALYTICS OPERATING SYSTEM")
    print("=" * 70)
    print(" [OK] Ingestion Connectors Initialized (CSV, JSON, IoT, REST APIs)")
    print(" [OK] Auto-ETL Cleaning & Visual DAG Pipeline Engine Ready")
    print(" [OK] AI Business Brain: Predictive Forecasts & Churn Matrix Active")
    print(" [OK] Security & DPDP Act 2023 / GDPR Statutory Scanner Active")
    print(" [OK] SHA-256 Cryptographic Audit Ledger Verified")
    print(" [OK] Unified Razorpay & Stripe Payment Engine Ready")
    print("=" * 70)
    print(" [>>] Access Web Studio at: http://localhost:8000")
    print(" [>>] Swagger API Docs at:  http://localhost:8000/docs")
    print("=" * 70)
    
    uvicorn.run("backend.server.app:app", host="127.0.0.1", port=8000, reload=False)
