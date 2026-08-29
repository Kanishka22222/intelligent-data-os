import unittest
import sys
import os
import pandas as pd

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from backend.ingestion.connectors import DatasetIngestionManager
from backend.etl.cleaner import AutoETLCleaner
from backend.etl.transformations import PipelineGraphExecutor
from backend.ai_brain.forecasting import TimeSeriesForecaster
from backend.ai_brain.customer_intelligence import CustomerBrain
from backend.ai_brain.anomaly_detector import AnomalyDetectionEngine
from backend.security.pii_masking import PIISecurityEngine
from backend.security.compliance_scanner import ComplianceScanner
from backend.security.audit_logger import AuditLogger
from backend.billing.subscription_manager import SubscriptionManager
from backend.billing.payment_gateway import PaymentGateway
from backend.learning.autonomous_trainer import AutonomousModelTrainer

class TestDataOSPlatform(unittest.TestCase):
    def setUp(self):
        self.ingestion = DatasetIngestionManager()

    def test_01_ingestion(self):
        datasets = self.ingestion.list_datasets()
        self.assertGreater(len(datasets), 0)
        df = self.ingestion.get_dataset("ecommerce_sales")
        self.assertIsNotNone(df)
        self.assertGreater(len(df), 50)

    def test_02_auto_cleaning(self):
        df = self.ingestion.get_dataset("ecommerce_sales")
        clean_res = AutoETLCleaner.clean_dataset(df)
        self.assertIn("cleaned_df", clean_res)
        self.assertGreaterEqual(clean_res["final_score"], clean_res["initial_score"])

    def test_03_pipeline_execution(self):
        df = self.ingestion.get_dataset("ecommerce_sales")
        nodes = [
            {"type": "filter", "params": {"column": "Sales", "operator": ">", "value": "100"}},
            {"type": "aggregate", "params": {"group_by": ["Category"], "agg_column": "Sales", "func": "sum"}}
        ]
        res_df, trace = PipelineGraphExecutor.run_pipeline(df, nodes)
        self.assertGreater(len(res_df), 0)
        self.assertEqual(len(trace), 2)

    def test_04_forecasting(self):
        df = self.ingestion.get_dataset("ecommerce_sales")
        fcst = TimeSeriesForecaster.forecast_metric(df)
        self.assertIn("growth_rate_pct", fcst)
        self.assertIn("forecast", fcst)
        self.assertGreater(len(fcst["forecast"]), 0)

    def test_05_customer_intelligence(self):
        df = self.ingestion.get_dataset("customer_churn")
        res = CustomerBrain.analyze_rfm_and_churn(df)
        self.assertIn("churn_rate_pct", res)
        self.assertIn("segments", res)

    def test_06_anomaly_detection(self):
        df = self.ingestion.get_dataset("ecommerce_sales")
        anomalies = AnomalyDetectionEngine.detect_anomalies(df)
        self.assertIn("anomalies_found", anomalies)

    def test_07_pii_masking(self):
        df_gst = self.ingestion.get_dataset("indian_financial_gst")
        findings = PIISecurityEngine.scan_dataframe(df_gst)
        self.assertGreater(len(findings), 0)
        masked_df, summary = PIISecurityEngine.mask_dataframe(df_gst, method="redact")
        self.assertEqual(len(masked_df), len(df_gst))
        self.assertGreater(len(summary), 0)

    def test_08_compliance_scan(self):
        df_gst = self.ingestion.get_dataset("indian_financial_gst")
        audit = ComplianceScanner.evaluate_compliance(df_gst, "indian_financial_gst")
        self.assertGreaterEqual(audit["overall_compliance_score"], 80.0)

    def test_09_audit_chain_integrity(self):
        logger = AuditLogger()
        logger.log_event("test@enterprise.com", "DataAnalyst", "TEST_ACTION", "UnitTests")
        valid, msg = logger.verify_integrity()
        self.assertTrue(valid)

    def test_10_billing_and_payments(self):
        sub_mgr = SubscriptionManager()
        status = sub_mgr.get_status()
        self.assertIn("plans", status)
        
        session = PaymentGateway.create_checkout_session("plan_pro")
        self.assertIn("order_id", session)
        
        invoice = PaymentGateway.verify_payment_and_generate_invoice(session["order_id"], "plan_pro")
        self.assertEqual(invoice["payment_status"], "PAID_VERIFIED")

    def test_11_autonomous_model_training_and_export(self):
        trainer = AutonomousModelTrainer()
        df = self.ingestion.get_dataset("ecommerce_sales")
        res = trainer.train_on_dataset("ecommerce_sales", df)
        self.assertEqual(res["status"], "success")
        self.assertGreater(res["autonomy_readiness_score"], 80.0)
        
        # Test standalone code generation
        code = trainer.generate_standalone_model_code()
        self.assertIn("class StandaloneBrain", code)
        self.assertIn("def predict_trend", code)
        self.assertIn("def detect_anomalies", code)
        self.assertIn("def nlq_inference", code)

if __name__ == "__main__":
    unittest.main()
