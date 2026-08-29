import os
import json
import pandas as pd
import numpy as np
import requests
import io

class DatasetIngestionManager:
    def __init__(self, catalog_dir="storage/datasets"):
        self.catalog_dir = catalog_dir
        os.makedirs(self.catalog_dir, exist_ok=True)
        self.datasets = {}
        self.preload_defaults()

    def preload_defaults(self):
        default_files = {
            "ecommerce_sales": "data/ecommerce_sales.csv",
            "indian_financial_gst": "data/indian_financial_gst.csv",
            "customer_churn": "data/customer_churn.csv",
            "iot_sensor_stream": "data/iot_sensor_stream.json"
        }
        for name, path in default_files.items():
            if os.path.exists(path):
                if path.endswith(".csv"):
                    df = pd.read_csv(path)
                elif path.endswith(".json"):
                    df = pd.read_json(path)
                self.register_dataset(name, df, source_type="built-in", file_path=path)

    def register_dataset(self, name, df, source_type="upload", file_path=None):
        meta = {
            "name": name,
            "row_count": int(len(df)),
            "col_count": int(len(df.columns)),
            "columns": list(df.columns),
            "dtypes": {col: str(dtype) for col, dtype in df.dtypes.items()},
            "memory_usage_kb": round(float(df.memory_usage(deep=True).sum() / 1024.0), 2),
            "source_type": source_type,
            "file_path": file_path
        }
        self.datasets[name] = {
            "df": df,
            "metadata": meta
        }
        return meta

    def ingest_file(self, file_name, content_bytes):
        name = os.path.splitext(file_name)[0].lower().replace(" ", "_").replace("-", "_")
        ext = os.path.splitext(file_name)[1].lower()
        if ext == ".csv" or ext == ".tsv":
            df = pd.read_csv(io.BytesIO(content_bytes), sep="\t" if ext == ".tsv" else ",")
        elif ext == ".json":
            df = pd.read_json(io.BytesIO(content_bytes))
        elif ext in [".xlsx", ".xls"]:
            df = pd.read_excel(io.BytesIO(content_bytes))
        elif ext == ".parquet":
            df = pd.read_parquet(io.BytesIO(content_bytes))
        else:
            raise ValueError(f"Unsupported file extension: {ext}")
        
        save_path = os.path.join(self.catalog_dir, f"{name}.csv")
        df.to_csv(save_path, index=False)
        return self.register_dataset(name, df, source_type="file_upload", file_path=save_path)

    def ingest_api(self, name, url, headers=None, json_path=None):
        resp = requests.get(url, headers=headers or {}, timeout=15)
        resp.raise_for_status()
        data = resp.json()
        if json_path and isinstance(data, dict) and json_path in data:
            data = data[json_path]
        df = pd.json_normalize(data)
        save_path = os.path.join(self.catalog_dir, f"{name}.csv")
        df.to_csv(save_path, index=False)
        return self.register_dataset(name, df, source_type="rest_api", file_path=save_path)

    def generate_iot_telemetry(self, machine_id="ROBOT-X9", count=20):
        import time
        now = time.time()
        records = []
        for i in range(count):
            t = pd.to_datetime(now + i*60, unit="s").isoformat()
            is_anomaly = (i % 7 == 0)
            records.append({
                "timestamp": t,
                "machine_id": machine_id,
                "temperature_c": round(65.0 + (30.0 if is_anomaly else np.random.uniform(-3, 5)), 2),
                "vibration_hz": round(40.0 + (40.0 if is_anomaly else np.random.uniform(-2, 4)), 2),
                "pressure_psi": round(120.0 + (45.0 if is_anomaly else np.random.uniform(-5, 5)), 2),
                "voltage_v": round(230.0 + (15.0 if is_anomaly else np.random.uniform(-1, 2)), 2),
                "operating_status": "CRITICAL" if is_anomaly else "NORMAL",
                "anomaly_flag": 1 if is_anomaly else 0
            })
        df = pd.DataFrame(records)
        name = f"iot_stream_{machine_id.lower().replace('-', '_')}"
        return self.register_dataset(name, df, source_type="iot_stream")

    def get_dataset(self, name):
        if name in self.datasets:
            return self.datasets[name]["df"]
        return None

    def list_datasets(self):
        return [ds["metadata"] for ds in self.datasets.values()]
