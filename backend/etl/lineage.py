import time

class DataLineageManager:
    def __init__(self):
        self.lineage_graph = {}
        self.snapshots = {}

    def record_node(self, dataset_name, parents=None, operation="ingestion", metadata=None):
        node_id = f"{dataset_name}_{int(time.time()*1000)}"
        self.lineage_graph[dataset_name] = {
            "id": node_id,
            "dataset_name": dataset_name,
            "parents": parents or [],
            "operation": operation,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "metadata": metadata or {}
        }
        return self.lineage_graph[dataset_name]

    def create_snapshot(self, dataset_name, df, version_label=None):
        if dataset_name not in self.snapshots:
            self.snapshots[dataset_name] = []
        ver = version_label or f"v1.{len(self.snapshots[dataset_name])}"
        snap = {
            "version": ver,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "row_count": len(df),
            "df": df.copy()
        }
        self.snapshots[dataset_name].append(snap)
        return snap

    def get_lineage(self, dataset_name):
        nodes = []
        edges = []
        if dataset_name in self.lineage_graph:
            node = self.lineage_graph[dataset_name]
            nodes.append({"id": node["dataset_name"], "label": f"{node['dataset_name']} ({node['operation']})"})
            for p in node["parents"]:
                nodes.append({"id": p, "label": p})
                edges.append({"source": p, "target": node["dataset_name"]})
        return {"nodes": nodes, "edges": edges}
