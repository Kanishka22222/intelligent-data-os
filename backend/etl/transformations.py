import pandas as pd
import numpy as np
from backend.etl.cleaner import AutoETLCleaner

class PipelineGraphExecutor:
    @staticmethod
    def execute_node(df, node_type, params):
        res_df = df.copy()
        msg = ""

        if node_type == "filter":
            col = params.get("column")
            op = params.get("operator", "==")
            val = params.get("value")
            if col in res_df.columns:
                if op == "==":
                    res_df = res_df[res_df[col].astype(str) == str(val)]
                elif op == "!=":
                    res_df = res_df[res_df[col].astype(str) != str(val)]
                elif op == ">":
                    res_df = res_df[pd.to_numeric(res_df[col], errors="coerce") > float(val)]
                elif op == "<":
                    res_df = res_df[pd.to_numeric(res_df[col], errors="coerce") < float(val)]
                elif op == "contains":
                    res_df = res_df[res_df[col].astype(str).str.contains(str(val), case=False, na=False)]
                msg = f"Filtered '{col}' where value {op} '{val}'. Rows: {len(res_df)}"

        elif node_type == "select":
            cols = params.get("columns", [])
            valid_cols = [c for c in cols if c in res_df.columns]
            if valid_cols:
                res_df = res_df[valid_cols]
                msg = f"Selected {len(valid_cols)} columns: {', '.join(valid_cols)}."

        elif node_type == "sort":
            col = params.get("column")
            asc = params.get("ascending", True)
            if col in res_df.columns:
                res_df = res_df.sort_values(by=col, ascending=asc)
                msg = f"Sorted by '{col}' ({'Ascending' if asc else 'Descending'})."

        elif node_type == "aggregate":
            group_by = params.get("group_by", [])
            agg_col = params.get("agg_column")
            func = params.get("func", "sum")
            valid_groups = [g for g in group_by if g in res_df.columns]
            if valid_groups and agg_col in res_df.columns:
                res_df[agg_col] = pd.to_numeric(res_df[agg_col], errors="coerce")
                res_df = res_df.groupby(valid_groups)[agg_col].agg(func).reset_index()
                msg = f"Aggregated '{agg_col}' ({func}) grouped by {', '.join(valid_groups)}."

        elif node_type == "mutate":
            new_col = params.get("new_column", "calculated_metric")
            formula = params.get("formula", "")
            try:
                # Safe evaluated arithmetic on columns
                res_df[new_col] = res_df.eval(formula)
                msg = f"Created column '{new_col}' using formula: '{formula}'."
            except Exception as e:
                msg = f"Mutation warning: {str(e)}"

        elif node_type == "auto_clean":
            clean_res = AutoETLCleaner.clean_dataset(res_df)
            res_df = clean_res["cleaned_df"]
            msg = f"Auto-cleaned: Quality score improved from {clean_res['initial_score']}% to {clean_res['final_score']}%."

        return res_df, msg

    @classmethod
    def run_pipeline(cls, initial_df, nodes):
        current_df = initial_df.copy()
        execution_trace = []
        for i, node in enumerate(nodes):
            n_type = node.get("type", "unknown")
            params = node.get("params", {})
            rows_before = len(current_df)
            current_df, step_msg = cls.execute_node(current_df, n_type, params)
            rows_after = len(current_df)
            execution_trace.append({
                "step": i + 1,
                "node_type": n_type,
                "description": step_msg or f"Executed {n_type}",
                "rows_before": rows_before,
                "rows_after": rows_after
            })
        return current_df, execution_trace
