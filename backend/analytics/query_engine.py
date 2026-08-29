import pandas as pd
import numpy as np

class AnalyticsQueryEngine:
    @staticmethod
    def get_summary_statistics(df):
        numeric_df = df.select_dtypes(include=[np.number])
        summary = {}
        for col in numeric_df.columns:
            s = numeric_df[col].dropna()
            if not s.empty:
                summary[col] = {
                    "count": int(len(s)),
                    "mean": round(float(s.mean()), 2),
                    "std": round(float(s.std()), 2) if len(s) > 1 else 0.0,
                    "min": round(float(s.min()), 2),
                    "25%": round(float(s.quantile(0.25)), 2),
                    "median": round(float(s.median()), 2),
                    "75%": round(float(s.quantile(0.75)), 2),
                    "max": round(float(s.max()), 2),
                    "sum": round(float(s.sum()), 2)
                }
        return summary

    @staticmethod
    def get_correlation_matrix(df):
        numeric_df = df.select_dtypes(include=[np.number])
        if numeric_df.shape[1] < 2:
            return {"columns": [], "matrix": []}
        corr = numeric_df.corr().fillna(0.0)
        return {
            "columns": list(corr.columns),
            "matrix": [[round(float(val), 2) for val in row] for row in corr.values]
        }

    @staticmethod
    def run_aggregate_query(df, group_by_col, metric_col, agg_type="sum"):
        if group_by_col not in df.columns or metric_col not in df.columns:
            return []
        temp_df = df.copy()
        temp_df[metric_col] = pd.to_numeric(temp_df[metric_col], errors="coerce")
        res = temp_df.groupby(group_by_col)[metric_col].agg(agg_type).reset_index()
        res = res.sort_values(by=metric_col, ascending=False).head(15)
        return res.to_dict(orient="records")
