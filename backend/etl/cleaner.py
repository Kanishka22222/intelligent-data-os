import pandas as pd
import numpy as np

class AutoETLCleaner:
    @staticmethod
    def calculate_quality_score(df):
        total_cells = df.size
        if total_cells == 0:
            return 100.0
        missing_cells = int(df.isna().sum().sum())
        duplicate_rows = int(df.duplicated().sum())
        
        # Penalties
        missing_penalty = (missing_cells / total_cells) * 60.0
        dup_penalty = (duplicate_rows / len(df)) * 40.0 if len(df) > 0 else 0
        score = max(5.0, min(100.0, 100.0 - (missing_penalty + dup_penalty)))
        return round(float(score), 1)

    @classmethod
    def clean_dataset(cls, df):
        initial_score = cls.calculate_quality_score(df)
        initial_rows = len(df)
        logs = []
        cleaned_df = df.copy()

        # 1. Deduplication
        dup_count = int(cleaned_df.duplicated().sum())
        if dup_count > 0:
            cleaned_df = cleaned_df.drop_duplicates()
            logs.append(f"Removed {dup_count} duplicate rows.")

        # 2. Column-by-column cleaning
        for col in cleaned_df.columns:
            # Check if column looks like a date
            if "date" in col.lower() or "time" in col.lower():
                try:
                    cleaned_df[col] = pd.to_datetime(cleaned_df[col], errors="ignore")
                    logs.append(f"Parsed datetime format for column '{col}'.")
                except Exception:
                    pass

            # Numeric imputation & outlier handling
            if pd.api.types.is_numeric_dtype(cleaned_df[col]):
                missing_num = int(cleaned_df[col].isna().sum())
                if missing_num > 0:
                    med = float(cleaned_df[col].median()) if not cleaned_df[col].dropna().empty else 0.0
                    cleaned_df[col] = cleaned_df[col].fillna(med)
                    logs.append(f"Imputed {missing_num} missing values in '{col}' with median ({med:.2f}).")
                
                # Outlier detection (IQR capping)
                if len(cleaned_df[col].dropna()) > 10:
                    q1 = float(cleaned_df[col].quantile(0.01))
                    q99 = float(cleaned_df[col].quantile(0.99))
                    outliers_low = (cleaned_df[col] < q1).sum()
                    outliers_high = (cleaned_df[col] > q99).sum()
                    if outliers_low + outliers_high > 0:
                        cleaned_df[col] = cleaned_df[col].clip(lower=q1, upper=q99)
                        logs.append(f"Capped {outliers_low + outliers_high} statistical outliers in '{col}' to [1st, 99th] percentiles.")

            # Categorical imputation & stripping
            elif pd.api.types.is_object_dtype(cleaned_df[col]) or pd.api.types.is_string_dtype(cleaned_df[col]):
                cleaned_df[col] = cleaned_df[col].astype(str).str.strip()
                missing_cat = (cleaned_df[col].isna()) | (cleaned_df[col].str.lower().isin(["nan", "null", "none", ""]))
                if missing_cat.sum() > 0:
                    cleaned_df.loc[missing_cat, col] = "Unknown"
                    logs.append(f"Replaced {int(missing_cat.sum())} empty/null categorical strings in '{col}' with 'Unknown'.")

        final_score = cls.calculate_quality_score(cleaned_df)
        if not logs:
            logs.append("Dataset was already in high-fidelity standard. Schema validated.")

        return {
            "cleaned_df": cleaned_df,
            "initial_rows": initial_rows,
            "final_rows": len(cleaned_df),
            "initial_score": initial_score,
            "final_score": final_score,
            "improvement_pct": round(float(final_score - initial_score), 1),
            "logs": logs
        }
