import re
import hashlib
import pandas as pd

class PIISecurityEngine:
    PATTERNS = {
        "Aadhaar_Number": r"\b\d{4}\s?\d{4}\s?\d{4}\b",
        "Indian_PAN": r"\b[A-Z]{5}[0-9]{4}[A-Z]\b",
        "Credit_Card": r"\b(?:4[0-9]{12}(?:[0-9]{3})?|5[1-5][0-9]{14}|6(?:011|5[0-9][0-9])[0-9]{12}|3[47][0-9]{13})\b|\b(?:\d{4}[-\s]?){3}\d{4}\b",
        "Email_Address": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",
        "Phone_Number": r"\b(?:\+91[\-\s]?)?[6789]\d{9}\b",
        "US_SSN": r"\b\d{3}-\d{2}-\d{4}\b"
    }

    @classmethod
    def scan_dataframe(cls, df):
        findings = []
        for col in df.columns:
            sample_values = df[col].dropna().astype(str).head(50).tolist()
            for pii_type, regex_pattern in cls.PATTERNS.items():
                match_count = sum(1 for val in sample_values if re.search(regex_pattern, val))
                if match_count > 0:
                    findings.append({
                        "column": col,
                        "pii_type": pii_type,
                        "matched_samples": match_count,
                        "severity": "CRITICAL" if pii_type in ["Aadhaar_Number", "Credit_Card", "Indian_PAN"] else "HIGH",
                        "recommended_action": "Mask with SHA-256 or redact before export"
                    })
        return findings

    @classmethod
    def mask_value(cls, val, pii_type, method="redact"):
        val_str = str(val)
        if method == "redact":
            if pii_type == "Aadhaar_Number":
                return "XXXX-XXXX-" + val_str[-4:] if len(val_str) >= 4 else "XXXX-XXXX-XXXX"
            elif pii_type == "Indian_PAN":
                return val_str[:2] + "XXXXX" + val_str[-2:] if len(val_str) >= 5 else "XXXXX0000X"
            elif pii_type == "Credit_Card":
                return "****-****-****-" + val_str[-4:] if len(val_str) >= 4 else "****-****-****-****"
            elif pii_type == "Email_Address":
                parts = val_str.split("@")
                return (parts[0][:2] + "***@" + parts[1]) if len(parts) == 2 else "hidden@domain.com"
            elif pii_type == "Phone_Number":
                return "+91-XXXXX-" + val_str[-4:] if len(val_str) >= 4 else "+91-XXXXX-0000"
            return "[REDACTED_PII]"
        elif method == "hash":
            return hashlib.sha256(val_str.encode("utf-8")).hexdigest()[:16]
        return val

    @classmethod
    def mask_dataframe(cls, df, method="redact"):
        masked_df = df.copy()
        findings = cls.scan_dataframe(df)
        masked_summary = []
        for item in findings:
            col = item["column"]
            pii_type = item["pii_type"]
            pattern = cls.PATTERNS[pii_type]
            
            def repl(cell):
                s = str(cell)
                if re.search(pattern, s):
                    return cls.mask_value(s, pii_type, method=method)
                return cell

            masked_df[col] = masked_df[col].apply(repl)
            masked_summary.append(f"Sanitized column '{col}' ({pii_type}) using {method.upper()} masking.")

        return masked_df, masked_summary
