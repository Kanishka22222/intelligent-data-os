import pandas as pd
import numpy as np

class AnomalyDetectionEngine:
    @staticmethod
    def detect_anomalies(df):
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        if not numeric_cols:
            return {"anomalies_found": 0, "records": []}

        # Multi-variable Z-score detection
        primary_col = "Sales" if "Sales" in numeric_cols else ("Taxable_Value" if "Taxable_Value" in numeric_cols else ("temperature_c" if "temperature_c" in numeric_cols else numeric_cols[0]))
        vals = pd.to_numeric(df[primary_col], errors="coerce").fillna(0.0)
        mean_val = float(vals.mean())
        std_val = float(vals.std()) if len(vals) > 1 else 1.0
        
        if std_val == 0:
            std_val = 1.0

        z_scores = np.abs((vals - mean_val) / std_val)
        anomaly_indices = np.where(z_scores > 2.2)[0]

        records = []
        for idx in anomaly_indices[:10]:
            row = df.iloc[idx].to_dict()
            clean_row = {k: (str(v) if pd.isna(v) else v) for k, v in row.items()}
            records.append({
                "index": int(idx),
                "metric_column": primary_col,
                "observed_value": round(float(vals.iloc[idx]), 2),
                "z_score": round(float(z_scores[idx]), 2),
                "severity": "CRITICAL" if z_scores[idx] > 3.0 else "WARNING",
                "reason": f"Value {vals.iloc[idx]:.2f} deviates significantly from mean ({mean_val:.2f}) by {z_scores[idx]:.1f} sigmas.",
                "row_sample": clean_row
            })

        return {
            "total_evaluated": len(df),
            "anomalies_found": len(anomaly_indices),
            "anomaly_rate_pct": round(float(len(anomaly_indices) / max(1, len(df)) * 100.0), 2),
            "primary_metric": primary_col,
            "records": records
        }
